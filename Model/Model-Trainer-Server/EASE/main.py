import os
import argparse
from box import Box
from utils.config import ConfigParser
import pickle
import requests

import mlflow

from preprocess.preprocess import Preprocess
from model.model import EASE
from trainer.trainer import Trainer

PICKLE_PROTOCOL = 4

def main(config):
    
    preprocess = Preprocess(config=config, data_dir=config.data_dir, data_name=config.data_name)
    preprocess.load_data()
    
    train_matrix = preprocess.get_train_matrix()
    valid_dict = preprocess.get_valid_dict()

    model = EASE(reg = config.reg)
    trainer = Trainer(model=model, train_matrix=train_matrix, valid_dict=valid_dict)
    trainer.train()

    total_matrix = preprocess.get_total_matrix()
    model.fit(total_matrix)
    model.clear_memory()

    ease_item_similarity_matrix = model.B.numpy()

    with open(os.path.join(config.save_dir, config.model_name + '.pickle'), 'wb') as file:
            pickle.dump(ease_item_similarity_matrix, file, protocol = PICKLE_PROTOCOL)

    mlflow.log_artifact(os.path.join(config.save_dir, config.model_name + '.pickle'), "Embedding")


if __name__ == '__main__':
    args = argparse.ArgumentParser(description="PyTorch Template")
    
    args.add_argument(
        '-c', 
        '--config', 
        default=None, 
        type=str, 
        help='config file path (default: None)')

    args = args.parse_args()

    config = Box(ConfigParser(args).config)

    if not os.path.isdir(config.save_dir):
        os.mkdir(config.save_dir)

    mlflow.set_tracking_uri(config.remote_server_uri)
    experiment = mlflow.get_experiment_by_name(config.experiment_name)
    if experiment == None: experiment = mlflow.set_experiment(config.experiment_name)
    
    client = mlflow.tracking.MlflowClient()
    run = client.create_run(experiment.experiment_id)

    with mlflow.start_run(run_id=run.info.run_id):
        mlflow.set_tag('mlflow.user', config.user)
        mlflow.log_param("reg", config.reg)
        main(config)
    
    if config.model_update:
        model_update_data = {
            'key': config.model_update_key,
            'model_type': config.model_type,
            "model_name": config.model_name,
            "run_id": run.info.run_id,
        }
        res = requests.post(config.model_update_url, json = model_update_data)
        print(res.json())