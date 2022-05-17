import os
import json
import numpy as np
from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity

DATA_PATH = '/opt/ml/final-project-level3-recsys-05/Model/Model-Server/preprocessing'
MODEL_PATH = '/opt/ml/final-project-level3-recsys-05/Model/Model-Experiment/model'

with open(os.path.join(DATA_PATH, 'problem_id2idx.json'), 'r', encoding = 'utf-8') as f:
    problem_id2idx = json.load(f)

with open(os.path.join(DATA_PATH, 'idx2problem_id.json'), 'r', encoding = 'utf-8') as f:
    idx2problem_id = json.load(f)

# 'Word2Vec-CBOW-problem_association_seq-problem_level_seq-problem_tag_seq'
# 'Word2Vec-CBOW-problem_association_seq-problem_level_seq-problem_tag_seq-problem_course_seq'
# 'Word2Vec-CBOW-problem_association_seq-problem_level_seq-problem_tag_seq-problem_course_seq-32'
model = Word2Vec.load(os.path.join(MODEL_PATH, 'Word2Vec-CBOW-problem_association_seq-problem_level_seq-problem_tag_seq.model'))

vectors = []
for idx in range(len(model.wv.key_to_index.keys())):
    vectors.append(model.wv[idx2problem_id[str(idx)]])
vectors = np.array(vectors)

def word2vec_model(problem_seq):
    cos_arr = cosine_similarity(model.wv[idx2problem_id[str(problem_seq[0])]].reshape(1, -1), vectors)[0]
    return cos_arr

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