from flask import Blueprint, jsonify
import random

# ensure that you set a URL prefix for the endpoint's route
bp = Blueprint('internal_comms', __name__, url_prefix='/api/internal-comms')

@bp.route('/')
def get_internal_comms_logs():
    data = {
        "type": "lockdown alert",
        "recipients": ["security_team", "admin_office"],
        "message": "Zone 3 lockdown initiated due to intruder detection.",
        "sent_by": "automated-system",
        "timestamp": "2025-04-03T10:27:30Z"
    }
    return jsonify(data)
