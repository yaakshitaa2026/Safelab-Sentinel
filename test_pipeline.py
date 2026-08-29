from pipeline import run_pipeline


# ============================================================
# TEST 1 — NORMAL
# ============================================================

normal_data = {

    "device_id": "ESP32_01",

    "timestamp": "2026-08-29T23:00:00",

    "temperature": 30,

    "humidity": 60,

    "voltage": 3.3,

    "current": 0.42,

    "vibration": 0.12
}


print("\n" + "=" * 60)
print("TEST 1 — NORMAL")
print("=" * 60)

result = run_pipeline(normal_data)

print(result)


# ============================================================
# TEST 2 — HAZARD
# ============================================================

hazard_data = {

    "device_id": "ESP32_01",

    "timestamp": "2026-08-29T23:05:00",

    "temperature": 85,

    "humidity": 92,

    "voltage": 4.3,

    "current": 2.0,

    "vibration": 3.0
}


print("\n" + "=" * 60)
print("TEST 2 — HAZARD")
print("=" * 60)

result = run_pipeline(hazard_data)

print(result)


# ============================================================
# TEST 3 — UNKNOWN DEVICE
# ============================================================

unknown_device_data = {

    "device_id": "UNKNOWN_DEVICE",

    "timestamp": "2026-08-29T23:10:00",

    "temperature": 30,

    "humidity": 60,

    "voltage": 3.3,

    "current": 0.42,

    "vibration": 0.12
}


print("\n" + "=" * 60)
print("TEST 3 — UNKNOWN DEVICE")
print("=" * 60)

result = run_pipeline(
    unknown_device_data
)

print(result)


# ============================================================
# TEST 4 — TAMPERED DATA
# ============================================================

tamper_data = {

    "device_id": "ESP32_01",

    "timestamp": "2026-08-29T23:15:00",

    "temperature": 30,

    "humidity": 60,

    "voltage": 3.3,

    "current": 0.42,

    "vibration": 0.12
}


print("\n" + "=" * 60)
print("TEST 4 — TAMPERED DATA")
print("=" * 60)

result = run_pipeline(
    tamper_data,
    tamper=True
)

print(result)
