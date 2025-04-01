import os
import sys
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# check sync
from pipelines.fetch_raw_log_Mezmo_pipeline import fetch_raw_mezmo
from pipelines.process_check_existence_log import process_and_check_existence
from pipelines.upload_to_s3 import upload_to_s3

default_args = {
    'owner':  'Brian Nguyen',
    'start_date': datetime(2023, 10, 22),
}

dag = DAG(
    dag_id='mezmo_etl_pipeline',
    default_args = default_args,
    schedule_interval='@daily',
    catchup=False,
    tags = ['mezmo', 'etl'])

now = datetime.now()
unix_end = int(now.timestamp()*1000)
file_name = now.strftime("%Y%m%d")
unix_start = int((now-timedelta(days=1)).timestamp()*1000)

fetch_task = PythonOperator(
    task_id = 'fetch_mezmo_logs',
    python_callable = fetch_raw_mezmo,
    provide_context = True,
    params={
        'unix_start': unix_start,
        'unix_end': unix_end
    },
    dag = dag
)

process_task = PythonOperator(
    task_id = 'process_logs',
    python_callable= process_and_check_existence,
    provide_context=True,
    params={
        'file_name': f'mezmo_{file_name}'
    },
    dag = dag
)

upload_to_s3_task = PythonOperator(
    task_id = 'upload_to_s3',
    python_callable= upload_to_s3,
    provide_context=True,
    dag=dag
)
fetch_task >> process_task >> upload_to_s3_task