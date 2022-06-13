import os
import json
import numpy as np
import pandas as pd
from abc import abstractmethod


class BasePreprocess:
    def __init__(self, config, data_dir, data_name):
        self.config = config
        self.data_dir = data_dir
        self.data_name = data_name

    @ abstractmethod
    def get_train_sentences(self):
        raise NotImplementedError

    @ abstractmethod
    def make_problem_association_seq(self):
        raise NotImplementedError

    @ abstractmethod
    def make_problem_level_seq(self):
        raise NotImplementedError

    @ abstractmethod
    def make_problem_tag_seq(self):
        raise NotImplementedError

    @ abstractmethod
    def preprocessing(self, df):
        raise NotImplementedError

    def load_data_from_file(self, data_dir, data_name):
        # TODO: GCP 연동
        return pd.read_csv(os.path.join(data_dir, data_name + '.csv'))

    def load_data(self):
        with open(os.path.join(self.data_dir, 'problem_id_to_idx.json'), 'r', encoding = 'utf-8') as f:
            self.problem_id2idx = json.load(f)
        with open(os.path.join(self.data_dir, 'idx_to_problem_id.json'), 'r', encoding = 'utf-8') as f:
            self.idx2problem_id  = json.load(f)
        self.preprocessing(self.load_data_from_file(self.data_dir, self.data_name))