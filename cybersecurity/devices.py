# ============================================================
# SAFELAB SENTINEL - DEVICE REGISTRY
# ============================================================

DEVICES = {

    "ARDUINO_01": {
        "secret": "ARDUINO_SECRET_KEY_01",
        "active": True
    },

    "ARDUINO_02": {
        "secret": "ARDUINO_SECRET_KEY_02",
        "active": True
    },

    "ESP32_01": {
        "secret": "ESP32_SECRET_KEY_01",
        "active": True
    },

    "ESP32_02": {
        "secret": "ESP32_SECRET_KEY_02",
        "active": True
    }
}


# ============================================================
# VERIFY DEVICE
# ============================================================

def verify_device(device_id):

    device = DEVICES.get(device_id)

    if device is None:
        return False

    return device["active"]


# ============================================================
# GET DEVICE SECRET
# ============================================================

def get_device_secret(device_id):

    device = DEVICES.get(device_id)

    if device is None:
        return None

    if not device["active"]:
        return None

    return device["secret"]