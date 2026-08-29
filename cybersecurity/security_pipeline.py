from cybersecurity.devices import (
    verify_device,
    get_device_secret
)

from cybersecurity.security import (
    verify_signature
)

from cybersecurity.risk_engine import (
    calculate_risk
)


def process_message(data, signature):

    device_id = data.get("device_id")

    # Step 1: Verify device
    if not verify_device(device_id):
        return {
            "accepted": False,
            "reason": "Unknown device"
        }

    # Step 2: Get device secret
    secret = get_device_secret(device_id)

    # Step 3: Verify HMAC signature
    if not verify_signature(
        data,
        signature,
        secret
    ):
        return {
            "accepted": False,
            "reason": "Invalid signature"
        }

    # Step 4: Analyze risk
    risk = calculate_risk(data)

    return {
        "accepted": True,
        "security_status": "VERIFIED",
        "risk": risk
    }