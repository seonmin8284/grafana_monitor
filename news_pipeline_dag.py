from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG('news_pipeline_dag',
         start_date=datetime(2024, 1, 1),
         schedule='@hourly',
         catchup=False) as dag:

    kafka_task = BashOperator(
        task_id='start_kafka_producer',
        bash_command='python3 /Users/l-20190029/Downloads/kafka/kafka_news_producer.py'
    )

    spark_task = BashOperator(
        task_id='start_spark_streaming',
        bash_command='spark-submit /Users/l-20190029/Downloads/kafka/news_stream_processor.py'
    )

    kafka_task >> spark_task
    