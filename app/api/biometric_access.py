from flask import Blueprint, jsonify
import random

# ensure that you set a URL prefix for the endpoint's route
bp = Blueprint('biometric_access', __name__, url_prefix='/api/biometric-access')

@bp.route('/')
def get_biometric_access_logs():
    data = {
        "scanner_id": "biometric-2F",
        "user_id": "unknown",
        "access_result": "denied",
        "reason": "fingerprint mismatch",
        "location": "lab wing",
        "timestamp": "2025-04-03T10:26:03Z"
    }
    return jsonify(data)
