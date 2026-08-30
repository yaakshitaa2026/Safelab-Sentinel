from cybersecurity.risk_engine import calculate_risk


def test_normal_case():

    data = {
        "temperature": 30,
        "aqi": 45,
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
        "aqi": 250,
        "vibration": 3.0
    }

    result = calculate_risk(data)

    # Temperature = +35
    # AQI 250 = +25
    # Vibration 3.0 = +10
    # Total = 70

    assert result["risk_score"] == 70
    assert result["risk_level"] == "HIGH"

    assert "Critically high temperature" in result["reasons"]
    assert "Very unhealthy air quality" in result["reasons"]
    assert "High vibration" in result["reasons"]