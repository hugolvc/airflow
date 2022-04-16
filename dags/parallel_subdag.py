from datetime import datetime
from airflow import DAG
from airflow.operators.subdag import SubDagOperator
from airflow.operators.bash import BashOperator
from subdags.subdag_parallel_dag import subdag_parallel_dag

default_args = {
    'start_date': datetime(2022, 1, 1)
}

with DAG(
    'parallel_subdag',
    schedule_interval='@daily',
    default_args=default_args,
    catchup=False) as dag:

    task_1 = BashOperator(
        task_id='task_1',
        bash_command='sleep 3'
    )

    processing = SubDagOperator(
        task_id='processing_tasks',
        subdag=subdag_parallel_dag(
            'parallel_subdag', 'processing_tasks', default_args)
    )

    task_4 = BashOperator(
        task_id='task_4',
        bash_command='sleep 3'
    )

    task_1 >> processing >> task_4
