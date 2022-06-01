import os
import torch
import pickle
import numpy as np
from abc import abstractmethod
from sklearn.metrics.pairwise import cosine_similarity
from .modules import MultiModal
import mlflow
from mlflow.tracking import MlflowClient

remote_server_uri = "http://34.64.110.227:5000"
mlflow.set_tracking_uri(remote_server_uri)

class ServingBase:
    def __init__(self, run_id:str, model_name:str):
        self.model = self.init_model(run_id, model_name)

    def init_model(self, run_id:str, model_name:str):
        client = MlflowClient()
        local_path = client.download_artifacts(run_id, 'Embedding', './')
        with open(os.path.join(local_path, model_name + '.pickle'), 'rb') as file: 
            model = pickle.load(file)
        return model
    
    @abstractmethod
    def predict(self):
        """
        predict logic
        """
        raise NotImplementedError


class ServingEASE(ServingBase):
    def __init__(self, run_id: str, model_name: str):
        super().__init__(run_id, model_name)

    def predict(self, problem_seq):
        mat = np.zeros(shape = (1, self.model.shape[0]))
        mat[0, problem_seq] = 1
        output = mat @ self.model
        output = output[0]
        return output


class ServingItem2Vec(ServingBase):
    def __init__(self, run_id: str, model_name: str):
        super().__init__(run_id, model_name)

    def predict(self, problem_seq):
        output = cosine_similarity(self.model[problem_seq[0]].reshape(1, -1), self.model)[0]
        return output


class ServingLightGCN(ServingBase):
    def __init__(self, run_id: str, model_name: str):
        super().__init__(run_id, model_name)

    def predict(self, problem_seq):
        output = cosine_similarity(self.model[problem_seq[0]].reshape(1, -1), self.model)[0]
        return output


class ServingMultiModal(ServingBase):
    def __init__(self, run_id: str, model_name: str):
        super().__init__(run_id, model_name)
    
    def init_model(self, run_id, model_name):
        state_dict_uri = f"gs://santa-mlflow-artifact/8/{run_id}/artifacts/{model_name}"
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        model = MultiModal().to(device)
        model.load_state_dict(mlflow.pytorch.load_state_dict(state_dict_uri))
        return model

    def predict(self, problem_seq):
        self.model.eval()
        input = {'assessmentItem' : torch.tensor([problem_seq[::-1]]) + 1}
        with torch.no_grad():
            output = self.model(input)[0].cpu().numpy()
        return output
