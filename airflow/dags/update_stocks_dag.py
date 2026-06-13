from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="update_stock_prices",
    start_date=datetime(2026, 6, 11),
    schedule="0 16 * * *",   # 4:00 PM daily
    catchup=False,
) as dag:

    update_prices = BashOperator(
        task_id="update_prices",
        bash_command="""
        cd /opt/airflow/project &&
        python daily_update_all.py
        """
    )