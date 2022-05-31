import numpy as np
from torch.utils.data import Dataset

class CustomDataset(Dataset):
    def __init__(self, df):

        self.problems = []
        self.targets = []

        group_df = df.groupby('target')

        for target2idx, g_df in group_df:
            gg_df = g_df.groupby('key')
            for userID, ggg_df in gg_df:
                if len(ggg_df) >= 2:
                    self.problems.append(ggg_df['problem_id2idx'].tolist()[:-1])
                    self.targets.append(ggg_df['problem_id2idx'].tolist()[-1] - 1)

    def __len__(self):
        return len(self.targets)

    def __getitem__(self, idx):
        problem = self.problems[idx]
        target = self.targets[idx]
        return {
            'problem' : np.array(problem), 
            'target' : target,
            }
