import hmac
import hashlib
import json


def generate_signature(data, secret_key):
    message = json.dumps(
        data,
        sort_keys=True,
        separators=(",", ":")
    ).encode()

    signature = hmac.new(
        secret_key.encode(),
        message,
        hashlib.sha256
    ).hexdigest()

    return signature


def verify_signature(data, received_signature, secret_key):
    expected_signature = generate_signature(
        data,
        secret_key
    )

    return hmac.compare_digest(
        expected_signature,
        received_signature
    )