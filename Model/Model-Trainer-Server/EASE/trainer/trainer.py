import mlflow
import numpy as np
from model.metric import get_hit

class Trainer:
    def __init__(self, model, train_matrix, valid_dict):
        self.model = model
        self.train_matrix = train_matrix
        self.valid_dict = valid_dict
        self.hit = 0

    def train(self):
        """
        Full training logic
        """
        self.model.fit(self.train_matrix)
        self.model.clear_memory()

        output = self.model.predict(self.train_matrix)
        self.model.clear_memory()

        output[self.train_matrix == 1] = -np.Inf
        rec_list = output.argsort(dim = 1)

        for idx, rec in enumerate(rec_list):
            pred = rec.cpu().numpy().tolist()[::-1][:10]
            true = self.valid_dict[idx]
            self.hit += get_hit(pred, true)
        
        self.hit /= len(output)

        print(f'reg: {self.model.reg} | HIT@10 : {self.hit:.5f}')
        mlflow.log_metric('HIT_10', self.hit)