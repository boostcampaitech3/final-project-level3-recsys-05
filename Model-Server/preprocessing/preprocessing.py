import json

with open('/opt/ml/final-project-level3-recsys-05/Model-Server/preprocessing/problem_id2idx.json', 'r', encoding = 'utf-8') as f:
    problem_id2idx = json.load(f)

with open('/opt/ml/final-project-level3-recsys-05/Model-Server/preprocessing/idx2problem_id.json', 'r', encoding = 'utf-8') as f:
    idx2problem_id = json.load(f)

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
