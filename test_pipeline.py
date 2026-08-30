from pipeline import run_pipeline


def test_normal_pipeline():

    normal_data = {
        "device_id": "ESP32_01",
        "timestamp": "2026-08-30T13:00:00",
        "temperature": 30,
        "aqi": 45,
        "vibration": 0.12
    }

    result = run_pipeline(
        normal_data
    )

    assert result["accepted"] is True
    assert result["device_verified"] is True
    assert result["signature_valid"] is True
    assert result["security_status"] == "VERIFIED"
    assert result["security_risk"] == "LOW"


def test_hazard_pipeline():

    hazard_data = {
        "device_id": "ESP32_01",
        "timestamp": "2026-08-30T13:05:00",
        "temperature": 85,
        "aqi": 250,
        "vibration": 3.0
    }

    result = run_pipeline(
        hazard_data
    )

    assert result["accepted"] is True
    assert result["device_verified"] is True
    assert result["signature_valid"] is True
    assert result["security_risk"] == "HIGH"
    assert result["security_risk_score"] > 0


def test_unknown_device_pipeline():

    unknown_device_data = {
        "device_id": "UNKNOWN_DEVICE",
        "timestamp": "2026-08-30T13:10:00",
        "temperature": 30,
        "aqi": 45,
        "vibration": 0.12
    }

    result = run_pipeline(
        unknown_device_data
    )

    assert result["accepted"] is False
    assert result["device_verified"] is False
    assert result["security_status"] == "REJECTED"
    assert result["security_risk"] == "HIGH"
    assert result["final_status"] == "CRITICAL"
    assert result["action"] == "BLOCK"
    assert result["ai_status"] == "NOT_RUN"


def test_tampered_data_pipeline():

    tamper_data = {
        "device_id": "ESP32_01",
        "timestamp": "2026-08-30T13:15:00",
        "temperature": 30,
        "aqi": 45,
        "vibration": 0.12
    }

    result = run_pipeline(
        tamper_data,
        tamper=True
    )

    assert result["accepted"] is False
    assert result["signature_valid"] is False
    assert result["security_status"] == "REJECTED"
    assert result["security_risk"] == "HIGH"
    assert result["final_status"] == "CRITICAL"
    assert result["action"] == "BLOCK"