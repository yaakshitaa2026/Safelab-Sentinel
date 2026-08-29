from cybersecurity.devices import (
    verify_device,
    get_device_secret
)

from cybersecurity.security import (
    generate_signature,
    verify_signature
)


# ============================================================
# SAMPLE SENSOR DATA
# ============================================================

sensor_data = {
    "device_id": "ESP32_01",
    "timestamp": "2026-08-29T23:00:00",
    "temperature": 30,
    "humidity": 60,
    "voltage": 3.3,
    "current": 0.42,
    "vibration": 0.12
}


print("\n" + "=" * 60)
print("SAFE LAB SENTINEL - CYBERSECURITY TEST")
print("=" * 60)


# ============================================================
# TEST 1 — AUTHORIZED DEVICE
# ============================================================

print("\n[TEST 1] AUTHORIZED DEVICE")

device_id = sensor_data["device_id"]

authorized = verify_device(device_id)

print("Device:", device_id)
print("Authorized:", authorized)


# ============================================================
# TEST 2 — UNKNOWN DEVICE
# ============================================================

print("\n[TEST 2] UNKNOWN DEVICE")

unknown_device = "UNKNOWN_DEVICE"

authorized_unknown = verify_device(unknown_device)

print("Device:", unknown_device)
print("Authorized:", authorized_unknown)


# ============================================================
# TEST 3 — VALID HMAC
# ============================================================

print("\n[TEST 3] VALID HMAC")

secret = get_device_secret(device_id)

signature = generate_signature(
    sensor_data,
    secret
)

valid_signature = verify_signature(
    sensor_data,
    signature,
    secret
)

print("Signature generated:", signature)
print("Signature valid:", valid_signature)


# ============================================================
# TEST 4 — TAMPERED DATA
# ============================================================

print("\n[TEST 4] TAMPERED DATA")

tampered_data = sensor_data.copy()

tampered_data["temperature"] = 99

tampered_signature_valid = verify_signature(
    tampered_data,
    signature,
    secret
)

print("Original temperature:", sensor_data["temperature"])
print("Tampered temperature:", tampered_data["temperature"])
print(
    "Signature valid after tampering:",
    tampered_signature_valid
)


print("\n" + "=" * 60)
print("CYBERSECURITY TEST COMPLETE")
print("=" * 60)