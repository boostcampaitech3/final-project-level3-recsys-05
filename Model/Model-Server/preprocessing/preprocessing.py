import os
import json
import numpy as np

VAL_TO_IDX_DATA_PATH = '/opt/ml/final-project-level3-recsys-05/Model/Model-Server/data'

with open(os.path.join(VAL_TO_IDX_DATA_PATH, 'problemId_to_idx.json'), 'r', encoding = 'utf-8') as f:
    problem_id2idx = json.load(f)

with open(os.path.join(VAL_TO_IDX_DATA_PATH, 'idx_to_problemId.json'), 'r', encoding = 'utf-8') as f:
    idx2problem_id = json.load(f)


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
