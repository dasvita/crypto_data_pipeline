from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {"start_date": datetime(2024, 2, 21), "catchup": False}
dag = DAG("crypto_etl", default_args=default_args, schedule_interval="*/5 * * * *")

etl_task = BashOperator(
    task_id="run_crypto_etl",
    bash_command="python3 /opt/airflow/scripts/crypto_etl.py",
    dag=dag
)
