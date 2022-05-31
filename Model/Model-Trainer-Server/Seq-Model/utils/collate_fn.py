import torch
import numpy as np

def pad_sequence(seq, max_len, padding_value = 0):
    try:
        seq_len, col = seq.shape
        padding = np.zeros((max_len - seq_len, col)) + padding_value
    except:
        seq_len = seq.shape[0]
        padding = np.zeros((max_len - seq_len, )) + padding_value

    padding_seq = np.concatenate([padding, seq])

    return padding_seq


def make_collate_fn(samples):
    max_len = 0
    for sample in samples:
        seq_len = sample['problem'].shape[0]
        if max_len < seq_len:
            max_len = seq_len
    
    problems = []
    targets = []

    for sample in samples:
        problems += [pad_sequence(sample['problem'], max_len = max_len, padding_value = 0)]
        targets += [sample['target']]

    return {
        'problems' : torch.tensor(problems, dtype = torch.long), 
        'targets': torch.tensor(targets, dtype = torch.long),
    }