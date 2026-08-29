def calculate_risk(data):
    """
    Calculate laboratory safety/security risk from sensor data.

    Returns:
        risk_score: 0-100
        risk_level: LOW / MEDIUM / HIGH
        reasons: list of detected issues
    """

    risk_score = 0
    reasons = []

    # ---------------------------------------------------------
    # SENSOR VALUES
    # ---------------------------------------------------------

    temperature = data.get("temperature", 0)
    humidity = data.get("humidity", 0)
    voltage = data.get("voltage", 0)
    current = data.get("current", 0)
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
    # HUMIDITY
    # ---------------------------------------------------------

    if humidity > 90:
        risk_score += 20
        reasons.append("Abnormally high humidity")

    elif humidity > 75:
        risk_score += 10
        reasons.append("High humidity")

    # ---------------------------------------------------------
    # VOLTAGE
    # ---------------------------------------------------------

    if voltage > 4.2:
        risk_score += 20
        reasons.append("Abnormally high voltage")

    elif voltage < 2.8 and voltage > 0:
        risk_score += 15
        reasons.append("Abnormally low voltage")

    # ---------------------------------------------------------
    # CURRENT
    # ---------------------------------------------------------

    if current > 2.0:
        risk_score += 20
        reasons.append("Abnormally high current")

    elif current > 1.0:
        risk_score += 10
        reasons.append("High current")

    # ---------------------------------------------------------
    # VIBRATION
    # ---------------------------------------------------------

    if vibration > 3.0:
        risk_score += 20
        reasons.append("Abnormally high vibration")

    elif vibration > 1.5:
        risk_score += 10
        reasons.append("High vibration")

    # ---------------------------------------------------------
    # LIMIT SCORE TO 100
    # ---------------------------------------------------------

    risk_score = min(risk_score, 100)

    # ---------------------------------------------------------
    # DETERMINE RISK LEVEL
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
        reasons.append("All monitored parameters are within normal range")

    # ---------------------------------------------------------
    # FINAL RESULT
    # ---------------------------------------------------------

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "reasons": reasons
    }