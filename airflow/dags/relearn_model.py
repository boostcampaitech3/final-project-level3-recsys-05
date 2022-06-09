from airflow.models import DAG
from airflow.contrib.operators.ssh_operator import SSHOperator
from airflow.operators.python import PythonOperator

from datetime import datetime, timedelta

default_args = {
    "owner": "airflow",
    "email_on_failure": False,
    "email_on_retry": False,
    "email": "kgw7401@gmail.com",
    "retries": 1,
    "retry_delay": timedelta(minutes=5)
}

def test():
    print("trigger complete!!!")

with DAG("relearn_model", start_date=datetime(2022, 6, 8), 
    schedule_interval="* * * * *", default_args=default_args, catchup=False) as dag:

    start_learning = SSHOperator(
        task_id="start_learning",
        ssh_conn_id="",
        command="",
        get_pty=True,
        queue=f"worker"
    )