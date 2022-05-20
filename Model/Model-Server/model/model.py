import os
import json
import pickle
import numpy as np
from scipy.stats import beta
from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity

from .model_architecture import SASRec, EASE

import torch

VAL_TO_IDX_DATA_PATH = '/opt/ml/final-project-level3-recsys-05/Model/Model-Server/data'
MODEL_PATH = '/opt/ml/final-project-level3-recsys-05/Model/Model-Experiment/model'

with open(os.path.join(VAL_TO_IDX_DATA_PATH, 'problemId_to_idx.json'), 'r', encoding = 'utf-8') as f:
    problem_id2idx = json.load(f)

with open(os.path.join(VAL_TO_IDX_DATA_PATH, 'idx_to_problemId.json'), 'r', encoding = 'utf-8') as f:
    idx2problem_id = json.load(f)

# item2vec
# 'Word2Vec-CBOW-problem_association_seq-problem_level_seq-problem_tag_seq'
# 'Word2Vec-CBOW-problem_association_seq-problem_level_seq-problem_tag_seq-problem_course_seq'
# 'Word2Vec-CBOW-problem_association_seq-problem_level_seq-problem_tag_seq-problem_course_seq-32'
# 'Word2Vec-CBOW-problem_association_seq-problem_level_seq-problem_tag_seq-vs128.model'
item2vec = Word2Vec.load(os.path.join(MODEL_PATH, 'Word2Vec-CBOW-problem_association_seq-problem_level_seq-problem_tag_seq-vs128.model'))

vectors = []
for idx in range(len(problem_id2idx)):
    vectors.append(item2vec.wv[idx2problem_id[str(idx)]])
vectors = np.array(vectors)

## Transformer
device = 'cuda' if torch.cuda.is_available() else 'cpu'

num_assessmentItemID = len(problem_id2idx)
hidden_units = 128
num_heads = 8
num_layers = 1
dropout_rate = 0.5
num_workers = 8

# user_seq
user_seq = SASRec(
        num_assessmentItemID = num_assessmentItemID,
        hidden_units = hidden_units,
        num_heads = num_heads,
        num_layers = num_layers,
        dropout_rate = dropout_rate
        ).to(device)

# User-Seq-Transformer
# new-User-Seq-Transformer
user_seq.load_state_dict(torch.load(os.path.join(MODEL_PATH, 'new-User-Seq-Transformer' + '.pt')))

# pretrained_user_seq
pretrained_user_seq = SASRec(
        num_assessmentItemID = num_assessmentItemID,
        hidden_units = hidden_units,
        num_heads = num_heads,
        num_layers = num_layers,
        dropout_rate = dropout_rate
        ).to(device)

# User-Seq-Transformer
# new-Item2Vec-pretrained-User-Seq-Transformer
pretrained_user_seq.load_state_dict(torch.load(os.path.join(MODEL_PATH, 'new-Item2Vec-pretrained-User-Seq-Transformer' + '.pt')))

# ease
class MyCoustomUnpickler(pickle.Unpickler):
    def find_class(self, __module_name: str, __global_name: str):
        if __module_name == '__main__':
            __module_name = __name__
        return super().find_class(__module_name, __global_name)

with open(os.path.join(MODEL_PATH, 'ease.pickle'), 'rb') as file:
    ease = MyCoustomUnpickler(file)
    ease = ease.load()
    ease.device = device

def thompson_sampling(model_type_click_dict):
    '''
    
    model_type_click_dict = {
            'item2vec' : {'pos_click' : 1, 'total_view' : 1},
            'user_seq' : {'pos_click' : 1, 'total_view' : 1},
            'pretrained_user_seq' : {'pos_click' : 1, 'total_view' : 1},
    }

    '''

    A_sampling = beta.rvs(model_type_click_dict['item2vec']['pos_click'], model_type_click_dict['item2vec']['total_view'])
    
    B_sampling = beta.rvs(model_type_click_dict['user_seq']['pos_click'], model_type_click_dict['user_seq']['total_view'])
    
    C_sampling = beta.rvs(model_type_click_dict['pretrained_user_seq']['pos_click'], model_type_click_dict['pretrained_user_seq']['total_view'])
    
    # 가장 값이 높은 추천을 선택
    idx = np.argmax([A_sampling, B_sampling, C_sampling])
    
    if idx == 0: return 'item2vec'
    elif idx == 1: return 'user_seq'
    elif idx == 2: return 'pretrained_user_seq'

def ease_model(problem_seq):
    mat = torch.zeros(size = (1, len(problem_id2idx)))
    mat[0, problem_seq] = 1
    output = ease.predict(mat)[0].cpu().numpy()
    ease.clear_memory()
    return output

def item2vec_model(problem_seq):
    cos_arr = cosine_similarity(item2vec.wv[idx2problem_id[str(problem_seq[0])]].reshape(1, -1), vectors)[0]
    return cos_arr

def user_seq_model(problem_seq):
    user_seq.eval()
    input = {'assessmentItem' : torch.tensor([problem_seq[::-1]]) + 1}
    with torch.no_grad():
        output = user_seq(input)[0].cpu().numpy()
    return output

def pretrained_user_seq_model(problem_seq):
    pretrained_user_seq.eval()
    input = {'assessmentItem' : torch.tensor([problem_seq[::-1]]) + 1}
    with torch.no_grad():
        output = pretrained_user_seq(input)[0].cpu().numpy()
    return output

def output_fitering(output, fiterling_list):
    output[fiterling_list] = -np.Inf
    return output

def output_sorted(output, top = 10):
    output = output.argsort()[::-1][:top]
    return output

def preprocessing_seq_problem_id2idx(problem_seq):
    return_problem_seq = []
    for problem_id in problem_seq:
        try:
            return_problem_seq.append(problem_id2idx[problem_id])
        except:
            continue
    
    return return_problem_seq

def preprocessing_seq_idx2problem_id(output):
    return_problem_seq = []
    for idx in output:
        try:
            return_problem_seq.append(idx2problem_id[str(idx)])
        except:
            continue
    
    return return_problem_seq