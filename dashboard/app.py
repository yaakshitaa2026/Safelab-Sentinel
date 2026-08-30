import streamlit as st
import sys
from pathlib import Path
import pandas as pd
from textwrap import dedent
from html import escape


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="SafeLab Sentinel",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# HTML RENDER HELPER
# ============================================================

def render_html(content):
    html = dedent(content).strip()

    html = "\n".join(
        line.strip() for line in html.splitlines()
    )

    st.markdown(
        html,
        unsafe_allow_html=True,
    )


# ============================================================
# PROJECT PATH / IMPORTS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from pipeline import run_pipeline
from database import save_event, get_recent_events


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>

/* ============================================================
   HIDE STREAMLIT TOP HEADER
   ============================================================ */

header[data-testid="stHeader"] {
    display: none !important;
}

[data-testid="stToolbar"] {
    display: none !important;
}

[data-testid="stDecoration"] {
    display: none !important;
}


@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap');


/* ============================================================
   GLOBAL
   ============================================================ */

html,
body,
[class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at 90% 0%,
            rgba(0, 180, 255, 0.08),
            transparent 28%
        ),
        radial-gradient(
            circle at 10% 20%,
            rgba(0, 255, 180, 0.04),
            transparent 25%
        ),
        #050b12;
}

.block-container {
    max-width: 1400px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}


/* ============================================================
   SIDEBAR
   ============================================================ */

section[data-testid="stSidebar"] {
    background: #070f18 !important;
    border-right: 1px solid rgba(90, 210, 255, 0.12);
}

section[data-testid="stSidebar"] > div {
    background: #070f18 !important;
}

section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span {
    color: #e1edf4 !important;
}

.sidebar-title {
    color: #f4fbff;
    font-size: 22px;
    font-weight: 800;
    margin-bottom: 12px;
    letter-spacing: 0.3px;
}

.sidebar-description {
    color: #9db4c4;
    font-size: 13px;
    line-height: 1.6;
    margin-bottom: 24px;
}

.module {
    color: #c4d5df;
    font-size: 13px;
    padding: 9px 0;
    display: flex;
    align-items: center;
    gap: 10px;
}

.dot {
    width: 9px;
    height: 9px;
    min-width: 9px;
    border-radius: 50%;
    background: #54f5ae;
    box-shadow: 0 0 10px rgba(84, 245, 174, 0.6);
}


/* ============================================================
   RADIO
   ============================================================ */

div[data-testid="stRadio"] label {
    color: #e6f2f8 !important;
    font-weight: 600 !important;
}

div[data-testid="stRadio"] label p {
    color: #e6f2f8 !important;
}


/* ============================================================
   HERO
   ============================================================ */

.hero {
    background:
        radial-gradient(
            circle at 90% 10%,
            rgba(0, 210, 255, 0.12),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #082532,
            #07151e
        );

    border: 1px solid rgba(70, 210, 255, 0.25);
    border-radius: 24px;
    padding: 46px 48px;
    margin-bottom: 52px;

    box-shadow:
        0 20px 60px rgba(0, 0, 0, 0.30),
        inset 0 1px 0 rgba(255, 255, 255, 0.03);
}

.hero-title {
    color: #f4fbff;
    font-size: 48px;
    font-weight: 800;
    letter-spacing: -1.5px;
    margin-bottom: 18px;
}

.hero-subtitle {
    color: #a6bfce;
    font-size: 17px;
    letter-spacing: 2px;
    margin-bottom: 28px;
}

.online {
    display: inline-block;
    color: #54f5ae;
    background: rgba(84, 245, 174, 0.09);
    border: 1px solid rgba(84, 245, 174, 0.30);
    padding: 9px 17px;
    border-radius: 999px;
    font-family: 'Space Mono', monospace;
    font-size: 12px;
    font-weight: 700;
}


/* ============================================================
   SECTIONS
   ============================================================ */

.section {
    color: #f1faff;
    font-size: 28px;
    font-weight: 800;
    margin-top: 35px;
    margin-bottom: 24px;
    letter-spacing: -0.5px;
}


/* ============================================================
   RISK
   ============================================================ */

.risk-box {
    background: #09131f;
    border: 1px solid rgba(100, 210, 255, 0.18);
    border-radius: 22px;
    padding: 42px;
    text-align: center;
    margin-bottom: 40px;
}

.risk-number {
    color: #f4fbff;
    font-size: 70px;
    font-weight: 800;
    line-height: 1;
    letter-spacing: -2px;
}

.risk-out-of {
    color: #8fa8b9;
    font-size: 20px;
    font-family: 'Space Mono', monospace;
}

.risk-label {
    font-size: 25px;
    font-weight: 800;
    letter-spacing: 2px;
    margin-top: 16px;
}

.risk-description {
    color: #a4b9c7;
    font-size: 14px;
    margin-top: 10px;
}


/* ============================================================
   OVERVIEW CARDS
   ============================================================ */

.overview-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 18px;
    margin-bottom: 45px;
}

.overview-card {
    background: #0b1622;
    border: 1px solid rgba(100, 210, 255, 0.16);
    border-radius: 18px;
    padding: 25px;
    min-height: 150px;
    overflow: hidden;
}

.card-label {
    color: #91aabd;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 1.3px;
    text-transform: uppercase;
    margin-bottom: 18px;
}

.card-value {
    color: #f1faff;
    font-size: 28px;
    font-weight: 800;
    line-height: 1.15;
    overflow-wrap: anywhere;
    word-break: break-word;
}

.card-sub {
    color: #9aafbd;
    font-size: 13px;
    margin-top: 14px;
}


/* ============================================================
   TELEMETRY
   ============================================================ */

.telemetry-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 16px;
    margin-bottom: 45px;
}

.telemetry-card {
    background: #0b1622;
    border: 1px solid rgba(100, 210, 255, 0.16);
    border-radius: 17px;
    padding: 23px;
    overflow: hidden;
}

.telemetry-label {
    color: #a5bac7;
    font-size: 14px;
    margin-bottom: 12px;
}

.telemetry-value {
    color: #eefaff;
    font-size: 35px;
    font-weight: 700;
    line-height: 1.1;
    overflow-wrap: anywhere;
}


/* ============================================================
   STATUS
   ============================================================ */

.status-card {
    background: #071b19;
    border: 1px solid rgba(84, 245, 174, 0.24);
    border-radius: 17px;
    padding: 23px;
    margin-bottom: 18px;
}

.status-card-danger {
    background: #1a0d14;
    border-color: rgba(255, 91, 110, 0.35);
}

.status-title {
    color: #f1faff;
    font-size: 15px;
    font-weight: 800;
    margin-bottom: 12px;
}

.status-detail {
    color: #a8bcc8;
    font-size: 14px;
    line-height: 1.6;
}

.status-dot-green {
    color: #54f5ae;
}

.status-dot-red {
    color: #ff5b6e;
}


/* ============================================================
   SCORE
   ============================================================ */

.score-card {
    background: #0b1622;
    border: 1px solid rgba(100, 210, 255, 0.16);
    border-radius: 17px;
    padding: 25px;
    margin-bottom: 18px;
}

.score-title {
    color: #a2b8c5;
    font-size: 14px;
    margin-bottom: 10px;
}

.score-value {
    color: #eefaff;
    font-size: 40px;
    font-weight: 700;
}


/* ============================================================
   INDICATORS
   ============================================================ */

.indicator {
    color: #c1d2dc;
    font-size: 14px;
    margin: 12px 0;
    line-height: 1.5;
}

.indicator-warning {
    color: #ffd166;
}


/* ============================================================
   DECISION
   ============================================================ */

.decision-box {
    border-radius: 18px;
    padding: 24px 28px;
    margin-bottom: 25px;
}

.decision-normal {
    background: #06261c;
    border: 1px solid rgba(84, 245, 174, 0.25);
}

.decision-warning {
    background: #241d06;
    border: 1px solid rgba(255, 200, 87, 0.28);
}

.decision-critical {
    background: #250d15;
    border: 1px solid rgba(255, 91, 110, 0.35);
}

.decision-title {
    color: #f4fbff;
    font-size: 16px;
    font-weight: 800;
    margin-bottom: 8px;
}

.decision-text {
    color: #a9bcc8;
    font-size: 14px;
}


/* ============================================================
   EXPLANATION
   ============================================================ */

.explanation {
    background: #0b1622;
    border-radius: 15px;
    padding: 22px;
    border: 1px solid rgba(100, 210, 255, 0.14);
    color: #c0d1db;
    line-height: 1.7;
    margin-bottom: 30px;
}


/* ============================================================
   EVENTS
   ============================================================ */

.event {
    border-bottom: 1px solid rgba(100, 210, 255, 0.10);
    padding: 14px 0;
    color: #b6c9d4;
    font-family: 'Space Mono', monospace;
    font-size: 11px;
    line-height: 1.7;
}

.event:last-child {
    border-bottom: none;
}


/* ============================================================
   ARCHITECTURE
   ============================================================ */

.architecture {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    flex-wrap: wrap;
    margin: 30px 0 55px;
}

.arch-node {
    background: #0b1622;
    border: 1px solid rgba(100, 210, 255, 0.18);
    border-radius: 15px;
    padding: 18px 22px;
    min-width: 125px;
    text-align: center;
    color: #e4f7ff;
    font-size: 12px;
    font-weight: 700;
    line-height: 1.5;
}

.arch-arrow {
    color: #55dfff;
    font-size: 25px;
}


/* ============================================================
   GENERAL
   ============================================================ */

h1,
h2,
h3,
h4,
h5,
h6 {
    color: #f4fbff !important;
}

p,
li {
    color: #c1d1dc;
}

.stMarkdown p {
    color: #c1d1dc !important;
}

small {
    color: #a8bdc9 !important;
}

hr {
    border-color: rgba(100, 210, 255, 0.10) !important;
}


/* ============================================================
   BUTTONS
   ============================================================ */

.stButton > button {
    background: #101c29;
    color: #d9f5ff;
    border: 1px solid rgba(85, 223, 255, 0.18);
    border-radius: 10px;
}

.stButton > button:hover {
    border-color: rgba(85, 223, 255, 0.45);
    color: white;
}


/* ============================================================
   DATAFRAME
   ============================================================ */

[data-testid="stDataFrame"] {
    border-radius: 15px;
    overflow: hidden;
}


/* ============================================================
   RESPONSIVE
   ============================================================ */

@media (max-width: 1100px) {

    .overview-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }

    .telemetry-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }

    .hero-title {
        font-size: 38px;
    }
}

@media (max-width: 700px) {

    .overview-grid {
        grid-template-columns: 1fr;
    }

    .telemetry-grid {
        grid-template-columns: 1fr;
    }

    .hero {
        padding: 30px 25px;
    }

    .hero-title {
        font-size: 32px;
    }

    .hero-subtitle {
        font-size: 13px;
    }
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown(
    """
<div class="sidebar-title">
    🎛️ CONTROL PANEL
</div>

<div class="sidebar-description">
    Select a scenario to simulate the
    SafeLab Sentinel security pipeline.
</div>
""",
    unsafe_allow_html=True,
)


mode = st.sidebar.radio(
    "Simulation Mode",
    [
        "Normal",
        "Hazard",
        "Cyber Attack",
    ],
)


st.sidebar.divider()


st.sidebar.markdown(
    """
<div style="
    color:#e0f2f8;
    font-size:13px;
    font-weight:800;
    margin-bottom:10px;
">
    SYSTEM MODULES
</div>

<div class="module">
    <span class="dot"></span>
    Sensor Monitoring
</div>

<div class="module">
    <span class="dot"></span>
    Device Authentication
</div>

<div class="module">
    <span class="dot"></span>
    HMAC Integrity
</div>

<div class="module">
    <span class="dot"></span>
    Cybersecurity Analysis
</div>

<div class="module">
    <span class="dot"></span>
    AI Anomaly Detection
</div>

<div class="module">
    <span class="dot"></span>
    Risk Engine
</div>

<div class="module">
    <span class="dot"></span>
    Event Database
</div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# SENSOR DATA
# ============================================================

if mode == "Normal":

    sensor_data = {
        "device_id": "ARDUINO_01",
        "timestamp": "2026-08-30T00:00:00",
        "temperature": 30,
        "aqi": 45,
        "vibration": 0.12,
    }

elif mode == "Hazard":

    sensor_data = {
        "device_id": "ARDUINO_01",
        "timestamp": "2026-08-30T00:05:00",
        "temperature": 85,
        "aqi": 250,
        "vibration": 3.0,
    }

else:

    sensor_data = {
        "device_id": "UNKNOWN_DEVICE",
        "timestamp": "2026-08-30T00:10:00",
        "temperature": 30,
        "aqi": 45,
        "vibration": 0.12,
    }


# ============================================================
# RUN PIPELINE
# ============================================================

try:

    pipeline_result = run_pipeline(
        sensor_data,
        tamper=(mode == "Cyber Attack"),
    )

    if not isinstance(pipeline_result, dict):
        pipeline_result = {}

except Exception as e:

    st.error(
        f"Pipeline error: {e}"
    )

    pipeline_result = {}


# ============================================================
# SAVE EVENT
# ============================================================

try:

    save_event(
        sensor_data,
        pipeline_result,
    )

except Exception:
    pass


# ============================================================
# SAFE HELPERS
# ============================================================

def safe_int(value, default=0):

    try:
        return int(float(value))

    except (TypeError, ValueError):
        return default


def safe_float(value, default=0.0):

    try:
        return float(value)

    except (TypeError, ValueError):
        return default


def safe_text(value, default="UNKNOWN"):

    if value is None:
        return default

    text = str(value).strip()

    if not text:
        return default

    return text


def safe_reasons(value):

    if value is None:
        return []

    if isinstance(value, str):
        return [value]

    if isinstance(value, (list, tuple, set)):
        return [str(item) for item in value]

    return [str(value)]


# ============================================================
# EXTRACT PIPELINE RESULTS
# ============================================================

device_verified = bool(
    pipeline_result.get(
        "device_verified",
        False,
    )
)


signature_valid = bool(
    pipeline_result.get(
        "signature_valid",
        False,
    )
)


security_status = safe_text(
    pipeline_result.get(
        "security_status",
        "UNKNOWN",
    )
)


security_risk = safe_text(
    pipeline_result.get(
        "security_risk",
        "UNKNOWN",
    )
)


security_risk_score = safe_int(
    pipeline_result.get(
        "security_risk_score",
        0,
    )
)


security_reasons = safe_reasons(
    pipeline_result.get(
        "security_reasons",
        pipeline_result.get(
            "reasons",
            [],
        ),
    )
)


ai_status = safe_text(
    pipeline_result.get(
        "ai_status",
        "UNKNOWN",
    )
)


ai_risk = safe_text(
    pipeline_result.get(
        "ai_risk",
        "UNKNOWN",
    )
)


ai_risk_score = safe_int(
    pipeline_result.get(
        "ai_risk_score",
        0,
    )
)


ai_prediction = safe_int(
    pipeline_result.get(
        "ai_prediction",
        0,
    )
)


final_status = safe_text(
    pipeline_result.get(
        "final_status",
        "UNKNOWN",
    )
)


action = safe_text(
    pipeline_result.get(
        "action",
        "UNKNOWN",
    )
)


# ============================================================
# NORMALIZE VALUES
# ============================================================

security_risk_score = max(
    0,
    min(
        100,
        security_risk_score,
    ),
)


ai_risk_score = max(
    0,
    min(
        100,
        ai_risk_score,
    ),
)


overall_risk = max(
    security_risk_score,
    ai_risk_score,
)


# ============================================================
# FALLBACK FINAL STATUS
# ============================================================

if final_status.upper() == "UNKNOWN":

    if overall_risk >= 80:

        final_status = "CRITICAL"

    elif overall_risk >= 40:

        final_status = "WARNING"

    else:

        final_status = "NORMAL"


status_upper = final_status.upper()


# ============================================================
# DEVICE DISPLAY
# ============================================================

device_id = safe_text(
    sensor_data.get(
        "device_id",
        "UNKNOWN_DEVICE",
    )
)


if device_id == "UNKNOWN_DEVICE":

    device_display = "UNAUTHORIZED"

else:

    device_display = device_id


device_display_html = escape(
    device_display
)


security_risk_html = escape(
    security_risk.upper()
)


ai_risk_html = escape(
    ai_risk.upper()
)


action_html = escape(
    action.upper()
)


status_html = escape(
    status_upper
)


# ============================================================
# HERO
# ============================================================

render_html(
    """
<div class="hero">

<div class="hero-title">
🛡️ SAFELAB SENTINEL
</div>

<div class="hero-subtitle">
AI-POWERED LABORATORY SAFETY & CYBERSECURITY COMMAND CENTER
</div>

<div class="online">
● SYSTEM OPERATIONAL
</div>

</div>
"""
)


# ============================================================
# LIVE SAFETY STATUS
# ============================================================

render_html(
    """
<div class="section">
🛡️ LIVE SAFETY STATUS
</div>
"""
)


if status_upper == "CRITICAL":

    risk_color = "#ff5b6e"
    risk_message = "IMMEDIATE ATTENTION REQUIRED"

elif status_upper == "WARNING":

    risk_color = "#ffc857"
    risk_message = "INVESTIGATION RECOMMENDED"

else:

    risk_color = "#54f5ae"
    risk_message = "ENVIRONMENT OPERATING NORMALLY"


render_html(
    f"""
<div class="risk-box">

<div class="risk-number">
{overall_risk}
<span class="risk-out-of">
/100
</span>
</div>

<div
class="risk-label"
style="color:{risk_color};"
>
{status_html}
</div>

<div class="risk-description">
{risk_message}
</div>

</div>
"""
)


# ============================================================
# SYSTEM OVERVIEW
# ============================================================

render_html(
    """
<div class="section">
📊 SYSTEM OVERVIEW
</div>
"""
)


device_status_text = (
    "Authenticated"
    if device_verified
    else "Rejected"
)


device_status_html = escape(
    device_status_text
)


render_html(
    f"""
<div class="overview-grid">

<div class="overview-card">

<div class="card-label">
DEVICE
</div>

<div class="card-value">
{device_display_html}
</div>

<div class="card-sub">
• {device_status_html}
</div>

</div>


<div class="overview-card">

<div class="card-label">
SECURITY RISK
</div>

<div class="card-value">
{security_risk_html}
</div>

<div class="card-sub">
Score: {security_risk_score}/100
</div>

</div>


<div class="overview-card">

<div class="card-label">
AI RISK
</div>

<div class="card-value">
{ai_risk_html}
</div>

<div class="card-sub">
Score: {ai_risk_score}/100
</div>

</div>


<div class="overview-card">

<div class="card-label">
RECOMMENDED ACTION
</div>

<div class="card-value">
{action_html}
</div>

<div class="card-sub">
Final system response
</div>

</div>

</div>
"""
)


# ============================================================
# LIVE SENSOR TELEMETRY
# ============================================================

render_html(
    """
<div class="section">
📡 LIVE SENSOR TELEMETRY
</div>
"""
)


temperature = sensor_data.get(
    "temperature",
    0,
)

aqi = sensor_data.get(
    "aqi",
    0,
)

vibration = sensor_data.get(
    "vibration",
    0,
)


render_html(
    f"""
<div class="telemetry-grid">

<div class="telemetry-card">

<div class="telemetry-label">
🌡️ Temperature
</div>

<div class="telemetry-value">
{temperature} °C
</div>

</div>


<div class="telemetry-card">

<div class="telemetry-label">
💨 Air Quality (AQI)
</div>

<div class="telemetry-value">
{aqi}
</div>

</div>


<div class="telemetry-card">

<div class="telemetry-label">
📳 Vibration
</div>

<div class="telemetry-value">
{vibration}
</div>

</div>

</div>
"""
)


# ============================================================
# INTELLIGENCE & SECURITY
# ============================================================

render_html(
    """
<div class="section">
🧠 INTELLIGENCE & SECURITY
</div>
"""
)


col1, col2 = st.columns(2)


# ============================================================
# SECURITY COLUMN
# ============================================================

with col1:

    st.markdown(
        "### 🔐 Security Verification"
    )


    if device_verified:

        render_html(
            """
<div class="status-card">

<div class="status-title">
<span class="status-dot-green">●</span>
DEVICE AUTHENTICATION
</div>

<div class="status-detail">
VERIFIED
</div>

</div>
"""
        )

    else:

        render_html(
            """
<div class="status-card status-card-danger">

<div class="status-title">
<span class="status-dot-red">●</span>
DEVICE AUTHENTICATION
</div>

<div class="status-detail">
REJECTED — UNAUTHORIZED DEVICE
</div>

</div>
"""
        )


    if signature_valid:

        render_html(
            """
<div class="status-card">

<div class="status-title">
<span class="status-dot-green">●</span>
HMAC MESSAGE INTEGRITY
</div>

<div class="status-detail">
VALID
</div>

</div>
"""
        )

    else:

        render_html(
            """
<div class="status-card status-card-danger">

<div class="status-title">
<span class="status-dot-red">●</span>
HMAC MESSAGE INTEGRITY
</div>

<div class="status-detail">
INVALID — POSSIBLE TAMPERING
</div>

</div>
"""
        )


    render_html(
        f"""
<div class="score-card">

<div class="score-title">
Security Risk Score
</div>

<div class="score-value">
{security_risk_score}/100
</div>

</div>
"""
    )


    st.markdown(
        "#### Security Indicators"
    )


    if security_reasons:

        for reason in security_reasons:

            reason_html = escape(
                str(reason)
            )

            render_html(
                f"""
<div class="indicator indicator-warning">
⚠️ {reason_html}
</div>
"""
            )

    else:

        render_html(
            """
<div class="indicator">
🟢 All monitored security parameters are normal
</div>
"""
        )


# ============================================================
# AI COLUMN
# ============================================================

with col2:

    st.markdown(
        "### 🤖 AI Threat Analysis"
    )


    ai_status_upper = ai_status.upper()


    ai_anomaly = (
        ai_status_upper in [
            "SUSPICIOUS",
            "ANOMALY",
            "ABNORMAL",
        ]
        or ai_prediction == 1
    )


    if ai_anomaly:

        render_html(
            """
<div class="status-card status-card-danger">

<div class="status-title">
🚨 ANOMALY DETECTED
</div>

<div class="status-detail">
AI classification indicates abnormal behaviour.
</div>

</div>
"""
        )

    else:

        render_html(
            """
<div class="status-card">

<div class="status-title">
<span class="status-dot-green">●</span>
NO SIGNIFICANT ANOMALY
</div>

<div class="status-detail">
AI analysis indicates normal behaviour.
</div>

</div>
"""
        )


    render_html(
        f"""
<div class="score-card">

<div class="score-title">
AI Risk Score
</div>

<div class="score-value">
{ai_risk_score}/100
</div>

</div>
"""
    )


    ai_status_html = escape(
        ai_status_upper
    )


    render_html(
        f"""
<div class="indicator">
AI Status:
<strong>{ai_status_html}</strong>
</div>

<div class="indicator">
AI Prediction:
<strong>{ai_prediction}</strong>
</div>
"""
    )


# ============================================================
# FINAL SYSTEM DECISION
# ============================================================

render_html(
    """
<div class="section">
🚨 FINAL SYSTEM DECISION
</div>
"""
)


if status_upper == "CRITICAL":

    decision_class = "decision-critical"
    decision_icon = "🔴"
    decision_title = "SYSTEM CRITICAL"
    decision_text = (
        "Immediate intervention required."
    )

elif status_upper == "WARNING":

    decision_class = "decision-warning"
    decision_icon = "🟡"
    decision_title = "SYSTEM WARNING"
    decision_text = (
        "Investigation and corrective action recommended."
    )

else:

    decision_class = "decision-normal"
    decision_icon = "🟢"
    decision_title = "SYSTEM NORMAL"
    decision_text = (
        "Environment is operating within expected conditions."
    )


render_html(
    f"""
<div class="decision-box {decision_class}">

<div class="decision-title">
{decision_icon} {decision_title}
</div>

<div class="decision-text">
{decision_text}
</div>

</div>
"""
)


# ============================================================
# FINAL STATUS CARDS
# ============================================================

final_col1, final_col2 = st.columns(2)


with final_col1:

    render_html(
        f"""
<div class="overview-card">

<div class="card-label">
FINAL STATUS
</div>

<div class="card-value">
{status_html}
</div>

</div>
"""
    )


with final_col2:

    render_html(
        f"""
<div class="overview-card">

<div class="card-label">
RECOMMENDED ACTION
</div>

<div class="card-value">
{action_html}
</div>

</div>
"""
    )


# ============================================================
# DECISION EXPLANATION
# ============================================================

render_html(
    """
<div class="section">
💡 DECISION EXPLANATION
</div>
"""
)


if status_upper == "CRITICAL":

    explanation = (
        "The system detected a critical condition requiring "
        "immediate attention."
    )

elif status_upper == "WARNING":

    explanation = (
        "The system detected an abnormal condition that "
        "requires investigation."
    )

elif mode == "Cyber Attack":

    explanation = (
        "The cybersecurity layer detected an unauthorized "
        "or potentially tampered sensor communication."
    )

else:

    explanation = (
        "All monitored parameters are currently within "
        "the expected operating conditions."
    )


explanation_icon = (
    "🚨"
    if status_upper == "CRITICAL"
    else "💡"
)


render_html(
    f"""
<div class="explanation">

{explanation_icon}
&nbsp;&nbsp;
{escape(explanation)}

</div>
"""
)


# ============================================================
# HISTORICAL MONITORING
# ============================================================

render_html(
    """
<div class="section">
📈 HISTORICAL MONITORING
</div>
"""
)


try:

    recent_events = get_recent_events(20)

except Exception:

    recent_events = []


if recent_events:

    history = pd.DataFrame(
        recent_events
    )


    if "id" in history.columns:

        history = history.sort_values(
            "id"
        )


    history_col1, history_col2 = st.columns(
        [1.5, 1]
    )


    # ========================================================
    # SENSOR TRENDS
    # ========================================================

    with history_col1:

        st.markdown(
            "### 📊 Sensor Trends"
        )


        chart_columns = [
            "temperature",
            "aqi",
            "vibration",
        ]


        available_columns = [
            column
            for column in chart_columns
            if column in history.columns
        ]


        if available_columns:

            chart_data = history[
                available_columns
            ].copy()


            chart_data.columns = [
                column.capitalize()
                for column in available_columns
            ]


            st.line_chart(
                chart_data,
                width="stretch",
            )

        else:

            st.info(
                "Sensor trend data is not available."
            )


    # ========================================================
    # RECENT SECURITY EVENTS
    # ========================================================

    with history_col2:

        st.markdown(
            "### ⚡ Recent Security Events"
        )


        events_preview = (
            history
            .tail(7)
            .iloc[::-1]
        )


        for _, row in events_preview.iterrows():

            timestamp = escape(
                str(
                    row.get(
                        "timestamp",
                        "--",
                    )
                )
            )


            status = escape(
                str(
                    row.get(
                        "final_status",
                        "UNKNOWN",
                    )
                )
            )


            action_value = escape(
                str(
                    row.get(
                        "action",
                        "--",
                    )
                )
            )


            status_upper_event = (
                status.upper()
            )


            if status_upper_event == "CRITICAL":

                icon = "🔴"

            elif status_upper_event == "WARNING":

                icon = "🟡"

            else:

                icon = "🟢"


            render_html(
                f"""
<div class="event">

{icon} {timestamp}

<br>

STATUS:
{status_upper_event}

&nbsp; | &nbsp;

ACTION:
{action_value}

</div>
"""
            )

else:

    st.info(
        "No monitoring history available yet."
    )


# ============================================================
# EVENT AUDIT LOG
# ============================================================

render_html(
    """
<div class="section">
📋 EVENT AUDIT LOG
</div>
"""
)


if recent_events:

    events = pd.DataFrame(
        recent_events
    )


    display_columns = [
        "timestamp",
        "device_id",
        "security_status",
        "security_risk",
        "security_risk_score",
        "ai_status",
        "ai_risk",
        "ai_risk_score",
        "final_status",
        "action",
    ]


    available_display_columns = [
        column
        for column in display_columns
        if column in events.columns
    ]


    if available_display_columns:

        st.dataframe(
            events[
                available_display_columns
            ],
            width="stretch",
            hide_index=True,
        )

    else:

        st.dataframe(
            events,
            width="stretch",
            hide_index=True,
        )

else:

    st.info(
        "No recent events available."
    )


# ============================================================
# ARCHITECTURE
# ============================================================

render_html(
    """
<div class="section">
⚙️ SENTINEL ARCHITECTURE
</div>
"""
)


render_html(
    """
<div class="architecture">

<div class="arch-node">
📡<br>
SENSOR
</div>

<div class="arch-arrow">
→
</div>

<div class="arch-node">
🔐<br>
DEVICE<br>
AUTHENTICATION
</div>

<div class="arch-arrow">
→
</div>

<div class="arch-node">
🛡️<br>
HMAC<br>
INTEGRITY
</div>

<div class="arch-arrow">
→
</div>

<div class="arch-node">
🔎<br>
SECURITY<br>
ANALYSIS
</div>

<div class="arch-arrow">
→
</div>

<div class="arch-node">
🤖<br>
AI ANOMALY<br>
DETECTION
</div>

<div class="arch-arrow">
→
</div>

<div class="arch-node">
🎯<br>
RISK<br>
ENGINE
</div>

<div class="arch-arrow">
→
</div>

<div class="arch-node">
🚨<br>
FINAL<br>
DECISION
</div>

</div>
"""
)


# ============================================================
# HARDWARE SIMULATION
# ============================================================

render_html(
    """
<div class="section">
🔌 ARDUINO HARDWARE SIMULATION
</div>
"""
)


st.caption(
    "The current prototype uses an Arduino-based hardware "
    "simulation to demonstrate temperature, air quality, "
    "vibration telemetry and the SafeLab Sentinel security pipeline."
)


circuit_image = (
    Path(__file__).resolve().parent
    / "circuit.png"
)


if circuit_image.exists():

    st.image(
        str(circuit_image),
        caption="Arduino-based hardware simulation",
        width="stretch",
    )

else:

    st.info(
        "Hardware simulation diagram not found."
    )


# ============================================================
# FOOTER
# ============================================================

render_html(
    """
<div style="
text-align:center;
color:#66808e;
font-family:'Space Mono', monospace;
font-size:9px;
letter-spacing:1.2px;
padding:35px 0 5px;
">

SAFELAB SENTINEL
&nbsp;•&nbsp;
AI SAFETY + CYBERSECURITY
&nbsp;•&nbsp;
HACKATHON PROTOTYPE

</div>
"""
)