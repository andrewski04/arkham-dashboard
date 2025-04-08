from flask import Blueprint, jsonify
from app.api.sample_log_generator import generate_biometric_access_log
import datetime

# ensure that you set a URL prefix for the endpoint's route
bp = Blueprint('biometric_access', __name__, url_prefix='/api/biometric-access')

@bp.route('/')
def get_biometric_access_logs():
    # Generate a list of logs
    logs = [generate_biometric_access_log() for _ in range(50)] # Generate 50 sample logs
    # Sort logs by timestamp (descending - newest first)
    logs.sort(key=lambda x: x['timestamp'], reverse=True)
    return jsonify(logs) # Return the sorted list
