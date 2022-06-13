import numpy as np
from torch.utils.data import Dataset

class TrainCustomDataset(Dataset):
    def __init__(self, num_user, num_item, user_to_items):
        self.num_users = []
        self.pos_items = []
        self.neg_items = []
        total_items = [item for item in range(num_item)]

        for user in range(num_user):
            items = user_to_items[user]
            self.pos_items += items
            self.neg_items += np.random.choice(list(set(total_items) - set(items)), len(items)).tolist()
            self.num_users += [user] * len(items)

    def __len__(self):
        return len(self.num_users)

    def __getitem__(self, idx):
        return {
            'user' : self.num_users[idx],
            'pos_item' : self.pos_items[idx],
            'neg_item' : self.neg_items[idx],
            }

class ValidCustomDataset(Dataset):
    def __init__(self, num_user):
        self.num_user = num_user

    def __len__(self):
        return self.num_user

    def __getitem__(self, idx):
        return {
            'user' : idx
            }