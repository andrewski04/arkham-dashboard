from flask import Blueprint, jsonify
import random

# ensure that you set a URL prefix for the endpoint's route
bp = Blueprint('physical_security', __name__, url_prefix='/api/physical-security')

@bp.route('/')
def get_physical_security_logs():
    data = {
        "system": "emergency_alarm",
        "location": "cell block D",
        "status": "active",
        "trigger_reason": "manual override",
        "timestamp": "2025-04-03T10:26:50Z"
    }
    return jsonify(data)
