import time
from datetime import datetime

from pipeline import run_pipeline


DEVICE_ID = "ESP32_01"


def generate_normal_reading():

    return {
        "device_id": DEVICE_ID,
        "timestamp": datetime.now().isoformat(),
        "temperature": 30,
        "aqi": 45,
        "vibration": 0.12
    }


def generate_hazard_reading():

    return {
        "device_id": DEVICE_ID,
        "timestamp": datetime.now().isoformat(),
        "temperature": 85,
        "aqi": 250,
        "vibration": 3.0
    }


def print_result(sensor_data, result):

    print("\n" + "=" * 60)

    print("SAFE LAB SENTINEL — SENSOR READING")

    print("=" * 60)

    print("\nSENSOR DATA")
    print("-" * 60)

    print("Device:", sensor_data["device_id"])
    print("Temperature:", sensor_data["temperature"], "°C")
    print("AQI:", sensor_data["aqi"])
    print("Vibration:", sensor_data["vibration"])

    print("\nSECURITY")
    print("-" * 60)

    print(
        "Device Verified:",
        result.get("device_verified")
    )

    print(
        "Signature Valid:",
        result.get("signature_valid")
    )

    print(
        "Security Status:",
        result.get("security_status")
    )

    print(
        "Security Risk:",
        result.get("security_risk")
    )

    print(
        "Security Score:",
        result.get("security_risk_score")
    )

    print("\nAI")
    print("-" * 60)

    print(
        "AI Status:",
        result.get("ai_status")
    )

    print(
        "AI Risk:",
        result.get("ai_risk")
    )

    print(
        "AI Score:",
        result.get("ai_risk_score")
    )

    print("\nFINAL DECISION")
    print("-" * 60)

    print(
        "Status:",
        result.get("final_status")
    )

    print(
        "Action:",
        result.get("action")
    )

    print("=" * 60)


def run_simulation():

    print("\n")
    print("=" * 60)
    print(" SAFE LAB SENTINEL SENSOR SIMULATOR")
    print("=" * 60)

    # --------------------------------------------------------
    # NORMAL
    # --------------------------------------------------------

    print("\nSending NORMAL reading...")

    normal_data = generate_normal_reading()

    normal_result = run_pipeline(
        normal_data
    )

    print_result(
        normal_data,
        normal_result
    )

    time.sleep(2)

    # --------------------------------------------------------
    # HAZARD
    # --------------------------------------------------------

    print("\nSending HAZARD reading...")

    hazard_data = generate_hazard_reading()

    hazard_result = run_pipeline(
        hazard_data
    )

    print_result(
        hazard_data,
        hazard_result
    )

    print("\n")
    print("=" * 60)
    print(" SIMULATION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":

    run_simulation()