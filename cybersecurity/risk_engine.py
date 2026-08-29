def calculate_risk(data):
    risk_score = 0
    reasons = []

    temperature = data.get("temperature", 0)
    humidity = data.get("humidity", 0)

    if temperature > 80:
        risk_score += 60
        reasons.append("Abnormally high temperature")

    elif temperature > 60:
        risk_score += 30
        reasons.append("High temperature")

    if humidity > 90:
        risk_score += 20
        reasons.append("Abnormally high humidity")

    if risk_score >= 60:
        level = "HIGH"

    elif risk_score >= 30:
        level = "MEDIUM"

    else:
        level = "LOW"

    return {
        "risk_score": risk_score,
        "risk_level": level,
        "reasons": reasons
    }