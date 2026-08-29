from cybersecurity.security import (
    generate_signature,
    verify_signature
)

from cybersecurity.risk_engine import (
    calculate_risk
)


# Our test device
secret = "ESP32_SECRET_KEY_01"

# Normal sensor data
data = {
    "device_id": "ESP32_01",
    "temperature": 38,
    "humidity": 60
}


# Create a security signature
signature = generate_signature(
    data,
    secret
)

print("================================")
print("CYBERSECURITY TEST")
print("================================")

print("\nGenerated HMAC signature:")
print(signature)

# Check whether the signature is valid
result = verify_signature(
    data,
    signature,
    secret
)
# Simulate an attacker changing the temperature
data["temperature"] = 99

tampered_result = verify_signature(
    data,
    signature,
    secret
)

print("\nAfter someone changes the temperature to 99:")
print("Is the tampered signature valid?")
print(tampered_result)

print("\nIs the signature valid?")
print(result)

# Check the risk level
risk = calculate_risk(data)

print("\nRisk analysis:")
print(risk)

print("\n================================")
print("TEST COMPLETE")
print("================================")
# Test an unknown device

fake_data = {
    "device_id": "HACKER_01",
    "temperature": 38,
    "humidity": 60
}

print("\n================================")
print("UNKNOWN DEVICE TEST")
print("================================")

from cybersecurity.devices import verify_device

fake_device_result = verify_device(
    fake_data["device_id"]
)

print("\nIs the device authorized?")
print(fake_device_result)