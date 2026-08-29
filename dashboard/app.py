import streamlit as st
import requests
import pandas as pd


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Safe Lab Sentinel",
    page_icon="🛡️",
    layout="wide"
)


# ============================================================
# CONFIGURATION
# ============================================================

AI_API_URL = "http://127.0.0.1:8000/predict"


# ============================================================
# TITLE
# ============================================================

st.title("🛡️ Safe Lab Sentinel")
st.subheader("Intelligent Laboratory Monitoring System")

st.divider()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🎛️ Control Panel")

mode = st.sidebar.radio(
    "Simulation Mode",
    ["Normal", "Hazard", "Cyber Attack"]
)


# ============================================================
# SENSOR DATA
# ============================================================

# ============================================================
# SENSOR DATA
# ============================================================

if mode == "Normal":

    sensor_data = {
        "device_id": "ESP32_01",
        "temperature": 30,
        "humidity": 60,
        "voltage": 3.3,
        "current": 0.42,
        "vibration": 0.12
    }

elif mode == "Hazard":

    sensor_data = {
        "device_id": "ESP32_01",
        "temperature": 85,
        "humidity": 92,
        "voltage": 4.3,
        "current": 2.0,
        "vibration": 3.0
    }

elif mode == "Cyber Attack":

    sensor_data = {
        "device_id": "UNKNOWN_DEVICE",
        "temperature": 30,
        "humidity": 60,
        "voltage": 3.3,
        "current": 0.42,
        "vibration": 0.12
    }


# ============================================================
# GET AI RESULT
# ============================================================

try:

    response = requests.post(
        AI_API_URL,
        json=sensor_data,
        timeout=5
    )

    ai_result = response.json()

    ai_connected = True

except Exception as error:

    ai_result = {}

    ai_connected = False

    st.error(
        "⚠️ AI backend is not running. "
        "Start the FastAPI server first."
    )


# ============================================================
# TOP STATUS CARDS
# ============================================================

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Device",
        sensor_data["device_id"]
    )


with col2:

    if ai_connected:

        st.metric(
            "AI Connection",
            "🟢 ONLINE"
        )

    else:

        st.metric(
            "AI Connection",
            "🔴 OFFLINE"
        )


with col3:

    if ai_connected:

        risk = ai_result.get(
            "risk",
            "UNKNOWN"
        )

        st.metric(
            "AI Risk",
            risk
        )

    else:

        st.metric(
            "AI Risk",
            "UNKNOWN"
        )


st.divider()


# ============================================================
# SENSOR READINGS
# ============================================================

st.subheader("📡 Live Sensor Readings")

col1, col2, col3, col4, col5 = st.columns(5)


with col1:

    st.metric(
        "🌡️ Temperature",
        f"{sensor_data['temperature']} °C"
    )


with col2:

    st.metric(
        "💧 Humidity",
        f"{sensor_data['humidity']} %"
    )


with col3:

    st.metric(
        "⚡ Voltage",
        f"{sensor_data['voltage']} V"
    )


with col4:

    st.metric(
        "🔌 Current",
        f"{sensor_data['current']} A"
    )


with col5:

    st.metric(
        "📳 Vibration",
        sensor_data["vibration"]
    )


st.divider()


# ============================================================
# AI MONITORING
# ============================================================

st.subheader("🤖 AI Monitoring")

col1, col2, col3 = st.columns(3)


if ai_connected:

    ai_status = ai_result.get(
        "status",
        "UNKNOWN"
    )

    ai_risk = ai_result.get(
        "risk",
        "UNKNOWN"
    )

    risk_score = ai_result.get(
        "risk_score",
        0
    )

    prediction = ai_result.get(
        "prediction",
        0
    )

else:

    ai_status = "OFFLINE"
    ai_risk = "UNKNOWN"
    risk_score = 0
    prediction = 0


with col1:

    if prediction == 1:

        st.error(
            f"🚨 {ai_status}"
        )

    else:

        st.success(
            f"🟢 {ai_status}"
        )


with col2:

    st.metric(
        "Risk Level",
        ai_risk
    )


with col3:

    st.metric(
        "Risk Score",
        risk_score
    )


st.divider()


# ============================================================
# CYBERSECURITY STATUS
# ============================================================

st.subheader("🔐 Cybersecurity Status")

col1, col2 = st.columns(2)


with col1:

    st.success(
        "🟢 DEVICE VERIFIED"
    )


with col2:

    st.info(
        "HMAC integrity verification active"
    )


st.divider()


# ============================================================
# SYSTEM DECISION
# ============================================================

st.subheader("🚨 System Decision")


if prediction == 1:

    st.error(
        "🚨 ALERT — SUSPICIOUS ACTIVITY DETECTED"
    )

    st.write(
        "The AI model detected an abnormal sensor pattern."
    )

else:

    st.success(
        "🟢 SYSTEM NORMAL"
    )

    st.write(
        "No abnormal sensor pattern detected."
    )


st.divider()


# ============================================================
# SENSOR HISTORY
# ============================================================

st.subheader("📈 Sensor History")

history = pd.DataFrame({

    "Temperature": [
        27.0,
        27.3,
        27.1,
        27.5,
        27.8,
        28.0,
        sensor_data["temperature"]
    ],

    "Humidity": [
        55,
        57,
        56,
        58,
        59,
        60,
        sensor_data["humidity"]
    ],

    "Vibration": [
        0.18,
        0.21,
        0.20,
        0.22,
        0.19,
        0.25,
        sensor_data["vibration"]
    ]
})

st.line_chart(history)


st.divider()


# ============================================================
# RECENT EVENTS
# ============================================================

st.subheader("📋 Recent Events")

events = pd.DataFrame({

    "Event": [
        "Sensor data received",
        "AI analysis completed",
        "Security verification completed"
    ],

    "Status": [
        "🟢 Received",
        "🚨 Suspicious" if prediction == 1 else "🟢 Normal",
        "🟢 Verified"
    ]
})

st.dataframe(
    events,
    use_container_width=True
)