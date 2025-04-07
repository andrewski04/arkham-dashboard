from flask import Blueprint, jsonify
import random

# ensure that you set a URL prefix for the endpoint's route
bp = Blueprint('inmate_threats', __name__, url_prefix='/api/inmate-threats')

@bp.route('/')
def get_inmate_threats_logs():
    data = {
        "inmate_id": "ARK-056",
        "name": "Edward Nigma",
        "threat_level": "high",
        "last_known_location": "restricted library",
        "incident_flag": "tampering with surveillance",
        "recommendation": "increased surveillance and access revocation",
        "timestamp": "2025-04-03T10:28:15Z"
    }
    return jsonify(data)
