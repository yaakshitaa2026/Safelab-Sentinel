from cybersecurity.risk_engine import calculate_risk


def test_case(name, data):
    print("\n" + "=" * 50)
    print(name)
    print("=" * 50)

    result = calculate_risk(data)

    print("Risk Score:", result["risk_score"])
    print("Risk Level:", result["risk_level"])

    print("Reasons:")

    for reason in result["reasons"]:
        print(" -", reason)


# ============================================================
# TEST 1 — NORMAL
# ============================================================

test_case(
    "TEST 1 — NORMAL",
    {
        "device_id": "ESP32_01",
        "timestamp": "2026-08-29T23:00:00",
        "temperature": 30,
        "humidity": 60,
        "voltage": 3.3,
        "current": 0.42,
        "vibration": 0.12
    }
)


# ============================================================
# TEST 2 — HAZARD
# ============================================================

test_case(
    "TEST 2 — HAZARD",
    {
        "device_id": "ESP32_01",
        "timestamp": "2026-08-29T23:05:00",
        "temperature": 85,
        "humidity": 92,
        "voltage": 4.3,
        "current": 2.0,
        "vibration": 3.0
    }
)


# ============================================================
# TEST 3 — VIBRATION
# ============================================================

test_case(
    "TEST 3 — VIBRATION",
    {
        "device_id": "ESP32_01",
        "timestamp": "2026-08-29T23:10:00",
        "temperature": 30,
        "humidity": 60,
        "voltage": 3.3,
        "current": 0.42,
        "vibration": 2.5
    }
)


# ============================================================
# TEST 4 — ELECTRICAL
# ============================================================

test_case(
    "TEST 4 — ELECTRICAL",
    {
        "device_id": "ESP32_01",
        "timestamp": "2026-08-29T23:15:00",
        "temperature": 30,
        "humidity": 60,
        "voltage": 4.5,
        "current": 1.5,
        "vibration": 0.12
    }
)