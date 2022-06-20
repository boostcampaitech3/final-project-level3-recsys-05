import torch
import numpy as np
from base.BaseTrainer import BaseTrainer
from model.metric import get_hit, get_ndcg

class Trainer(BaseTrainer):
    def __init__(self, model, criterion, optimizer, data_loader, valid_data_loader, config):
        super().__init__(model, criterion, optimizer, data_loader, valid_data_loader, config)
    
    def _train_epoch(self):
        self.model.train()
        train_loss = 0

        for input in self.data_loader:
            self.optimizer.zero_grad()
            
            output = self.model(input)
            loss = self.criterion(output, input['targets'].to(self.device))

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
            for input in self.valid_data_loader:
                output = -self.model(input)
                predictions = output.argsort()

                targets = input['targets']

                for target, prediction in zip(targets, predictions):
                    target = [target.item()]
                    prediction = prediction.cpu().tolist()[:10]

                    hit += get_hit(prediction, target)
                    ndcg += get_ndcg(prediction, target)
        
        hit /= len(self.valid_data_loader.dataset)
        ndcg /= len(self.valid_data_loader.dataset)

        return hit, ndcg



