from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib

from pathlib import Path


# ============================================================
# CREATE FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="SafeLab Sentinel AI Backend",
    description="AI-based anomaly detection system",
    version="1.0"
)


# ============================================================
# LOAD TRAINED MACHINE-LEARNING MODEL
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

model = joblib.load(
    BASE_DIR / "model" / "anomaly_model.pkl"
)


# ============================================================
# SENSOR DATA MODEL
# ============================================================

class SensorData(BaseModel):

    device_id: str
    timestamp: str

    temperature: float
    aqi: float
    vibration: float


# ============================================================
# HOME / HEALTH CHECK
# ============================================================

@app.get("/")
def home():

    return {
        "status": "online",
        "message": "SafeLab Sentinel AI backend is running"
    }


# ============================================================
# AI PREDICTION
# ============================================================

@app.post("/predict")
def predict(data: SensorData):

    # --------------------------------------------------------
    # Convert received sensor data into a table
    # --------------------------------------------------------

    input_data = pd.DataFrame([{

        "temperature": data.temperature,
        "aqi": data.aqi,
        "vibration": data.vibration

    }])


    # --------------------------------------------------------
    # Ask the trained AI model to classify the reading
    # --------------------------------------------------------

    prediction = int(
        model.predict(input_data)[0]
    )


    # --------------------------------------------------------
    # Convert AI output into understandable result
    # --------------------------------------------------------

    if prediction == 1:

        status = "SUSPICIOUS"
        risk = "HIGH"
        risk_score = 90

    else:

        status = "NORMAL"
        risk = "LOW"
        risk_score = 10


    # --------------------------------------------------------
    # Return result
    # --------------------------------------------------------

    return {

        "device_id": data.device_id,
        "timestamp": data.timestamp,

        "status": status,
        "risk": risk,
        "risk_score": risk_score,

        "prediction": prediction

    }