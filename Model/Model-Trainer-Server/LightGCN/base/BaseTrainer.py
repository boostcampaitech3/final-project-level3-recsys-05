import os
import torch
from abc import abstractmethod
import mlflow
import pickle

PICKLE_PROTOCOL = 4

class BaseTrainer:
    """
    Base class for all trainers
    """
    def __init__(self, model, optimizer, data_loader, valid_data_loader, config):

        self.model = model
        self.optimizer = optimizer
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.data_loader = data_loader
        self.valid_data_loader = valid_data_loader
        
        self.config = config
        self.epochs = config.epochs
        self.save_dir = config.save_dir
        self.model_name = config.model_name

        self.start_epoch = 1
        self.best_epoch = 0
        self.best_loss = 0
        self.best_hit = 0
        self.best_ndcg = 0

    @abstractmethod
    def _train_epoch(self):
        """
        Training logic for an epoch

        :param epoch: Current epoch number
        """
        raise NotImplementedError
    
    @abstractmethod
    def _valid_epoch(self):
        """
        Training logic for an epoch

        :param epoch: Current epoch number
        """
        raise NotImplementedError

    def train(self):
        """
        Full training logic
        """

        for epoch in range(self.start_epoch, self.epochs + 1):
            train_loss = self._train_epoch()
            hit, ndcg = self._valid_epoch()
            print(f'Epoch: {epoch:3d}| Train loss: {train_loss:.5f}| NDCG@10: {ndcg:.5f}| HIT@10: {hit:.5f}')

            if self.best_ndcg < ndcg:
                self.best_epoch, self.best_loss, self.best_hit, self.best_ndcg = epoch, train_loss, hit, ndcg
                torch.save(self.model.state_dict(), os.path.join(self.save_dir, self.model_name + '.pt'))
                mlflow.pytorch.log_state_dict(self.model.state_dict(), self.model_name)
            
            mlflow.log_metric('Train_loss', train_loss)
            mlflow.log_metric('NDCG_10', ndcg)
            mlflow.log_metric('HIT_10', hit)

        self.model.load_state_dict(torch.load(os.path.join(self.save_dir, self.model_name + '.pt')))
        mlflow.pytorch.log_state_dict(self.model.state_dict(), self.model_name)

        # Embedding 저징
        embedding = self.model.i_final_embeddings.detach().cpu().numpy()
        with open(os.path.join(self.save_dir, self.config.embedding_name + '.pickle'), 'wb') as file:
            pickle.dump(embedding, file, protocol = PICKLE_PROTOCOL)

        mlflow.log_artifact(os.path.join(self.save_dir, self.config.embedding_name + '.pickle'), "Embedding")

        print(f'BEST | Epoch: {self.best_epoch:3d}| Train loss: {self.best_loss:.5f}| NDCG@10: {self.best_ndcg:.5f}| HIT@10: {self.best_hit:.5f}')
