import os
import json
import numpy as np

VAL_TO_IDX_DATA_PATH = '/opt/ml/final-project-level3-recsys-05/Model/Model-Serving-Server/db'

with open(os.path.join(VAL_TO_IDX_DATA_PATH, 'problem_id_to_idx.json'), 'r', encoding = 'utf-8') as f:
    problem_id2idx = json.load(f)

with open(os.path.join(VAL_TO_IDX_DATA_PATH, 'idx_to_problem_id.json'), 'r', encoding = 'utf-8') as f:
    idx2problem_id = json.load(f)

with open(os.path.join(VAL_TO_IDX_DATA_PATH, 'problem_id_to_tags.json'), 'r', encoding = 'utf-8') as f:
    problem_id_to_tags = json.load(f)

with open(os.path.join(VAL_TO_IDX_DATA_PATH, 'tag_to_idx.json'), 'r', encoding = 'utf-8') as f:
    tag_to_idx = json.load(f)

with open(os.path.join(VAL_TO_IDX_DATA_PATH, 'idx_to_tag.json'), 'r', encoding = 'utf-8') as f:
    idx_to_tag = json.load(f)

async def problem_seq2idx(problem_seq:list) -> list:
    return_problem_seq = []
    for problem_id in problem_seq:
        try:
            return_problem_seq.append(int(problem_id2idx[problem_id]))
        except:
            continue
    return return_problem_seq


def output2problem_id(output:list) -> list:
    return_problem_seq = []
    for idx in output:
        try:
            return_problem_seq.append(idx2problem_id[str(idx)])
        except:
            continue
    return return_problem_seq


def serch_best_tag(problem_seq:list, top:int = 3) -> list:
    tag_cnt_mat = np.zeros((len(tag_to_idx),))
    for problem_id_idx in problem_seq:
        tags = problem_id_to_tags[idx2problem_id[str(problem_id_idx)]]
        tags = [int(tag_to_idx[tag]) for tag in tags]
        tag_cnt_mat[tags] += 1
    
    best_tag_idx = tag_cnt_mat.argsort()[::-1][:top]
    best_tag = [idx_to_tag[str(tag_idx)] for tag_idx in best_tag_idx]
    return best_tag