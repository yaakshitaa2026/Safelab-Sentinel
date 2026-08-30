import requests


API_URL = "http://127.0.0.1:8000/predict"


def test_ai_prediction_api():

    sensor_data = {
        "device_id": "ESP32_01",
        "timestamp": "2026-08-30T13:00:00",
        "temperature": 85,
        "aqi": 250,
        "vibration": 3.0
    }

    response = requests.post(
        API_URL,
        json=sensor_data,
        timeout=5
    )

    assert response.status_code == 200

    result = response.json()

    assert "prediction" in result
    assert "risk" in result
    assert "risk_score" in result