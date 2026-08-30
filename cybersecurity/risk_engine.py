def calculate_risk(data):
    """
    Calculate laboratory safety risk from sensor readings.

    Monitored parameters:
        - Temperature
        - AQI (Air Quality Index)
        - Vibration

    Returns:
        risk_score: 0-100
        risk_level: LOW / MEDIUM / HIGH
        reasons: detected abnormal conditions
    """

    risk_score = 0
    reasons = []

    temperature = data.get("temperature", 0)
    aqi = data.get("aqi", 0)
    vibration = data.get("vibration", 0)

    # ---------------------------------------------------------
    # TEMPERATURE
    # ---------------------------------------------------------

    if temperature > 80:
        risk_score += 35
        reasons.append("Critically high temperature")

    elif temperature > 60:
        risk_score += 20
        reasons.append("High temperature")

    # ---------------------------------------------------------
    # AIR QUALITY INDEX (AQI)
    # ---------------------------------------------------------

    if aqi > 300:
        risk_score += 30
        reasons.append("Hazardous air quality")

    elif aqi > 200:
        risk_score += 25
        reasons.append("Very unhealthy air quality")

    elif aqi > 150:
        risk_score += 20
        reasons.append("Unhealthy air quality")

    elif aqi > 100:
        risk_score += 10
        reasons.append("Poor air quality")

    # ---------------------------------------------------------
    # VIBRATION
    # ---------------------------------------------------------

    if vibration > 3.0:
        risk_score += 20
        reasons.append("Abnormally high vibration")

    elif vibration > 1.5:
        risk_score += 10
        reasons.append("High vibration")

    # Keep score within 0-100
    risk_score = min(risk_score, 100)

    # ---------------------------------------------------------
    # RISK LEVEL
    # ---------------------------------------------------------

    if risk_score >= 60:
        risk_level = "HIGH"

    elif risk_score >= 30:
        risk_level = "MEDIUM"

    else:
        risk_level = "LOW"

    # ---------------------------------------------------------
    # NORMAL CASE
    # ---------------------------------------------------------

    if not reasons:
        reasons.append(
            "All monitored parameters are within normal range"
        )

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "reasons": reasons
    }