import requests


API_URL = "http://127.0.0.1:8000/predict"


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
    json=sensor_data
)


print("Status code:", response.status_code)

print("AI response:")

print(response.json())