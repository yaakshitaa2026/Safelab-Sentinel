from cybersecurity.devices import (
    verify_device,
    get_device_secret
)

from cybersecurity.security import (
    generate_signature,
    verify_signature
)


def test_authorized_device():
    device_id = "ESP32_01"

    result = verify_device(device_id)

    assert result is True


def test_unknown_device():
    device_id = "UNKNOWN_DEVICE"

    result = verify_device(device_id)

    assert result is False


def test_valid_hmac():
    sensor_data = {
        "device_id": "ESP32_01",
        "timestamp": "2026-08-29T23:00:00",
        "temperature": 30,
        "humidity": 60,
        "voltage": 3.3,
        "current": 0.42,
        "vibration": 0.12
    }

    secret = get_device_secret("ESP32_01")

    signature = generate_signature(
        sensor_data,
        secret
    )

    result = verify_signature(
        sensor_data,
        signature,
        secret
    )

    assert result is True


def test_tampered_data():
    sensor_data = {
        "device_id": "ESP32_01",
        "timestamp": "2026-08-29T23:00:00",
        "temperature": 30,
        "humidity": 60,
        "voltage": 3.3,
        "current": 0.42,
        "vibration": 0.12
    }

    secret = get_device_secret("ESP32_01")

    signature = generate_signature(
        sensor_data,
        secret
    )

    tampered_data = sensor_data.copy()
    tampered_data["temperature"] = 99

    result = verify_signature(
        tampered_data,
        signature,
        secret
    )

    assert result is False