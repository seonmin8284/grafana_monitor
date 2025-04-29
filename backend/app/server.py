from fastapi import FastAPI
import tritonclient.grpc
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import start_http_server, Gauge, Counter
import random

app = FastAPI()

# Instrumentator로 모든 엔드포인트 자동 모니터링
Instrumentator().instrument(app).expose(app)

# 커스텀 메트릭 정의
fraud_model_precision = Gauge('fraud_model_precision', 'Precision of fraud detection model')
fraud_model_recall = Gauge('fraud_model_recall', 'Recall of fraud detection model')
fraud_model_accuracy = Gauge('fraud_model_accuracy', 'Accuracy of fraud detection model')
fraud_model_feature_drift = Gauge('fraud_model_feature_drift', 'Feature drift score (e.g., population stability index)')
fraud_transactions_total = Counter('fraud_transactions_total', 'Total number of processed transactions')


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/predict/")
def predict(data: dict):
    # Triton 서버에 예측 요청
    response = triton_infer(data)
    return response

@app.get("/update_metrics")
def update_metrics():
    # 여기는 예시 - 실제 값은 모델 결과 기반으로
    fraud_model_precision.set(round(random.uniform(0.8, 0.95), 3))
    fraud_model_recall.set(round(random.uniform(0.7, 0.9), 3))
    fraud_model_accuracy.set(round(random.uniform(0.85, 0.98), 3))
    fraud_model_feature_drift.set(round(random.uniform(0.01, 0.15), 3))  # PSI 기준
    fraud_transactions_total.inc()  # 거래 수는 누적 증가

    return {"status": "metrics updated"}

# Prometheus용 HTTP 서버 실행 (exposed at :9101)
import threading
threading.Thread(target=lambda: start_http_server(9101)).start()