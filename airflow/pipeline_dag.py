from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG('pipeline_dag',
         start_date=datetime(2024, 1, 1),
         schedule='@hourly',
         catchup=False) as dag:

    kafka_task = BashOperator(
        task_id='start_kafka_producer',
        bash_command='python3 kafka\kafka_producer.py'
    )

    spark_task = BashOperator(
        task_id='start_spark_streaming',
        bash_command='spark-submit spark\stream_processor.py'
    )

    kafka_task >> spark_task
    