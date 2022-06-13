import torch
import numpy as np
from base.BaseTrainer import BaseTrainer
from model.metric import get_hit, get_ndcg

class Trainer(BaseTrainer):
    def __init__(self, model, optimizer, data_loader, valid_data_loader, config, R, user_to_items_valid_dict):
        super().__init__(model, optimizer, data_loader, valid_data_loader, config)
        self.R = R
        self.user_to_items_valid_dict = user_to_items_valid_dict
    
    def _train_epoch(self):
        self.model.train()
        train_loss = 0

        for input in self.data_loader:
            self.optimizer.zero_grad()

            loss = self.model(input['users'], input['pos_items'], input['neg_items'])
            loss.backward()

            self.optimizer.step()
            train_loss += loss.item()
            
        train_loss /= len(self.data_loader)

        return train_loss
    
    def _valid_epoch(self):
        self.model.eval()
        hit = 0
        ndcg = 0
        with torch.no_grad():
            score = torch.mm(self.model.u_final_embeddings, self.model.i_final_embeddings.T)
            score[self.R.todense() == 1] = -np.Inf

        for users in self.valid_data_loader:
            users_rec = score[users]
            users_rec = users_rec.argsort()
            for user, user_rec in zip(users, users_rec):
                prediction = user_rec.cpu().numpy().tolist()[::-1][:10]
                target = self.user_to_items_valid_dict[user]

                hit += get_hit(prediction, target)
                ndcg += get_ndcg(prediction, target)
        
        hit /= len(self.valid_data_loader.dataset)
        ndcg /= len(self.valid_data_loader.dataset)

        return hit, ndcg



