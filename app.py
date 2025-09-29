from fastapi import FastAPI
from pydantic import BaseModel, Field
import joblib
import os

# load model once when app starts
MODEL_PATH = os.getenv("MODEL_PATH", "model.pkl")
model = joblib.load(MODEL_PATH)

app = FastAPI(title="Housing Price API", version="1.0")


class PredictRequest(BaseModel):
    area: float = Field(..., gt=0, description="House area in sq ft")


class PredictResponse(BaseModel):
    prediction: float


@app.get("/")
def root():
    return {"status": "ok", "message": "Use POST /predict with {area: <number>}"}


@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    pred = float(model.predict([[req.area]])[0])

    # simple log line for monitor demo
    os.makedirs("logs", exist_ok=True)
    with open("logs/inference.log", "a") as f:
        f.write(f"PRED,{req.area},{pred}\n")

    return PredictResponse(prediction=pred)
