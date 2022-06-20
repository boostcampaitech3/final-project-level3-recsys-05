import os
import random
import torch
import numpy as np
import pandas as pd
from base.BasePreprocess import BasePreprocess

class Preprocess(BasePreprocess):
    def __init__(self, config, data_dir, data_name):
        super().__init__(config, data_dir, data_name)

    def get_total_matrix(self):
        return self.total_matrix

    def get_train_matrix(self):
        return self.train_matrix

    def get_valid_dict(self):
        return self.valid_dict

    def get_problems_to_idx(self, problems):
        problems = eval(problems)
        ret = []
        for problemId in problems:
            try: ret.append(int(self.problem_id2idx[problemId]))
            except: continue
        return ret

    def preprocessing(self, df):
        df['problems_to_idx'] = df['problems'].apply(lambda x : self.get_problems_to_idx(x))
        df = df[df['problems_to_idx'].apply(lambda x : True if len(x) >= 15 else False)].reset_index(drop = True)
        
        user_name_to_idx = {}
        for idx, user_name in enumerate(df['user_name'].tolist()):
            user_name_to_idx[user_name] = idx
        
        total_matrix = torch.zeros(size = (len(user_name_to_idx), len(self.problem_id2idx)))
        train_matrix = torch.zeros(size = (len(user_name_to_idx), len(self.problem_id2idx)))
        valid_dict = {}

        group_df = df.groupby('user_name')
        for user_name, df in group_df:
            random.seed(self.config.seed)
            total = df['problems_to_idx'].values[0]
            valid = random.sample(total, 10)
            train = list(set(total) - set(valid))

            total_matrix[user_name_to_idx[user_name], total] = 1
            train_matrix[user_name_to_idx[user_name], train] = 1
            valid_dict[user_name_to_idx[user_name]] = valid

        self.total_matrix = total_matrix
        self.train_matrix = train_matrix
        self.valid_dict = valid_dict