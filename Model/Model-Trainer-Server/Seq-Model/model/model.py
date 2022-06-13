import torch
import torch.nn as nn
import torch.nn.functional as F

from .layer import Block

class SeqModel(nn.Module):
    def __init__(
        self, 
        num_problem_id,
        hidden_units,
        num_heads, 
        num_layers, 
        dropout_rate,
        emb_cols):
        super(SeqModel, self).__init__()

        self.emb_cols = emb_cols
        self.emb_dict = nn.ModuleDict({emb_col : nn.Embedding(num_problem_id + 1, hidden_units, padding_idx = 0) for emb_col in emb_cols})
        self.emb = nn.Sequential(
            nn.Linear(hidden_units * len(emb_cols), hidden_units),
            nn.LayerNorm(hidden_units, eps=1e-6)
        )

        self.blocks = nn.ModuleList([Block(num_heads, hidden_units, dropout_rate) for _ in range(num_layers)])

        self.lstm = nn.LSTM(
            input_size = hidden_units,
            hidden_size = hidden_units,
            num_layers = num_layers,
            batch_first = True,
            bidirectional = False,
            dropout = dropout_rate,
            )
        
        self.predict_layer = nn.Sequential(
            nn.Linear(hidden_units, num_problem_id)
        )
        
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        
    
    def forward(self, input):
        """
        problems : (batch_size, max_len)
        """
        problems = input['problems']

        # masking
        mask_pad = torch.BoolTensor(problems > 0).unsqueeze(1).unsqueeze(1) # (batch_size, 1, 1, max_len)
        mask_time = (1 - torch.triu(torch.ones((1, 1, problems.size(1), problems.size(1))), diagonal=1)).bool() # (batch_size, 1, max_len, max_len)
        mask = (mask_pad & mask_time).to(self.device) # (batch_size, 1, max_len, max_len)

        emb = []
        for emb_col in self.emb_cols:
            emb.append(self.emb_dict[emb_col](problems.to(self.device)))
        
        emb = torch.concat(emb, dim = -1)
        emb = self.emb(emb)

        for block in self.blocks:
            emb, attn_dist = block(emb, mask)

        emb, _ = self.lstm(emb)
        
        output = self.predict_layer(emb[:, -1])

        return output