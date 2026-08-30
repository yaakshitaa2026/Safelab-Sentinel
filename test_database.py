from database import (
    initialize_database,
    save_event,
    get_recent_events
)


def test_database_save_and_retrieve():

    # Initialize the database
    initialize_database()


    # ========================================================
    # SAMPLE SENSOR DATA
    # ========================================================

    sensor_data = {
        "device_id": "ESP32_TEST",
        "timestamp": "2026-08-30T13:30:00",
        "temperature": 30,
        "aqi": 45,
        "vibration": 0.12
    }


    # ========================================================
    # SAMPLE PIPELINE RESULT
    # ========================================================

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


    # ========================================================
    # SAVE EVENT
    # ========================================================

    save_event(
        sensor_data,
        pipeline_result
    )


    # ========================================================
    # RETRIEVE STORED EVENTS
    # ========================================================

    events = get_recent_events()


    # ========================================================
    # VERIFY EVENTS EXIST
    # ========================================================

    assert len(events) > 0


    # ========================================================
    # VERIFY LATEST EVENT
    # ========================================================

    latest_event = events[0]


    assert latest_event["device_id"] == "ESP32_TEST"

    assert latest_event["temperature"] == 30

    assert latest_event["aqi"] == 45

    assert latest_event["vibration"] == 0.12

    assert latest_event["security_status"] == "VERIFIED"

    assert latest_event["final_status"] == "NORMAL"

    assert latest_event["action"] == "MONITOR"