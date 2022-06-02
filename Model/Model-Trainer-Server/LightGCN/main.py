import os
import argparse
from box import Box
from utils.config import ConfigParser

import random
import numpy as np
import mlflow

import torch

from preprocess.preprocess import Preprocess
from dataset.datasets import TrainCustomDataset, ValidCustomDataset
from torch.utils.data import DataLoader
from utils.collate_fn import train_make_collate_fn, valid_make_collate_fn
from model.model import LightGCN
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
    R, user_to_items_train_dict, user_to_items_valid_dict = preprocess.get_R(), preprocess.get_train_dict(), preprocess.get_valid_dict()

    seed_everything(config.seed)

    train_dataset = TrainCustomDataset(num_user=config.num_user, num_item=config.num_item, user_to_items=user_to_items_train_dict)
    train_data_loader = DataLoader(
        train_dataset, 
        batch_size = config.batch_size, 
        shuffle = True, 
        drop_last = False,
        collate_fn = train_make_collate_fn,
        num_workers = config.num_workers)

    valid_dataset = ValidCustomDataset(num_user=config.num_user)
    valid_data_loader = DataLoader(
            valid_dataset, 
            batch_size = config.batch_size, 
            shuffle = False, 
            drop_last = False,
            collate_fn = valid_make_collate_fn,
            num_workers = config.num_workers)
    
    model = LightGCN(
        num_user=config.num_user,
        num_item=config.num_item,
        hidden_units=config.hidden_units,
        n_layers=config.n_layers,
        reg=config.reg,
        node_dropout_rate=config.node_dropout_rate,
        R=R
        ).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr = config.lr)

    trainer = Trainer(
        model=model,
        optimizer=optimizer,
        data_loader=train_data_loader,
        valid_data_loader=valid_data_loader,
        config=config,
        R=R,
        user_to_items_valid_dict=user_to_items_valid_dict
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
        mlflow.log_param("n_layers", config.n_layers)
        mlflow.log_param("reg", config.reg)
        mlflow.log_param("node_dropout_rate", config.node_dropout_rate)
        mlflow.log_param("lr", config.lr)

        main(config)
    
    # TODO: 모델 학습 완료 후 모델 서빙 서버에 모델 업데이트 requests 보내기 (model_type, run_id, model_name)