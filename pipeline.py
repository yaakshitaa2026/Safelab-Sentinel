import requests

from cybersecurity.security_pipeline import process_message
from cybersecurity.devices import get_device_secret
from cybersecurity.security import generate_signature


# ============================================================
# AI BACKEND
# ============================================================

AI_API_URL = "http://127.0.0.1:8000/predict"


# ============================================================
# SAFE VALUE HELPERS
# ============================================================

def clamp(value, minimum=0, maximum=100):
    """Keep a number between minimum and maximum."""
    try:
        value = float(value)
    except (TypeError, ValueError):
        value = minimum

    return max(minimum, min(maximum, value))


def safe_int(value, default=0):
    """Safely convert a value to integer."""
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def safe_text(value, default="UNKNOWN"):
    """Safely convert a value to text."""
    if value is None:
        return default

    return str(value)


# ============================================================
# SENSOR-BASED SAFETY ANALYSIS
# ============================================================

def calculate_sensor_risk(sensor_data):
    """
    Calculate laboratory/environmental risk directly
    from the sensor readings.

    Monitored parameters:
        Temperature : laboratory/equipment heat
        AQI         : air quality / possible smoke or fumes
        Vibration   : abnormal equipment movement
    """

    temperature = float(
        sensor_data.get("temperature", 0)
    )

    aqi = float(
        sensor_data.get("aqi", 0)
    )

    vibration = float(
        sensor_data.get("vibration", 0)
    )

    risk_score = 0
    reasons = []

    # --------------------------------------------------------
    # TEMPERATURE
    # --------------------------------------------------------

    if temperature >= 80:
        risk_score += 35
        reasons.append(
            "Critically high temperature"
        )

    elif temperature >= 60:
        risk_score += 20
        reasons.append(
            "Abnormally high temperature"
        )

    elif temperature >= 45:
        risk_score += 10
        reasons.append(
            "Elevated temperature"
        )


    # --------------------------------------------------------
    # AIR QUALITY INDEX (AQI)
    # --------------------------------------------------------

    if aqi > 300:
        risk_score += 30
        reasons.append(
            "Hazardous air quality"
        )

    elif aqi > 200:
        risk_score += 25
        reasons.append(
            "Very unhealthy air quality"
        )

    elif aqi > 150:
        risk_score += 20
        reasons.append(
            "Unhealthy air quality"
        )

    elif aqi > 100:
        risk_score += 10
        reasons.append(
            "Poor air quality"
        )


    # --------------------------------------------------------
    # VIBRATION
    # --------------------------------------------------------

    if vibration >= 2.5:
        risk_score += 20
        reasons.append(
            "Critically high vibration"
        )

    elif vibration >= 1.5:
        risk_score += 12
        reasons.append(
            "Abnormally high vibration"
        )

    elif vibration >= 0.8:
        risk_score += 5
        reasons.append(
            "Elevated vibration"
        )


    # --------------------------------------------------------
    # LIMIT SCORE
    # --------------------------------------------------------

    risk_score = int(
        clamp(risk_score)
    )


    # --------------------------------------------------------
    # RISK LEVEL
    # --------------------------------------------------------

    if risk_score >= 70:
        risk_level = "HIGH"

    elif risk_score >= 30:
        risk_level = "MEDIUM"

    else:
        risk_level = "LOW"


    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "reasons": reasons
    }


# ============================================================
# COMPLETE SAFELAB SENTINEL PIPELINE
# ============================================================

def run_pipeline(sensor_data, tamper=False):
    """
    Complete SafeLab Sentinel processing pipeline.

    Flow:

        SENSOR DATA
             ↓
        DEVICE AUTHENTICATION
             ↓
        HMAC INTEGRITY
             ↓
        CYBERSECURITY ANALYSIS
             ↓
        SENSOR SAFETY ANALYSIS
             ↓
        AI ANOMALY DETECTION
             ↓
        RISK ENGINE
             ↓
        FINAL DECISION
    """

    # ========================================================
    # 1. DEVICE ID
    # ========================================================

    device_id = sensor_data.get(
        "device_id",
        "UNKNOWN_DEVICE"
    )


    # ========================================================
    # 2. GET DEVICE SECRET
    # ========================================================

    secret = get_device_secret(device_id)


    # ========================================================
    # UNKNOWN DEVICE
    # ========================================================

    if secret is None:

        return {
            "accepted": False,

            "device_verified": False,

            "signature_valid": False,

            "ai_status": "NOT_RUN",

            "ai_prediction": 0,

            "security_status": "REJECTED",

            "security_risk": "HIGH",

            "security_risk_score": 100,

            "security_reasons": [
                "Unknown or unauthorized device"
            ],

            "ai_risk": "UNKNOWN",

            "ai_risk_score": 0,

            "final_status": "CRITICAL",

            "action": "BLOCK",

            "reasons": [
                "Unknown or unauthorized device"
            ]
        }


    # ========================================================
    # 3. GENERATE ORIGINAL HMAC SIGNATURE
    # ========================================================

    signature = generate_signature(
        sensor_data,
        secret
    )


    # ========================================================
    # 4. CYBER ATTACK / TAMPER SIMULATION
    # ========================================================

    data_to_verify = sensor_data.copy()


    if tamper:

        # Change the data AFTER the original signature
        # was generated.

        data_to_verify["temperature"] = (
            float(
                data_to_verify.get(
                    "temperature",
                    30
                )
            ) + 50
        )


    # ========================================================
    # 5. CYBERSECURITY PIPELINE
    # ========================================================

    try:

        security_result = process_message(
            data_to_verify,
            signature
        )

    except Exception as error:

        return {
            "accepted": False,

            "device_verified": True,

            "signature_valid": False,

            "ai_status": "NOT_RUN",

            "ai_prediction": 0,

            "security_status": "ERROR",

            "security_risk": "HIGH",

            "security_risk_score": 100,

            "security_reasons": [
                f"Security pipeline error: {error}"
            ],

            "ai_risk": "UNKNOWN",

            "ai_risk_score": 0,

            "final_status": "CRITICAL",

            "action": "BLOCK",

            "reasons": [
                f"Security pipeline error: {error}"
            ]
        }


    # ========================================================
    # 6. SECURITY ACCEPTANCE
    # ========================================================

    accepted = bool(
        security_result.get(
            "accepted",
            False
        )
    )


    # ========================================================
    # CYBER ATTACK DETECTED
    # ========================================================

    if not accepted:

        reason = safe_text(
            security_result.get(
                "reason",
                "Security verification failed"
            ),
            "Security verification failed"
        )

        return {
            "accepted": False,

            "device_verified": True,

            "signature_valid": False,

            "ai_status": "NOT_RUN",

            "ai_prediction": 0,

            "security_status": "REJECTED",

            "security_risk": "HIGH",

            "security_risk_score": 100,

            "security_reasons": [
                reason
            ],

            "ai_risk": "UNKNOWN",

            "ai_risk_score": 0,

            "final_status": "CRITICAL",

            "action": "BLOCK",

            "reasons": [
                reason
            ]
        }


    # ========================================================
    # 7. EXTRACT SECURITY RESULT
    # ========================================================

    raw_security_risk = security_result.get(
        "risk",
        {}
    )


    if isinstance(raw_security_risk, dict):

        security_level = safe_text(
            raw_security_risk.get(
                "risk_level",
                "LOW"
            ),
            "LOW"
        ).upper()

        security_score_from_module = safe_int(
            raw_security_risk.get(
                "risk_score",
                0
            )
        )

        security_reasons_from_module = (
            raw_security_risk.get(
                "reasons",
                []
            )
        )

    else:

        security_level = "LOW"

        security_score_from_module = 0

        security_reasons_from_module = []


    if not isinstance(
        security_reasons_from_module,
        list
    ):

        security_reasons_from_module = [
            str(security_reasons_from_module)
        ]


    # ========================================================
    # 8. SENSOR SAFETY ANALYSIS
    # ========================================================

    sensor_risk = calculate_sensor_risk(
        data_to_verify
    )


    sensor_score = sensor_risk[
        "risk_score"
    ]

    sensor_level = sensor_risk[
        "risk_level"
    ]

    sensor_reasons = sensor_risk[
        "reasons"
    ]


    # ========================================================
    # 9. COMBINE SECURITY + SENSOR RISK
    # ========================================================

    if security_level == "HIGH":

        security_score = max(
            70,
            security_score_from_module
        )

    elif security_level == "MEDIUM":

        security_score = max(
            30,
            security_score_from_module
        )

    else:

        security_score = min(
            29,
            max(
                0,
                security_score_from_module
            )
        )


    # --------------------------------------------------------
    # FINAL SECURITY SCORE
    # --------------------------------------------------------

    combined_security_score = max(
        security_score,
        sensor_score
    )


    combined_security_score = int(
        clamp(
            combined_security_score
        )
    )


    # --------------------------------------------------------
    # SECURITY LEVEL
    # --------------------------------------------------------

    if combined_security_score >= 70:

        combined_security_level = "HIGH"

    elif combined_security_score >= 30:

        combined_security_level = "MEDIUM"

    else:

        combined_security_level = "LOW"


    # ========================================================
    # 10. SEND VERIFIED DATA TO AI
    # ========================================================

    ai_result = {}

    ai_online = True


    try:

        response = requests.post(
            AI_API_URL,
            json=data_to_verify,
            timeout=5
        )

        response.raise_for_status()

        ai_result = response.json()


    except requests.RequestException:

        ai_online = False

        ai_result = {}


    except ValueError:

        ai_online = False

        ai_result = {}


    # ========================================================
    # 11. AI RESULT
    # ========================================================

    if ai_online:

        ai_prediction = safe_int(
            ai_result.get(
                "prediction",
                0
            )
        )

        ai_status = safe_text(
            ai_result.get(
                "status",
                "NORMAL"
            ),
            "NORMAL"
        ).upper()

        ai_risk = safe_text(
            ai_result.get(
                "risk",
                "LOW"
            ),
            "LOW"
        ).upper()

        ai_risk_score = int(
            clamp(
                ai_result.get(
                    "risk_score",
                    0
                )
            )
        )

    else:

        ai_prediction = 0

        ai_status = "OFFLINE"

        ai_risk = "UNKNOWN"

        ai_risk_score = 0


    # ========================================================
    # 12. IMPORTANT AI SAFETY CHECK
    # ========================================================

    telemetry_is_abnormal = (
        sensor_score >= 30
    )


    ai_anomaly = (
        ai_prediction == 1
        and telemetry_is_abnormal
    )


    # ========================================================
    # 13. FINAL RISK SCORE
    # ========================================================

    if ai_anomaly:

        overall_risk = max(
            combined_security_score,
            sensor_score,
            ai_risk_score
        )

    else:

        overall_risk = max(
            combined_security_score,
            sensor_score
        )


    overall_risk = int(
        clamp(
            overall_risk
        )
    )


    # ========================================================
    # 14. FINAL STATUS
    # ========================================================

    if overall_risk >= 70:

        final_status = "CRITICAL"

        action = "ALERT"


    elif overall_risk >= 30:

        final_status = "WARNING"

        action = "INVESTIGATE"


    else:

        final_status = "NORMAL"

        action = "MONITOR"


    # ========================================================
    # 15. FINAL REASONS
    # ========================================================

    final_reasons = []


    # Sensor reasons first
    final_reasons.extend(
        sensor_reasons
    )


    # Add security reasons only if meaningful
    if security_level in [
        "HIGH",
        "MEDIUM"
    ]:

        for reason in security_reasons_from_module:

            if reason not in final_reasons:

                final_reasons.append(
                    reason
                )


    # AI anomaly reason
    if ai_anomaly:

        ai_reason = (
            "AI detected abnormal sensor behaviour"
        )

        if ai_reason not in final_reasons:

            final_reasons.append(
                ai_reason
            )


    # ========================================================
    # 16. NORMAL STATE CLEANUP
    # ========================================================

    if final_status == "NORMAL":

        final_reasons = []

        combined_security_level = "LOW"

        combined_security_score = int(
            clamp(
                min(
                    overall_risk,
                    29
                )
            )
        )


    # ========================================================
    # 17. RETURN COMPLETE RESULT
    # ========================================================

    return {

        # ----------------------------------------------------
        # PIPELINE STATE
        # ----------------------------------------------------

        "accepted": True,

        "device_verified": True,

        "signature_valid": True,


        # ----------------------------------------------------
        # SECURITY
        # ----------------------------------------------------

        "security_status": "VERIFIED",

        "security_risk": combined_security_level,

        "security_risk_score": combined_security_score,

        "security_reasons": final_reasons,


        # ----------------------------------------------------
        # AI
        # ----------------------------------------------------

        "ai_status": ai_status,

        "ai_risk": ai_risk,

        "ai_risk_score": ai_risk_score,

        "ai_prediction": ai_prediction,


        # ----------------------------------------------------
        # FINAL DECISION
        # ----------------------------------------------------

        "final_status": final_status,

        "action": action,

        "reasons": final_reasons
    }