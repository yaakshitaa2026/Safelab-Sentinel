from cybersecurity.risk_engine import calculate_risk


def test_normal_case():
    data = {
        "temperature": 30,
        "humidity": 60,
        "voltage": 3.3,
        "current": 0.42,
        "vibration": 0.12
    }

    result = calculate_risk(data)

    assert result["risk_score"] == 0
    assert result["risk_level"] == "LOW"
    assert result["reasons"] == [
        "All monitored parameters are within normal range"
    ]


def test_hazard_case():
    data = {
        "temperature": 85,
        "humidity": 92,
        "voltage": 4.3,
        "current": 2.0,
        "vibration": 3.0
    }

    result = calculate_risk(data)

    assert result["risk_score"] == 95
    assert result["risk_level"] == "HIGH"

    assert "Critically high temperature" in result["reasons"]
    assert "Abnormally high humidity" in result["reasons"]
    assert "Abnormally high voltage" in result["reasons"]