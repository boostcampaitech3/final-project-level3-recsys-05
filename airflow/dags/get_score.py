from airflow.models import DAG, Variable
from airflow.contrib.operators.ssh_operator import SSHOperator
from airflow.contrib.operators.sftp_operator import SFTPOperator
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.providers.google.cloud.sensors.gcs import GCSObjectExistenceSensor
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.operators.bash import BashOperator
from airflow.providers.slack.operators.slack_webhook import SlackWebhookOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

from datetime import datetime, timedelta


import os
import glob
import pandas as pd

default_args = {
    "owner": "airflow",
    "email_on_failure": False,
    "email_on_retry": False,
    "email": "kgw7401@gmail.com",
    "retries": 1,
    "retry_delay": timedelta(minutes=5)
}

def concat_file() -> None:
    save_file_name = "/home/kgw7401/score/score.parquet"
    all_filenames = [i for i in glob.glob('/home/kgw7401/user/score_*.csv')]
    score = pd.concat([pd.read_csv(f) for f in all_filenames])
    score.to_parquet(save_file_name)

def get_message() -> str:
    return "Score Data Upload Success!"


with DAG("get_score", start_date=datetime(2022, 6, 1), 
    schedule_interval=timedelta(minutes=0, hours=2, days=3), default_args=default_args, catchup=False) as dag:

    concat_file = PythonOperator(
        task_id="concat_file",
        python_callable=concat_file,
        queue="master_node"
    )

    worker_node_nums = Variable.get("worker_node_nums")

    for node in range(1, int(worker_node_nums)+1):
        trigger_get_data = SSHOperator(
            task_id=f"trigger_get_data_{node}",
            ssh_conn_id=f"ssh_id_{node}",
            command="nohup python3 /opt/ml/scraping_code/get_score.py & sleep 5",
            get_pty=True,
            queue=f"worker_{node}"
        )

        mv_score_file_to_master = SFTPOperator(
            task_id=f"mv_score_file_to_master_{node}",
            ssh_conn_id=f"ssh_id_{node}",
            local_filepath=f"/home/kgw7401/score/score_{node}.csv",
            remote_filepath=f"/opt/ml/data/score/score_{node}.csv",
            operation="get",
            queue=f"worker_{node}"
        )

        trigger_get_data >> mv_score_file_to_master >> concat_file

    mv_score_local_to_gcs = LocalFilesystemToGCSOperator(
        task_id="mv_score_local_to_gcs",
        gcp_conn_id="google_cloud_conn_id",
        src=os.path.join(os.getcwd(), "score", "score.parquet"),
        dst="score/{{ ds }}-score.parquet",
        bucket="santa-boj-final",
        queue="master_node"
    )

    is_score_gcs_exists = GCSObjectExistenceSensor(
        task_id="is_score_gcs_exists",
        bucket="santa-boj-final",
        object="score/{{ ds }}-score.parquet",
        google_cloud_conn_id ="google_cloud_conn_id",
        queue="master_node"
    )

    mv_score_gcs_to_bq = GCSToBigQueryOperator(
        task_id="mv_score_gcs_to_bq",
        bucket="santa-boj-final",
        source_objects=['score/{{ ds }}-score.parquet'],
        source_format="PARQUET",
        destination_project_dataset_table="santa-boj.dataset.score",
        write_disposition="WRITE_APPEND",
        skip_leading_rows=1,
        gcp_conn_id="google_cloud_conn_id",
        queue="master_node"
    )

    delete_local_score_data = BashOperator(
        task_id="delete_local_score_data",
        bash_command="rm -rf /home/kgw7401/score/score.parquet",
        queue="master_node"
    )

    send_slack_notification = SlackWebhookOperator(
        task_id="send_slack_notification",
        http_conn_id="slack_conn_id",
        message=get_message(),
        channel="#level2-recsys-05-알잘딱깔센-캠퍼만",
        queue="master_node"
    )

    trigger_relearn_model_dag = TriggerDagRunOperator(
        task_id="trigger_relearn_model_dag",
        trigger_dag_id="relearn_model"
    )

    concat_file >> mv_score_local_to_gcs >> is_score_gcs_exists >> mv_score_gcs_to_bq
    mv_score_gcs_to_bq >> delete_local_score_data >> send_slack_notification >> trigger_relearn_model_dag