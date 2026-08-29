import requests

from cybersecurity.security_pipeline import process_message
from cybersecurity.devices import get_device_secret
from cybersecurity.security import generate_signature


AI_API_URL = "http://127.0.0.1:8000/predict"


def run_pipeline(sensor_data, tamper=False):
    """
    Complete SafeLab Sentinel processing pipeline.

    Flow:

    Sensor data
        ↓
    Device verification
        ↓
    HMAC verification
        ↓
    Cybersecurity risk analysis
        ↓
    AI anomaly detection
        ↓
    Final decision
    """

    device_id = sensor_data.get("device_id")

    # ========================================================
    # 1. GET DEVICE SECRET
    # ========================================================

    secret = get_device_secret(device_id)

    if secret is None:
        return {
            "accepted": False,
            "device_verified": False,
            "signature_valid": False,
            "ai_status": "NOT_RUN",
            "security_status": "REJECTED",
            "security_risk": "HIGH",
            "security_risk_score": 100,
            "ai_risk": "UNKNOWN",
            "ai_risk_score": 0,
            "final_status": "CRITICAL",
            "action": "BLOCK",
            "reasons": [
                "Unknown or unauthorized device"
            ]
        }

    # ========================================================
    # 2. GENERATE HMAC SIGNATURE
    # ========================================================

    signature = generate_signature(
        sensor_data,
        secret
    )

    # ========================================================
    # 3. OPTIONAL TAMPER SIMULATION
    # ========================================================

    if tamper:
        sensor_data = sensor_data.copy()

        sensor_data["temperature"] = (
            sensor_data["temperature"] + 50
        )

    # ========================================================
    # 4. CYBERSECURITY PIPELINE
    # ========================================================

    security_result = process_message(
        sensor_data,
        signature
    )

    # ========================================================
    # 5. SECURITY REJECTED
    # ========================================================

    if not security_result["accepted"]:

        reason = security_result.get(
            "reason",
            "Security verification failed"
        )

        return {
            "accepted": False,
            "device_verified": (
                reason != "Unknown device"
            ),
            "signature_valid": False,
            "ai_status": "NOT_RUN",
            "security_status": "REJECTED",
            "security_risk": "HIGH",
            "security_risk_score": 100,
            "ai_risk": "UNKNOWN",
            "ai_risk_score": 0,
            "final_status": "CRITICAL",
            "action": "BLOCK",
            "reasons": [reason]
        }

    # ========================================================
    # 6. EXTRACT SECURITY RESULT
    # ========================================================

    security_risk = security_result["risk"]

    security_level = security_risk["risk_level"]
    security_score = security_risk["risk_score"]
    security_reasons = security_risk["reasons"]

    # ========================================================
    # 7. SEND VERIFIED DATA TO AI
    # ========================================================

    try:

        response = requests.post(
            AI_API_URL,
            json=sensor_data,
            timeout=5
        )

        response.raise_for_status()

        ai_result = response.json()

    except requests.RequestException as error:

        return {
            "accepted": True,
            "device_verified": True,
            "signature_valid": True,
            "ai_status": "OFFLINE",
            "security_status": "VERIFIED",
            "security_risk": security_level,
            "security_risk_score": security_score,
            "ai_risk": "UNKNOWN",
            "ai_risk_score": 0,
            "final_status": "WARNING",
            "action": "MONITOR",
            "reasons": security_reasons,
            "error": str(error)
        }

    # ========================================================
    # 8. EXTRACT AI RESULT
    # ========================================================

    ai_prediction = ai_result.get(
        "prediction",
        0
    )

    ai_risk = ai_result.get(
        "risk",
        "UNKNOWN"
    )

    ai_risk_score = ai_result.get(
        "risk_score",
        0
    )

    # ========================================================
    # 9. FINAL DECISION
    # ========================================================

    if (
        security_level == "HIGH"
        or ai_prediction == 1
    ):

        final_status = "CRITICAL"
        action = "ALERT"

    elif security_level == "MEDIUM":

        final_status = "WARNING"
        action = "INVESTIGATE"

    else:

        final_status = "NORMAL"
        action = "MONITOR"

    # ========================================================
    # 10. RETURN COMPLETE RESULT
    # ========================================================

    return {
        "accepted": True,
        "device_verified": True,
        "signature_valid": True,
        "security_status": "VERIFIED",
        "security_risk": security_level,
        "security_risk_score": security_score,
        "security_reasons": security_reasons,
        "ai_status": ai_result.get(
            "status",
            "UNKNOWN"
        ),
        "ai_risk": ai_risk,
        "ai_risk_score": ai_risk_score,
        "ai_prediction": ai_prediction,
        "final_status": final_status,
        "action": action
    }
    