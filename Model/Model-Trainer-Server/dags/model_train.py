from datetime import timedelta

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

with DAG(
    dag_id="Model-Train",
    description="모델 학습 파이프라인",
    start_date=days_ago(1),
    schedule_interval="0 6 * * *",
    tags=["my_dags"],
) as dag:

    t1 = BashOperator(
        task_id='Item2Vec',
        bash_command="cd /opt/ml/final-project-level3-recsys-05/Model/Model-Trainer-Server/Item2Vec/ && python -W ignore main.py -c config.json",
        owner='sb',
        retries=3,
        retry_delay=timedelta(minutes=3),
    )

    t2 = BashOperator(
        task_id='EASE',
        bash_command="cd /opt/ml/final-project-level3-recsys-05/Model/Model-Trainer-Server/EASE/ && python -W ignore main.py -c config.json",
        owner='sb',
        retries=3,
        retry_delay=timedelta(minutes=3),
    )

    t3 = BashOperator(
        task_id='LightGCN',
        bash_command="cd /opt/ml/final-project-level3-recsys-05/Model/Model-Trainer-Server/LightGCN/ && python -W ignore main.py -c config.json",
        owner='sb',
        retries=3,
        retry_delay=timedelta(minutes=3),
    )

    t4 = BashOperator(
        task_id='Multi-Modal',
        bash_command="cd /opt/ml/final-project-level3-recsys-05/Model/Model-Trainer-Server/Multi-Modal/ && python -W ignore main.py -c config.json",
        owner='sb',
        retries=3,
        retry_delay=timedelta(minutes=3),
    )

    t1 >> t2 >> t3 >> t4