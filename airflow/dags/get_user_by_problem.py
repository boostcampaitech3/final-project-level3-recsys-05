from airflow.models import DAG, Variable
from airflow.providers.http.sensors.http import HttpSensor
from airflow.contrib.operators.ssh_operator import SSHOperator
from airflow.contrib.sensors.sftp_sensor import SFTPSensor
from airflow.providers.slack.operators.slack_webhook import SlackWebhookOperator

from datetime import datetime, timedelta

from fake_useragent import UserAgent

default_args = {
    "owner": "airflow",
    "email_on_failure": True,
    "email_on_retry": False,
    "email": "kgw7401@gmail.com",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "depends_on_past": False
}

def get_message() -> str:
    return "User By Problem Data Upload Success!"


with DAG("get_user_by_problem", start_date=datetime(2022, 5, 31), 
    schedule_interval=timedelta(minutes=0, hours=2, days=3), default_args=default_args, catchup=False) as dag:

    is_boj_score_available = HttpSensor(
        task_id="is_boj_score_available",
        http_conn_id="is_boj_score_available_id",
        endpoint="status",
        headers={"User-agent": UserAgent().random},
        response_check=lambda response: response.status_code == 200,
        poke_interval=5,
        timeout=20,
        queue="master_node"
    )

    send_slack_notification = SlackWebhookOperator(
        task_id="send_slack_notification",
        http_conn_id="slack_conn_id",
        message=get_message(),
        channel="#level2-recsys-05-알잘딱깔센-캠퍼만",
        queue="master_node"
    )

    worker_node_nums = Variable.get("worker_node_nums")

    for node in range(1, int(worker_node_nums)+1):
        trigger_get_data = SSHOperator(
            task_id=f"trigger_get_data_{node}",
            ssh_conn_id=f"ssh_id_{node}",
            command="nohup python3 /opt/ml/scraping_code/get_user_by_problem.py & sleep 5",
            get_pty=True,
            queue=f"worker_{node}"
        )

        check_user_by_problem_exists = SFTPSensor(
            task_id=f"check_user_by_problem_exists_{node}",
            sftp_conn_id=f"ssh_id_{node}",
            path=f"/opt/ml/data/score/user_by_problem_*.csv",
            poke_interval=60,
            timeout=2000,
            queue=f"worker_{node}"
        )

        is_boj_score_available >> trigger_get_data >> check_user_by_problem_exists >> send_slack_notification