import sys
sys.path.append("/mnt/d/Data Engineering Prep/Python/nyc_data_project/src")

from pipeline_runner import run_pipeline # type: ignore
from airflow import DAG # type: ignore
from airflow.operators.python import PythonOperator # type: ignore
from datetime import datetime, timedelta
import os

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

dag = DAG(
    'nyc_restaurant_pipeline',
    default_args=default_args,
    description='ETL pipeline for NYC restaurant inspections',
    schedule_interval='@daily',
    start_date=datetime(2025, 4, 7),
    catchup=False,
    tags=['nyc', 'restaurant', 'etl'],
)

def run_etl_pipeline():
    run_pipeline()

run_pipeline_task = PythonOperator(
    task_id='run_pipeline',
    python_callable=run_etl_pipeline,
    dag=dag,
)

run_pipeline_task
