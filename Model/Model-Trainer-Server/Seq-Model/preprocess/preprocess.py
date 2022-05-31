import os
import numpy as np
import pandas as pd
from base.BasePreprocess import BasePreprocess

class Preprocess(BasePreprocess):
    def __init__(self, config, data_dir, data_name):
        super().__init__(config, data_dir, data_name)

    def get_train_data(self):
        return self.train_df
    
    def get_valid_data(self):
        return self.valid_df

    def preprocessing(self, df):
        used_problem_id = list(self.problem_id2idx.keys())

        df = df[~(df['problem_id'].isna())].reset_index(drop = True)
        df = df[~(df['user_name'].isna())].reset_index(drop = True)
        
        df['problem_id'] = df['problem_id'].astype(int).astype(str)
        df['target'] = df['target'].astype(int).astype(str)

        df = df.set_index('target').loc[used_problem_id, :].reset_index(drop = False)
        df = df.set_index('problem_id').loc[used_problem_id, :].reset_index(drop = False)
        
        df['key'] = df['user_name'] + '-' + df['target']
        df = df.sort_values(['key', 'date']).reset_index(drop = True)

        group_df = df.groupby('key')
        
        new_df = []
        for key, g_df in group_df:
            new_df.append(g_df[~(g_df.duplicated('problem_id'))].copy())

        df = pd.concat(new_df).reset_index(drop = True)

        df['problem_id2idx'] = df['problem_id'].apply(lambda x : int(self.problem_id2idx[x]) + 1)

        train_df = []
        valid_df = []

        group_df = df.groupby('target')
        for target, g_df in group_df:
            gg_df = g_df.groupby('key')
            for idx, (userID, ggg_df) in enumerate(gg_df):
                if idx == 0: valid_df.append(ggg_df)
                else: train_df.append(ggg_df)

        self.train_df = pd.concat(train_df).reset_index(drop = True)
        self.valid_df = pd.concat(valid_df).reset_index(drop = True)
        self.config.num_problem_id = len(self.problem_id2idx)