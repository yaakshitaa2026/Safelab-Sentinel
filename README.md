# 🛡️ SafeLab Sentinel

### AI-Powered Cybersecurity and Safety Monitoring System for Laboratory Environments

SafeLab Sentinel is a software-based intelligent laboratory monitoring system that combines **sensor monitoring, cybersecurity, HMAC integrity verification, AI-based anomaly detection, risk analysis, and database logging** into a single pipeline.

The system is designed to detect both:

- ⚠️ Physical/environmental hazards
- 🔐 Cybersecurity threats such as unauthorized devices and tampered sensor data

---

# 🚨 Problem

Laboratory environments can contain sensitive equipment and potentially hazardous conditions.

Traditional monitoring systems may detect abnormal sensor readings, but they may not verify whether incoming data is:

- From an authorized device
- Authentic and untampered
- Safe to send to an AI system

SafeLab Sentinel addresses this by placing a cybersecurity verification layer **before AI analysis**.

---

# 💡 Solution

SafeLab Sentinel processes incoming sensor data through multiple security and intelligence layers:

```text
Sensor Data
     ↓
Device Authentication
     ↓
HMAC Integrity Verification
     ↓
Cybersecurity Risk Analysis
     ↓
AI Anomaly Detection
     ↓
Final Risk Decision
     ↓
Database Logging
     ↓
Dashboard Visualization