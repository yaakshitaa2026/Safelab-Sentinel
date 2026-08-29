from database import initialize_database, save_event, get_recent_events


initialize_database()


sensor_data = {
    "device_id": "ESP32_01",
    "timestamp": "2026-08-30T00:30:00",
    "temperature": 30,
    "humidity": 60,
    "voltage": 3.3,
    "current": 0.42,
    "vibration": 0.12
}


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


save_event(sensor_data, pipeline_result)


events = get_recent_events()


print("\n" + "=" * 60)
print("DATABASE TEST")
print("=" * 60)

print("\nNumber of stored events:", len(events))

print("\nLatest event:")
print(events[0])

print("\n" + "=" * 60)
print("DATABASE TEST COMPLETE")
print("=" * 60)