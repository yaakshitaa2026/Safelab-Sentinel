DEVICES = {
    "ESP32_01": {
        "secret": "ESP32_SECRET_KEY_01",
        "active": True
    },
    "ESP32_02": {
        "secret": "ESP32_SECRET_KEY_02",
        "active": True
    }
}


def verify_device(device_id):
    device = DEVICES.get(device_id)

    if device is None:
        return False

    return device["active"]


def get_device_secret(device_id):
    device = DEVICES.get(device_id)

    if device is None:
        return None

    return device["secret"]