import os
import argparse
from box import Box
from utils.config import ConfigParser
import pickle

import random
import numpy as np
import mlflow
import requests

import torch
import torch.nn as nn

from preprocess.preprocess import Preprocess
from dataset.datasets import CustomDataset
from torch.utils.data import DataLoader
from utils.collate_fn import make_collate_fn
from model.model import MultiModal
from trainer.trainer import Trainer


def seed_everything(seed):
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    np.random.seed(seed)
    random.seed(seed)

def main(config):
    
    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    preprocess = Preprocess(config=config, data_dir=config.data_dir, data_name=config.data_name)
    preprocess.load_data()
    train_df, valid_df = preprocess.get_train_data(), preprocess.get_valid_data()

    seed_everything(config.seed)

    train_dataset = CustomDataset(df = train_df)
    train_data_loader = DataLoader(
        train_dataset, 
        batch_size = config.batch_size, 
        shuffle = True, 
        drop_last = False,
        collate_fn = make_collate_fn,
        num_workers = config.num_workers)

    valid_dataset = CustomDataset(df = valid_df)
    valid_data_loader = DataLoader(
            valid_dataset, 
            batch_size = config.batch_size, 
            shuffle = False, 
            drop_last = False,
            collate_fn = make_collate_fn,
            num_workers = config.num_workers)
    
    model = MultiModal(
        num_problem_id=config.num_problem_id,
        hidden_units=config.hidden_units,
        num_heads=config.num_heads,
        num_layers=config.num_layers,
        dropout_rate=config.dropout_rate,
        emb_cols=config.emb_cols,
        ).to(device)

    with torch.no_grad():
        for emb_col in config.emb_cols:
            with open(os.path.join(config.embedding_path, f'{emb_col}.pickle'), 'rb') as file:
                pre_emb = pickle.load(file)
            for idx in range(config.num_problem_id):
                model.emb_dict[emb_col].weight[idx + 1] = torch.tensor(pre_emb[idx]).to(device)

    optimizer = torch.optim.Adam(model.parameters(), lr = config.lr)
    criterion = nn.CrossEntropyLoss()

    trainer = Trainer(
        model=model,
        criterion=criterion,
        optimizer=optimizer,
        data_loader=train_data_loader,
        valid_data_loader=valid_data_loader,
        config=config,
    )

    trainer.train()

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

    # Embedding load
    for emb_col in config.emb_cols:
        client = mlflow.tracking.MlflowClient()
        embedding_path = client.download_artifacts(config.embedding_run_ids[emb_col], "Embedding", "./")
    config.embedding_path = embedding_path

    experiment = mlflow.get_experiment_by_name(config.experiment_name)
    if experiment == None: experiment = mlflow.set_experiment(config.experiment_name)
    
    client = mlflow.tracking.MlflowClient()
    run = client.create_run(experiment.experiment_id)

    with mlflow.start_run(run_id=run.info.run_id):
        mlflow.set_tag('mlflow.user', config.user)

        mlflow.log_param("epochs", config.epochs)
        mlflow.log_param("batch_size", config.batch_size)
        mlflow.log_param("num_workers", config.num_workers)
        mlflow.log_param("hidden_units", config.hidden_units)
        mlflow.log_param("num_heads", config.num_heads)
        mlflow.log_param("num_layers", config.num_layers)
        mlflow.log_param("dropout_rate", config.dropout_rate)
        mlflow.log_param("lr", config.lr)
        mlflow.log_param("emb_cols", config.emb_cols)
        
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