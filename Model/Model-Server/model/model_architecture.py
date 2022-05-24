import gc
import math

import torch
import torch.nn as nn
import torch.nn.functional as F

class ScaledDotProductAttention(nn.Module):
    def __init__(self, hidden_units, dropout_rate):
        super(ScaledDotProductAttention, self).__init__()
        self.hidden_units = hidden_units
        self.dropout = nn.Dropout(dropout_rate)

    def forward(self, Q, K, V, mask):
        """
        Q, K, V : (batch_size, num_heads, max_len, hidden_units)
        mask : (batch_size, 1, max_len, max_len)
        """
        attn_score = torch.matmul(Q, K.transpose(2, 3)) / math.sqrt(self.hidden_units) # (batch_size, num_heads, max_len, max_len)
        attn_score = attn_score.masked_fill(mask == 0, -1e9)  # 유사도가 0인 지점은 -infinity로 보내 softmax 결과가 0이 되도록 함
        attn_dist = self.dropout(F.softmax(attn_score, dim=-1))  # attention distribution
        output = torch.matmul(attn_dist, V)  # (batch_size, num_heads, max_len, hidden_units) / # dim of output : batchSize x num_head x seqLen x hidden_units
        return output, attn_dist


class MultiHeadAttention(nn.Module):
    def __init__(self, num_heads, hidden_units, dropout_rate):
        super(MultiHeadAttention, self).__init__()
        self.num_heads = num_heads # head의 수
        self.hidden_units = hidden_units
        
        # query, key, value, output 생성을 위해 Linear 모델 생성
        self.W_Q = nn.Linear(hidden_units, hidden_units, bias=False)
        self.W_K = nn.Linear(hidden_units, hidden_units, bias=False)
        self.W_V = nn.Linear(hidden_units, hidden_units, bias=False)
        self.W_O = nn.Linear(hidden_units, hidden_units, bias=False)

        self.attention = ScaledDotProductAttention(hidden_units, dropout_rate)
        self.dropout = nn.Dropout(dropout_rate) # dropout rate
        self.layerNorm = nn.LayerNorm(hidden_units, 1e-6) # layer normalization

    def forward(self, enc, mask):
        """
        enc : (batch_size, max_len, hidden_units)
        mask : (batch_size, 1, max_len, max_len)
        
        """
        residual = enc # residual connection을 위해 residual 부분을 저장
        batch_size, seqlen = enc.size(0), enc.size(1)

        # Query, Key, Value를 (num_head)개의 Head로 나누어 각기 다른 Linear projection을 통과시킴
        Q = self.W_Q(enc).view(batch_size, seqlen, self.num_heads, self.hidden_units // self.num_heads) # (batch_size, max_len, num_heads, hidden_units)
        K = self.W_K(enc).view(batch_size, seqlen, self.num_heads, self.hidden_units // self.num_heads) # (batch_size, max_len, num_heads, hidden_units)
        V = self.W_V(enc).view(batch_size, seqlen, self.num_heads, self.hidden_units // self.num_heads) # (batch_size, max_len, num_heads, hidden_units)

        # Head별로 각기 다른 attention이 가능하도록 Transpose 후 각각 attention에 통과시킴
        Q, K, V = Q.transpose(1, 2), K.transpose(1, 2), V.transpose(1, 2) # (batch_size, num_heads, max_len, hidden_units)
        output, attn_dist = self.attention(Q, K, V, mask) # output : (batch_size, num_heads, max_len, hidden_units) / attn_dist : (batch_size, num_heads, max_len, max_len)

        # 다시 Transpose한 후 모든 head들의 attention 결과를 합칩니다.
        output = output.transpose(1, 2).contiguous() # (batch_size, max_len, num_heads, hidden_units) / contiguous() : 가변적 메모리 할당
        output = output.view(batch_size, seqlen, -1) # (batch_size, max_len, hidden_units * num_heads)

        # Linear Projection, Dropout, Residual sum, and Layer Normalization
        output = self.layerNorm(self.dropout(self.W_O(output)) + residual) # (batch_size, max_len, hidden_units)
        return output, attn_dist


class PositionwiseFeedForward(nn.Module):
    def __init__(self, hidden_units, dropout_rate):
        super(PositionwiseFeedForward, self).__init__()

        self.W_1 = nn.Linear(hidden_units, hidden_units)
        self.W_2 = nn.Linear(hidden_units, hidden_units)
        self.dropout = nn.Dropout(dropout_rate)
        self.layerNorm = nn.LayerNorm(hidden_units, 1e-6) # layer normalization

    def forward(self, x):
        residual = x
        output = self.W_2(F.relu(self.dropout(self.W_1(x))))
        output = self.layerNorm(self.dropout(output) + residual)
        return output


class SASRecBlock(nn.Module):
    def __init__(self, num_heads, hidden_units, dropout_rate):
        super(SASRecBlock, self).__init__()
        self.attention = MultiHeadAttention(num_heads, hidden_units, dropout_rate)
        self.pointwise_feedforward = PositionwiseFeedForward(hidden_units, dropout_rate)

    def forward(self, input_enc, mask):
        """
        input_enc : (batch_size, max_len, hidden_units)
        mask : (batch_size, 1, max_len, max_len)
        """
        output_enc, attn_dist = self.attention(input_enc, mask)
        output_enc = self.pointwise_feedforward(output_enc)
        return output_enc, attn_dist


class SASRec(nn.Module):
    def __init__(
        self, 
        num_assessmentItemID,
        hidden_units,
        num_heads, 
        num_layers, 
        dropout_rate):
        super(SASRec, self).__init__()

        self.assessmentItemID_emb = nn.Embedding(num_assessmentItemID + 1, hidden_units, padding_idx = 0) # 문항에 대한 정보

        self.blocks = nn.ModuleList([SASRecBlock(num_heads, hidden_units, dropout_rate) for _ in range(num_layers)])

        self.lstm = nn.LSTM(
            input_size = hidden_units,
            hidden_size = hidden_units,
            num_layers = num_layers,
            batch_first = True,
            bidirectional = False,
            dropout = dropout_rate,
            )
        
        self.predict_layer = nn.Sequential(
            nn.Linear(hidden_units, num_assessmentItemID)
        )
        
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    
    def forward(self, input):
        """
        assessmentItem : (batch_size, max_len)
        """
        assessmentItem = input['assessmentItem']

        # masking
        mask_pad = torch.BoolTensor(assessmentItem > 0).unsqueeze(1).unsqueeze(1) # (batch_size, 1, 1, max_len)
        mask_time = (1 - torch.triu(torch.ones((1, 1, assessmentItem.size(1), assessmentItem.size(1))), diagonal=1)).bool() # (batch_size, 1, max_len, max_len)
        mask = (mask_pad & mask_time).to(self.device) # (batch_size, 1, max_len, max_len)

        assessmentItem_emb = self.assessmentItemID_emb(assessmentItem.to(self.device))
        for block in self.blocks:
            assessmentItem_emb, attn_dist = block(assessmentItem_emb, mask)

        assessmentItem_emb, _ = self.lstm(assessmentItem_emb)
        
        output = self.predict_layer(assessmentItem_emb[:, -1])

        return output

class MultiModalSASRec(nn.Module):
    def __init__(
        self, 
        num_assessmentItemID,
        hidden_units,
        num_heads, 
        num_layers, 
        dropout_rate):
        super(MultiModalSASRec, self).__init__()

        self.item2vec_emb = nn.Embedding(num_assessmentItemID + 1, hidden_units, padding_idx = 0) # 문항에 대한 정보
        self.assessmentItemID_emb = nn.Embedding(num_assessmentItemID + 1, hidden_units, padding_idx = 0) # 문항에 대한 정보
        self.emb = nn.Sequential(
            nn.Linear(hidden_units * 2, hidden_units),
            nn.LayerNorm(hidden_units, eps=1e-6)
        )

        self.blocks = nn.ModuleList([SASRecBlock(num_heads, hidden_units, dropout_rate) for _ in range(num_layers)])

        self.lstm = nn.LSTM(
            input_size = hidden_units,
            hidden_size = hidden_units,
            num_layers = num_layers,
            batch_first = True,
            bidirectional = False,
            dropout = dropout_rate,
            )
        
        self.predict_layer = nn.Sequential(
            nn.Linear(hidden_units, num_assessmentItemID)
        )
        
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    
    def forward(self, input):
        """
        assessmentItem : (batch_size, max_len)
        """
        assessmentItem = input['assessmentItem']

        # masking
        mask_pad = torch.BoolTensor(assessmentItem > 0).unsqueeze(1).unsqueeze(1) # (batch_size, 1, 1, max_len)
        mask_time = (1 - torch.triu(torch.ones((1, 1, assessmentItem.size(1), assessmentItem.size(1))), diagonal=1)).bool() # (batch_size, 1, max_len, max_len)
        mask = (mask_pad & mask_time).to(self.device) # (batch_size, 1, max_len, max_len)

        assessmentItem_emb = self.assessmentItemID_emb(assessmentItem.to(self.device))
        item2vec_emb = self.item2vec_emb(assessmentItem.to(self.device))
        
        emb = torch.concat([assessmentItem_emb, item2vec_emb], dim = -1)
        emb = self.emb(emb)

        for block in self.blocks:
            emb, attn_dist = block(emb, mask)

        emb, _ = self.lstm(emb)
        
        output = self.predict_layer(emb[:, -1])

        return output


class EASE():
    def __init__(self, reg = 1000):
        self.reg = reg
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    def clear_memory(self):
        gc.collect()
        torch.cuda.empty_cache()

    def fit(self, X):
        X = X.to(self.device)
        G = X.t() @ X
        diagIndices = torch.eye(G.shape[0]) == 1
        G[diagIndices] += self.reg

        P = G.inverse()
        B = P / (-1 * P.diag())
        B[diagIndices] = 0

        self.B = B.cpu()
    
    def predict(self, X):
        output = (X.to(self.device) @ self.B.to(self.device)).cpu()
        return output