
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Safe Lab Sentinel",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ Safe Lab Sentinel")
st.subheader("Intelligent Laboratory Monitoring System")
st.sidebar.title("🎛️ Control Panel")

mode = st.sidebar.radio(
    "Simulation Mode",
    ["Normal", "Hazard", "Cyber Attack"]
)

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.metric("Device Status", "🟢 ONLINE")

with col2:
    st.metric("System Risk", "🟢 NORMAL")

st.set_page_config(
    page_title="Safe Lab Sentinel",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ Safe Lab Sentinel")
st.subheader("Intelligent Laboratory Monitoring System")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.metric("Device Status", "🟢 ONLINE")

with col2:
    if mode == "Normal":
        risk = "🟢 NORMAL"

    elif mode == "Hazard":
        risk = "🔴 CRITICAL"

    elif mode == "Cyber Attack":
        risk = "🚨 SECURITY ALERT"
with col2:
    st.metric("System Risk", risk)
st.divider()

st.subheader("📡 Live Sensor Readings")

col1, col2, col3 = st.columns(3)

if mode == "Normal":
    temperature = 27.4
    gas = 142
    vibration = 0.21

elif mode == "Hazard":
    temperature = 75.0
    gas = 950
    vibration = 8.5

elif mode == "Cyber Attack":
    temperature = 27.4
    gas = 142
    vibration = 0.21
with col1:
    st.metric("🌡️ Temperature", f"{temperature} °C")

with col2:
    st.metric("💨 Gas Level", gas)

with col3:
    st.metric("📳 Vibration", vibration)
st.divider()

st.subheader("📈 Sensor History")

data = pd.DataFrame({
    "Temperature": [27.0, 27.3, 27.1, 27.5, 27.8, 28.0, 27.6],
    "Gas Level": [140, 142, 145, 143, 150, 148, 146],
    "Vibration": [0.18, 0.21, 0.20, 0.22, 0.19, 0.25, 0.21]
})

st.line_chart(data)
st.divider()

st.subheader("🤖 AI Monitoring")

col1, col2 = st.columns(2)

with col1:
    st.success("🟢 SYSTEM NORMAL")

with col2:
    st.info("AI anomaly detection is active.")
st.divider()

st.subheader("🔐 Cybersecurity Status")

col1, col2 = st.columns(2)

with col1:
    st.success("🟢 DEVICE VERIFIED")

with col2:
    st.info("HMAC integrity verification active")
st.divider()

st.subheader("📋 Recent Events")

events = pd.DataFrame({
    "Time": ["14:20", "14:18", "14:15"],
    "Event": [
        "Sensor data received",
        "Device authenticated",
        "System check completed"
    ],
    "Status": [
        "🟢 Normal",
        "🟢 Verified",
        "🟢 Passed"
    ]
})

st.dataframe(events, use_container_width=True)
