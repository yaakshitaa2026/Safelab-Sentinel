import requests


API_URL = "http://127.0.0.1:8000/predict"


def test_ai_prediction_api():
    sensor_data = {
        "device_id": "ESP001",
        "timestamp": "2026-08-29T19:15:00",
        "temperature": 85,
        "humidity": 92,
        "voltage": 4.3,
        "current": 2.0,
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