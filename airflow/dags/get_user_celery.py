from airflow.models import DAG, Variable
from airflow.providers.http.sensors.http import HttpSensor
from airflow.contrib.operators.ssh_operator import SSHOperator
from airflow.contrib.sensors.sftp_sensor import SFTPSensor
from airflow.providers.sftp.operators.sftp import SFTPOperator
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.providers.google.cloud.sensors.gcs import GCSObjectExistenceSensor
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.operators.bash import BashOperator
from airflow.providers.slack.operators.slack_webhook import SlackWebhookOperator

from datetime import datetime, timedelta

import os
import ast
import glob
import pandas as pd
import numpy as np
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

default_args = {
    "owner": "airflow",
    "email_on_failure": False,
    "email_on_retry": False,
    "email": "kgw7401@gmail.com",
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
    "provide_context": True
}

def _concat_file() -> pd.DataFrame:
    all_filenames = [i for i in glob.glob('/home/kgw7401/user/user_*.csv')]
    user = pd.concat([pd.read_csv(f) for f in all_filenames])
    return user

def _delete_and_rename(df) -> None:
    df.drop(['bio', 'badge', 'background', 'profileImageUrl', 'classDecoration', 'proUntil'], axis=1, inplace=True)
    df.rename(columns={
            "handle": "user_name",
            "solvedCount": "solved_count",
            "voteCount": "vote_count",
            "ratingByProblemsSum": "rating_by_problems_sum",
            "ratingByClass": "rating_by_class",
            "ratingBySolvedCount": "rating_by_solved_count",
            "ratingByVoteCount": "rating_by_vote_count",
            "rivalCount": "rival_count",
            "reverseRivalCount": "reverse_rival_count",
            "maxStreak": "max_streak"
        }, inplace=True)
    df.to_csv("/home/kgw7401/user/user.csv", index=False)

def process_user_data():
    user = _concat_file()
    _delete_and_rename(user)

def _get_user_problems(user_name, headers) -> list:    
    url = f"https://www.acmicpc.net/user/{user_name}"
    req = requests.get(url, headers=headers).text
    page_source = BeautifulSoup(req, "html.parser")
    try:
        problems = page_source.find('div', {'class':'problem-list'}).text.split()
        print(f"{user_name}'s extract complete!")
    except:
        print(f"{user_name}'s user error!")
        problems = []           

    return problems

def _str_to_list(df) -> pd.DataFrame:
    df['organizations'] = df.organizations.apply(lambda x: ast.literal_eval(x))
    df['problems'] = df.problems.apply(lambda x: ast.literal_eval(str(x)))
    return df

def add_problem_list_and_save() -> None:
    new_user = pd.read_csv("/home/kgw7401/user/user.csv")
    old_user = pd.read_csv("/home/kgw7401/user/old_user.csv")
    old_user = old_user.loc[:, ['user_name', 'solved_count', 'problems']]
    df_user = new_user.merge(old_user, on=['user_name', 'solved_count'], how='left')
    update_count = 0
    headers = {"User-agent": UserAgent().random}
    for index, row in df_user.iterrows():
        if row['problems'] is np.nan:
            df_user.at[index, 'problems'] = _get_user_problems(row['user_name'], headers)
            update_count += 1
    print(update_count)
    df_user = _str_to_list(df_user)
    df_user.to_csv("/home/kgw7401/user/new_user.csv", index=False)
    df_user.to_parquet('/home/kgw7401/user/new_user.parquet')


def get_message() -> str:
    return "User Data Upload Success!"

with DAG("get_user_celery", start_date=datetime(2022, 5, 31), 
    schedule_interval=timedelta(weeks=1), default_args=default_args, catchup=False) as dag:

    is_solved_ac_user_api_available = HttpSensor(
        task_id="is_solved_ac_user_api_available",
        http_conn_id="solved_ac_user_api_id",
        endpoint="ranking/tier",
        response_check=lambda response: response.status_code == 200,
        poke_interval=5,
        timeout=20
    )

    process_user_data = PythonOperator(
        task_id="process_user_data",
        python_callable=process_user_data
    )

    worker_node_nums = Variable.get("worker_node_nums")

    for node in range(1, int(worker_node_nums)+1):
        trigger_get_data = SSHOperator(
            task_id=f"trigger_get_data_{node}",
            ssh_conn_id=f"ssh_id_{node}",
            command="nohup python3 /opt/ml/scraping_code/get_user.py & sleep 5",
            get_pty=True,
            queue=f"worker_{node}"
        )

        check_user_exists = SFTPSensor(
            task_id=f"check_user_exists_{node}",
            sftp_conn_id=f"ssh_id_{node}",
            path=f"/opt/ml/data/user/user_{node}.csv",
            poke_interval=60,
            timeout=2000,
            queue=f"worker_{node}"
        )

        mv_user_file_to_master = SFTPOperator(
            task_id=f"mv_user_file_to_master_{node}",
            ssh_conn_id=f"ssh_id_{node}",
            local_filepath=f"/home/kgw7401/user/user_{node}.csv",
            remote_filepath=f"/opt/ml/data/user/user_{node}.csv",
            operation="get",
            queue=f"worker_{node}"
        )

        is_solved_ac_user_api_available >> trigger_get_data >> check_user_exists >> mv_user_file_to_master >> process_user_data


    add_problem_list_and_save = PythonOperator(
        task_id="add_problem_list_and_save",
        python_callable=add_problem_list_and_save,
        queue="master_node"
    )

    mv_user_local_to_gcs = LocalFilesystemToGCSOperator(
        task_id="mv_user_local_to_gcs",
        gcp_conn_id="google_cloud_conn_id",
        src=os.path.join(os.getcwd(), "user", "new_user.parquet"),
        dst="user/{{ ds }}-user.parquet",
        bucket="santa-boj-final",
        queue="master_node"
    )

    check_gcs_user_exists = GCSObjectExistenceSensor(
        task_id="check_gcs_user_exists",
        bucket="santa-boj-final",
        object="user/{{ ds }}-user.parquet",
        google_cloud_conn_id ="google_cloud_conn_id",
        queue="master_node"
    )

    mv_gcs_to_bq = GCSToBigQueryOperator(
        task_id="mv_gcs_to_bq",
        bucket="santa-boj-final",
        source_objects=['user/{{ ds }}-user.parquet'],
        source_format="PARQUET",
        destination_project_dataset_table="santa-boj.dataset.user",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        gcp_conn_id="google_cloud_conn_id",
        queue="master_node"
    )

    handle_local_user_data = BashOperator(
        task_id="handle_local_user_data",
        bash_command="""
            rm -rf /home/kgw7401/user/user*.csv /home/kgw7401/user/old_user.csv /home/kgw7401/user/new_user.parquet
            mv /home/kgw7401/user/new_user.csv /home/kgw7401/user/old_user.csv
            """,
        queue="master_node"
    )

    send_slack_notification = SlackWebhookOperator(
        task_id="send_slack_notification",
        http_conn_id="slack_conn_id",
        message=get_message(),
        channel="#level2-recsys-05-알잘딱깔센-캠퍼만",
        queue="master_node"
    )


    process_user_data >> add_problem_list_and_save >> mv_user_local_to_gcs >> check_gcs_user_exists
    check_gcs_user_exists >> mv_gcs_to_bq >> handle_local_user_data >> send_slack_notification