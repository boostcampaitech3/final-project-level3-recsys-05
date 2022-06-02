import os
import random
import numpy as np
import pandas as pd
import scipy.sparse as sp
from base.BasePreprocess import BasePreprocess

class Preprocess(BasePreprocess):
    def __init__(self, config, data_dir, data_name):
        super().__init__(config, data_dir, data_name)

    def get_R(self):
        return self.R
    
    def get_train_dict(self):
        return self.train_dict

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

        num_user = len(user_name_to_idx)
        num_item = len(self.problem_id2idx)

        R = sp.dok_matrix((num_user, num_item), dtype=np.float32)
        train_dict = {}
        valid_dict = {}

        group_df = df.groupby('user_name')
        for user_name, df in group_df:
            random.seed(self.config.seed)
            total = df['problems_to_idx'].values[0]
            valid = random.sample(total, 10)
            train = list(set(total) - set(valid))

            R[user_name_to_idx[user_name], train] = 1

            train_dict[user_name_to_idx[user_name]] = train
            valid_dict[user_name_to_idx[user_name]] = valid

        self.R = R
        self.train_dict = train_dict
        self.valid_dict = valid_dict
        self.config.num_user = num_user
        self.config.num_item = num_item