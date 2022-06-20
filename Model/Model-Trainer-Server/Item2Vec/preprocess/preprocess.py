import os
import re
import numpy as np
import pandas as pd
from base.BasePreprocess import BasePreprocess

class Preprocess(BasePreprocess):
    def __init__(self, config, data_dir, data_name):
        super().__init__(config, data_dir, data_name)

    def get_train_sentences(self):
        return self.train_sentences

    def make_problem_association_seq(self, df) -> list:
        problem_association_seq_list = set()

        problem_id_list = df['problem_id'].tolist()
        problem_association_list = df['problem_association'].tolist()
        title_list = df['title'].tolist()

        for title, problem_association in zip(title_list, problem_association_list):
            problem_association = eval(problem_association)
            if problem_association:
                problem_association += [title]
                problem_association = sorted(list(set(problem_id_list) & set(re.findall(r'([0-9]+?)번', '#'.join(problem_association)))))
                problem_association_seq_list.add(tuple(problem_association))
        
        problem_association_seq_list = list(map(list, problem_association_seq_list))

        return problem_association_seq_list
    
    def make_problem_level_seq(self, df) -> list:
        problem_level_seq_list = []
        group_df = df.groupby('level')
        for level, g_df in group_df:
            problem_level_seq_list.append(g_df['problem_id'].tolist())
        
        return problem_level_seq_list
    
    def make_problem_tag_seq(self, df) -> list:
        problem_tag_seq_list = []
        tag_list = []

        def get_preprocessing_tags(tags, tag_list):
            tags = eval(tags)
            if tags:
                tags = [tag['key'] for tag in tags]
                tag_list += tags
            return tags

        df['preprocessing_tags'] = df['problem_tags'].apply(lambda x : get_preprocessing_tags(x, tag_list))
        tag_list = list(set(tag_list))
        problem_num_list = df['problem_id'].tolist()

        tag_df = pd.DataFrame(data = np.zeros((len(problem_num_list), len(tag_list))), columns = tag_list, index = problem_num_list)

        for _df in df.iloc:
            tag_df.loc[_df['problem_id'], _df['preprocessing_tags']] = 1

        for tag in tag_list:
            problem_tag_seq = tag_df[tag_df[tag] == 1].index.tolist()
            problem_tag_seq_list.append(problem_tag_seq)
            
        return problem_tag_seq_list

    def preprocessing(self, df):
        used_problem_id = list(self.problem_id2idx.keys())
        df['problem_id'] = df['problem_id'].astype(str)
        df = df.set_index('problem_id').loc[used_problem_id, :].reset_index(drop = False).reset_index(drop = True)

        problem_association_seq = self.make_problem_association_seq(df)
        problem_level_seq = self.make_problem_level_seq(df)
        problem_tag_seq = self.make_problem_tag_seq(df)

        train_sentences = problem_association_seq + problem_level_seq + problem_tag_seq
        self.train_sentences = train_sentences