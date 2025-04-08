from flask import Blueprint, jsonify
from app.api.sample_log_generator import generate_network_log
import datetime

# This is an example blueprint for the network-monitoring endpoint.
# A new blueprint will be created for each endpoint.

# ensure that you set a URL prefix for the endpoint's route
bp = Blueprint('network_api', __name__, url_prefix='/api/network-monitoring')

@bp.route('/')
def get_network_logs():
    # Generate a list of logs
    logs = [generate_network_log() for _ in range(50)] # Generate 50 sample logs
    # Sort logs by timestamp (descending - newest first)
    logs.sort(key=lambda x: x['timestamp'], reverse=True)
    return jsonify(logs) # Return the sorted list
