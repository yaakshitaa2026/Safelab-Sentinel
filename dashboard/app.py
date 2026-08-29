import streamlit as st
import sys
from pathlib import Path
import pandas as pd

# ============================================================
# PROJECT IMPORT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from pipeline import run_pipeline


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Safe Lab Sentinel",
    page_icon="🛡️",
    layout="wide"
)


# ============================================================
# TITLE
# ============================================================

st.title("🛡️ Safe Lab Sentinel")
st.subheader("Intelligent Laboratory Monitoring & Security System")

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
# SENSOR SIMULATION
# ============================================================

if mode == "Normal":

    sensor_data = {
        "device_id": "ESP32_01",
        "timestamp": "2026-08-30T00:00:00",
        "temperature": 30,
        "humidity": 60,
        "voltage": 3.3,
        "current": 0.42,
        "vibration": 0.12
    }


elif mode == "Hazard":

    sensor_data = {
        "device_id": "ESP32_01",
        "timestamp": "2026-08-30T00:05:00",
        "temperature": 85,
        "humidity": 92,
        "voltage": 4.3,
        "current": 2.0,
        "vibration": 3.0
    }


else:

    sensor_data = {
        "device_id": "UNKNOWN_DEVICE",
        "timestamp": "2026-08-30T00:10:00",
        "temperature": 30,
        "humidity": 60,
        "voltage": 3.3,
        "current": 0.42,
        "vibration": 0.12
    }


# ============================================================
# RUN COMPLETE PIPELINE
# ============================================================

pipeline_result = run_pipeline(sensor_data)


# ============================================================
# EXTRACT PIPELINE RESULTS
# ============================================================

device_id = sensor_data["device_id"]

device_verified = pipeline_result.get(
    "device_verified",
    False
)

signature_valid = pipeline_result.get(
    "signature_valid",
    False
)

security_status = pipeline_result.get(
    "security_status",
    "UNKNOWN"
)

security_risk = pipeline_result.get(
    "security_risk",
    "UNKNOWN"
)

security_score = pipeline_result.get(
    "security_risk_score",
    0
)

security_reasons = pipeline_result.get(
    "security_reasons",
    pipeline_result.get("reasons", [])
)

ai_status = pipeline_result.get(
    "ai_status",
    "UNKNOWN"
)

ai_risk = pipeline_result.get(
    "ai_risk",
    "UNKNOWN"
)

ai_score = pipeline_result.get(
    "ai_risk_score",
    0
)

ai_prediction = pipeline_result.get(
    "ai_prediction",
    0
)

final_status = pipeline_result.get(
    "final_status",
    "UNKNOWN"
)

action = pipeline_result.get(
    "action",
    "UNKNOWN"
)


# ============================================================
# SYSTEM OVERVIEW
# ============================================================

st.subheader("📊 System Overview")

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Device",
        device_id
    )


with col2:

    if device_verified:
        st.metric(
            "Device Security",
            "VERIFIED"
        )
    else:
        st.metric(
            "Device Security",
            "REJECTED"
        )


with col3:

    st.metric(
        "Security Risk",
        security_risk
    )


with col4:

    st.metric(
        "AI Risk",
        ai_risk
    )


st.divider()


# ============================================================
# LIVE SENSOR READINGS
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
# CYBERSECURITY MONITORING
# ============================================================

st.subheader("🔐 Cybersecurity Monitoring")

col1, col2, col3 = st.columns(3)


with col1:

    if device_verified:

        st.success("🟢 DEVICE VERIFIED")

    else:

        st.error("🔴 DEVICE REJECTED")


with col2:

    if signature_valid:

        st.success("🟢 HMAC SIGNATURE VALID")

    else:

        st.error("🔴 HMAC SIGNATURE INVALID")


with col3:

    st.metric(
        "Security Risk Score",
        security_score
    )


# ============================================================
# SECURITY STATUS DETAILS
# ============================================================

st.subheader("Security Status")

st.write(
    f"**Status:** {security_status}"
)

st.write(
    f"**Risk Level:** {security_risk}"
)


if security_reasons:

    st.write("**Security Reasons:**")

    for reason in security_reasons:

        st.warning(
            f"⚠️ {reason}"
        )

else:

    st.success(
        "🟢 No security abnormalities detected."
    )


st.divider()


# ============================================================
# AI MONITORING
# ============================================================

st.subheader("🤖 AI Monitoring")

col1, col2, col3 = st.columns(3)


with col1:

    if ai_prediction == 1:

        st.error(
            f"🚨 AI Status: {ai_status}"
        )

    elif ai_status == "NOT_RUN":

        st.warning(
            "⚠️ AI Analysis Not Run"
        )

    else:

        st.success(
            f"🟢 AI Status: {ai_status}"
        )


with col2:

    st.metric(
        "AI Risk Level",
        ai_risk
    )


with col3:

    st.metric(
        "AI Risk Score",
        ai_score
    )


st.write(
    f"**AI Prediction:** `{ai_prediction}`"
)


st.divider()


# ============================================================
# FINAL SYSTEM DECISION
# ============================================================

st.subheader("🚨 Final System Decision")


if final_status == "CRITICAL":

    st.error(
        "🚨 SYSTEM ALERT"
    )

elif final_status == "WARNING":

    st.warning(
        "⚠️ SYSTEM WARNING"
    )

elif final_status == "NORMAL":

    st.success(
        "🟢 SYSTEM NORMAL"
    )

else:

    st.info(
        f"ℹ️ SYSTEM STATUS: {final_status}"
    )


col1, col2 = st.columns(2)


with col1:

    st.metric(
        "Final Status",
        final_status
    )


with col2:

    st.metric(
        "Recommended Action",
        action
    )


# ============================================================
# DECISION EXPLANATION
# ============================================================

if action == "BLOCK":

    st.error(
        "⛔ The system blocked the data because the device "
        "or message failed security verification."
    )

elif action == "ALERT":

    st.error(
        "🚨 The system detected a critical condition "
        "requiring immediate attention."
    )

elif action == "INVESTIGATE":

    st.warning(
        "⚠️ The system detected a medium-risk condition "
        "that should be investigated."
    )

else:

    st.success(
        "✅ No critical abnormalities detected."
    )


st.divider()


# ============================================================
# SENSOR HISTORY
# ============================================================

st.subheader("📈 Sensor History")

history = pd.DataFrame({

    "Temperature (°C)": [
        27.0,
        27.3,
        27.1,
        27.5,
        27.8,
        28.0,
        sensor_data["temperature"]
    ],

    "Humidity (%)": [
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
        "Device verification",
        "HMAC integrity check",
        "Security risk analysis",
        "AI anomaly detection",
        "Final system decision"
    ],

    "Status": [

        "🟢 Received",

        "🟢 Verified"
        if device_verified
        else "🔴 Rejected",

        "🟢 Valid"
        if signature_valid
        else "🔴 Invalid",

        security_risk,

        ai_risk,

        final_status
    ]
})


st.dataframe(
    events,
    use_container_width=True,
    hide_index=True
)


st.divider()


# ============================================================
# PROPOSED HARDWARE EXTENSION
# ============================================================

st.subheader("🔌 Proposed Hardware Extension")

st.write(
    "The current SafeLab Sentinel prototype is software-based. "
    "The following diagram represents a possible future hardware "
    "implementation using sensors and a microcontroller."
)


circuit_path = Path(__file__).resolve().parent / "circuit.png"

if circuit_path.exists():

    st.image(
        str(circuit_path),
        caption="Proposed Arduino-based hardware extension",
        width="stretch"
    )

else:

    st.info(
        "Hardware extension diagram not found."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "SafeLab Sentinel — Intelligent Laboratory Monitoring & Security System"
)