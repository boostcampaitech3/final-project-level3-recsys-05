import os
import mlflow
from gensim.models.callbacks import CallbackAny2Vec

class Trainer(CallbackAny2Vec):
    def __init__(self, config):
        self.epoch = 1
        self.total_loss = 0
        self.train_loss = 987654321
        self.config = config

    def on_epoch_end(self, model):
        loss = model.get_latest_training_loss()
        train_loss = loss - self.total_loss
        self.total_loss = loss

        print(f'Epoch: {self.epoch:3d}| Train loss: {train_loss:.5f}')
        mlflow.log_metric('Train_loss', train_loss)
        if train_loss < self.train_loss:
            self.train_loss = train_loss
            model.save(os.path.join(self.config.save_dir, self.config.model_name + '.model'))

        self.epoch += 1



