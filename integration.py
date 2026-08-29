import requests


from cybersecurity.devices import (
    verify_device,
    get_device_secret
)

from cybersecurity.security import (
    generate_signature
)

from cybersecurity.risk_engine import (
    calculate_risk
)

from cybersecurity.security_pipeline import process_message


# ============================================================
# CONFIGURATION
# ============================================================

AI_API_URL = "http://127.0.0.1:8000/predict"

DEVICE_ID = "ESP32_01"

# IMPORTANT:
# This must match the secret registered for ESP001
DEVICE_SECRET = get_device_secret(DEVICE_ID)


# ============================================================
# SENSOR DATA
# ============================================================

sensor_data = {
    "device_id": DEVICE_ID,

    "timestamp": "2026-08-29T20:00:00",

    "temperature": 85,

    "humidity": 92,

    "voltage": 4.3,

    "current": 2.0,

    "vibration": 3.0
}


# ============================================================
# STEP 1 — DEVICE VERIFICATION
# ============================================================

print("========================================")
print("SAFE LAB SENTINEL - FULL PIPELINE")
print("========================================")

print("\n[1] VERIFYING DEVICE...")

if verify_device(DEVICE_ID):

    print("Device:", DEVICE_ID)
    print("Device authorized: YES")

else:

    print("Device authorized: NO")
    print("Stopping pipeline.")
    exit()


# ============================================================
# STEP 2 — CREATE HMAC SIGNATURE
# ============================================================

print("\n[2] CREATING SECURITY SIGNATURE...")

signature = generate_signature(
    sensor_data,
    DEVICE_SECRET
)

print("HMAC signature created.")


# ============================================================
# STEP 3 — SEND SENSOR DATA TO AI
# ============================================================

print("\n[3] SENDING DATA TO AI...")

try:

    response = requests.post(
        AI_API_URL,
        json=sensor_data,
        timeout=5
    )

    ai_result = response.json()

    print("AI response received.")

    print("\nAI STATUS:")
    print("Status:", ai_result.get("status"))
    print("Risk:", ai_result.get("risk"))
    print("Risk Score:", ai_result.get("risk_score"))
    print("Prediction:", ai_result.get("prediction"))

except requests.exceptions.RequestException as error:

    print("Could not connect to AI backend.")
    print("Error:", error)
    exit()


# ============================================================
# STEP 4 — CYBERSECURITY RISK ANALYSIS
# ============================================================

print("\n[4] CYBERSECURITY ANALYSIS...")

risk_result = calculate_risk(sensor_data)

print("Security Risk Score:", risk_result["risk_score"])

print("Security Risk Level:", risk_result["risk_level"])

print("Reasons:")

for reason in risk_result["reasons"]:

    print("-", reason)
# ============================================================
# STEP 5 — RUN FULL SECURITY PIPELINE
# ============================================================

print("\n[5] RUNNING FULL SECURITY PIPELINE...")

security_result = process_message(
    sensor_data,
    signature
)

print("\nSECURITY PIPELINE RESULT:")
print(security_result)


# ============================================================
# STEP 5 — FINAL DECISION
# ============================================================

print("\n========================================")
print("FINAL SYSTEM DECISION")
print("========================================")

if ai_result.get("prediction") == 1:

    print("AI DETECTION: SUSPICIOUS")

else:

    print("AI DETECTION: NORMAL")


if risk_result["risk_level"] == "HIGH":

    print("SECURITY LEVEL: HIGH")

    print("ACTION: ALERT")

else:

    print("SECURITY LEVEL:", risk_result["risk_level"])

    print("ACTION: MONITOR")


print("\n========================================")
print("PIPELINE COMPLETE")
print("========================================")
