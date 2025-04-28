from fastapi import FastAPI
import tritonclient.grpc
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

# Instrumentator로 모든 엔드포인트 자동 모니터링
Instrumentator().instrument(app).expose(app)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/predict/")
def predict(data: dict):
    # Triton 서버에 예측 요청
    response = triton_infer(data)
    return response
