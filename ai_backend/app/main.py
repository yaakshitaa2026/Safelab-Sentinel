from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib


# Create the FastAPI application
app = FastAPI(
    title="SafeLab Sentinel AI Backend",
    description="AI-based anomaly detection system",
    version="1.0"
)


# Load the trained machine-learning model
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

model = joblib.load(
    BASE_DIR / "model" / "anomaly_model.pkl"
)


# Define the sensor data that our API expects
class SensorData(BaseModel):

    device_id: str
    timestamp: str

    temperature: float
    humidity: float
    voltage: float
    current: float
    vibration: float


# --------------------------------------------------
# HOME / HEALTH CHECK
# --------------------------------------------------

@app.get("/")
def home():

    return {
        "status": "online",
        "message": "SafeLab Sentinel AI backend is running"
    }


# --------------------------------------------------
# AI PREDICTION
# --------------------------------------------------

@app.post("/predict")
def predict(data: SensorData):

    # Convert received sensor data into a table
    input_data = pd.DataFrame([{

        "temperature": data.temperature,
        "humidity": data.humidity,
        "voltage": data.voltage,
        "current": data.current,
        "vibration": data.vibration

    }])


    # Ask the trained AI model to classify the reading
    prediction = int(
        model.predict(input_data)[0]
    )


    # Convert the AI's 0/1 output into something understandable
    if prediction == 1:

        status = "SUSPICIOUS"
        risk = "HIGH"
        risk_score = 90

    else:

        status = "NORMAL"
        risk = "LOW"
        risk_score = 10


    # Send the result back
    return {

        "device_id": data.device_id,
        "timestamp": data.timestamp,

        "status": status,
        "risk": risk,
        "risk_score": risk_score,

        "prediction": prediction

    }