from flask import Blueprint, jsonify
from app.api.sample_log_generator import generate_physical_security_log
import datetime

# Blueprint for physical security logs API
bp = Blueprint('physical_security_api', __name__, url_prefix='/api/physical-security')

@bp.route('/')
def get_physical_security_logs():
    # Generate a list of logs
    logs = [generate_physical_security_log() for _ in range(50)] # Generate 50 sample logs
    # Sort logs by timestamp (descending - newest first)
    logs.sort(key=lambda x: x['timestamp'], reverse=True)
    return jsonify(logs) # Return the sorted list
