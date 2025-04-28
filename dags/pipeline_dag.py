
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def retrain_model():
    # 모델 재학습 코드
    print("Relearning model...")

with DAG('model_training', start_date=datetime(2025, 4, 28), schedule_interval='@daily') as dag:
    retrain_task = PythonOperator(task_id='retrain_model', python_callable=retrain_model)
