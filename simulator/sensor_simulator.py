import requests
import time
from datetime import datetime


# ============================================================
# SAFE LAB SENTINEL - SENSOR SIMULATOR
# ============================================================

# This is the address of Role 2's AI backend.
API_URL = "http://127.0.0.1:8000/predict"

# Name of our simulated device.
DEVICE_ID = "ESP32_01"


# ============================================================
# FUNCTION TO SEND SENSOR DATA TO THE AI
# ============================================================

def send_sensor_data(
    temperature,
    humidity,
    voltage,
    current,
    vibration
):

    # Create the sensor data packet.
    sensor_data = {

        "device_id": DEVICE_ID,

        "timestamp": datetime.now().isoformat(),

        "temperature": temperature,

        "humidity": humidity,

        "voltage": voltage,

        "current": current,

        "vibration": vibration
    }


    try:

        # Send the sensor data to Role 2's AI API.
        response = requests.post(
            API_URL,
            json=sensor_data,
            timeout=5
        )


        # Convert the response into Python data.
        result = response.json()


        print("\n----------------------------------------")

        print("SENSOR DATA")
        print("----------------------------------------")

        print("Device:", DEVICE_ID)
        print("Temperature:", temperature)
        print("Humidity:", humidity)
        print("Voltage:", voltage)
        print("Current:", current)
        print("Vibration:", vibration)


        print("\nAI RESULT")
        print("----------------------------------------")

        print("Status:", result["status"])
        print("Risk:", result["risk"])
        print("Risk Score:", result["risk_score"])
        print("Prediction:", result["prediction"])


        print("----------------------------------------")


    except requests.exceptions.RequestException as error:

        print("\nCould not connect to AI backend.")
        print("Error:", error)


# ============================================================
# NORMAL SENSOR READING
# ============================================================

def generate_normal_reading():

    return {

        "temperature": 30,

        "humidity": 60,

        "voltage": 3.3,

        "current": 0.42,

        "vibration": 0.12
    }


# ============================================================
# ANOMALOUS SENSOR READING
# ============================================================

def generate_anomaly_reading():

    return {

        "temperature": 85,

        "humidity": 92,

        "voltage": 4.3,

        "current": 2.0,

        "vibration": 3.0
    }


# ============================================================
# MAIN SIMULATION
# ============================================================

def main():

    print("========================================")
    print("     SAFE LAB SENTINEL SIMULATOR")
    print("========================================")

    print("Device:", DEVICE_ID)

    print("Connecting to AI backend...")
    print("API:", API_URL)


    # --------------------------------------------------------
    # NORMAL READING
    # --------------------------------------------------------

    print("\nSending NORMAL sensor reading...")

    normal = generate_normal_reading()

    send_sensor_data(
        normal["temperature"],
        normal["humidity"],
        normal["voltage"],
        normal["current"],
        normal["vibration"]
    )


    time.sleep(3)


    # --------------------------------------------------------
    # ANOMALOUS READING
    # --------------------------------------------------------

    print("\nSending ANOMALOUS sensor reading...")

    anomaly = generate_anomaly_reading()

    send_sensor_data(
        anomaly["temperature"],
        anomaly["humidity"],
        anomaly["voltage"],
        anomaly["current"],
        anomaly["vibration"]
    )


    print("\n========================================")
    print("Simulation completed.")
    print("========================================")


# ============================================================
# START PROGRAM
# ============================================================

if __name__ == "__main__":

    main()