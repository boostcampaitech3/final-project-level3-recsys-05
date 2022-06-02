import os
import argparse
from box import Box
from utils.config import ConfigParser
import pickle

import numpy as np
import mlflow

from preprocess.preprocess import Preprocess
from trainer.trainer import Trainer
from gensim.models import Word2Vec

PICKLE_PROTOCOL = 4

def main(config):

    preprocess = Preprocess(config=config, data_dir=config.data_dir, data_name=config.data_name)
    preprocess.load_data()
    train_sentences = preprocess.get_train_sentences()

    trainer = Trainer(config=config)

    model = Word2Vec(
                sentences = train_sentences,
                seed = config.seed,
                epochs = config.epochs,
                min_count = config.min_count,
                vector_size = config.vector_size,
                sg = config.sg,
                negative = config.negative,
                window = config.window,
                compute_loss = True, 
                callbacks=[trainer],
    )

    model = Word2Vec.load(os.path.join(config.save_dir, config.model_name + '.model'))

    embedding = []
    idx2problem_id = preprocess.idx2problem_id
    for idx in range(len(idx2problem_id)):
        embedding.append(model.wv[idx2problem_id[str(idx)]])
    embedding = np.array(embedding)

    with open(os.path.join(config.save_dir, config.model_name + '.pickle'), 'wb') as file:
            pickle.dump(embedding, file, protocol = PICKLE_PROTOCOL)

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

        mlflow.log_param("seed", config.seed)
        mlflow.log_param("epochs", config.epochs)
        mlflow.log_param("min_count", config.min_count)
        mlflow.log_param("vector_size", config.vector_size)
        mlflow.log_param("sg", config.sg)
        mlflow.log_param("negative", config.negative)
        mlflow.log_param("window", config.window)

        main(config)
    
    # TODO: 모델 학습 완료 후 모델 서빙 서버에 모델 업데이트 requests 보내기 (model_type, run_id, model_name)