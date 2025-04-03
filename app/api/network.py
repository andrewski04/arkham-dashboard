from flask import Blueprint, jsonify
import random

# This is an example blueprint for the network-monitoring endpoint. 
# A new blueprint will be created for each endpoint.

# ensure that you set a URL prefix for the endpoint's route
bp = Blueprint('network_api', __name__, url_prefix='/api/network-monitoring')

# this contains static sample data, but in the future will generate more logs.
@bp.route('/')
def get_network_logs():
    data = {
        "source_ip": "192.168.1.54",
        "destination_ip": "10.0.0.7",
        "protocol": "TCP",
        "port": 22,
        "action": "blocked",
        "threat_level": random.choice(["low", "medium", "high"]),
        "timestamp": "2025-04-03T10:23:00Z"
    }
    return jsonify(data)
