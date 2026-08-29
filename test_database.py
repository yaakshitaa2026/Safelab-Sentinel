from database import initialize_database, save_event, get_recent_events


def test_database_save_and_retrieve():
    # Initialize the database
    initialize_database()

    # Sample sensor data
    sensor_data = {
        "device_id": "ESP32_TEST",
        "timestamp": "2026-08-30T00:30:00",
        "temperature": 30,
        "humidity": 60,
        "voltage": 3.3,
        "current": 0.42,
        "vibration": 0.12
    }

    # Sample pipeline result
    pipeline_result = {
        "device_verified": True,
        "signature_valid": True,
        "security_status": "VERIFIED",
        "security_risk": "LOW",
        "security_risk_score": 0,
        "ai_status": "NORMAL",
        "ai_risk": "LOW",
        "ai_risk_score": 10,
        "ai_prediction": 0,
        "final_status": "NORMAL",
        "action": "MONITOR"
    }

    # Save the event
    save_event(
        sensor_data,
        pipeline_result
    )

    # Retrieve stored events
    events = get_recent_events()

    # Verify that events exist
    assert len(events) > 0

    # Verify the latest event
    latest_event = events[0]

    assert latest_event["device_id"] == "ESP32_TEST"
    assert latest_event["security_status"] == "VERIFIED"
    assert latest_event["final_status"] == "NORMAL"
    assert latest_event["action"] == "MONITOR"