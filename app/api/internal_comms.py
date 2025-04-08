from flask import Blueprint, jsonify
from app.api.sample_log_generator import generate_internal_comms_log
import datetime

# Blueprint for internal communications logs API
bp = Blueprint('internal_comms_api', __name__, url_prefix='/api/internal-comms')

@bp.route('/')
def get_internal_comms_logs():
    # Generate a list of logs
    logs = [generate_internal_comms_log() for _ in range(50)] # Generate 50 sample logs
    # Sort logs by timestamp (descending - newest first)
    logs.sort(key=lambda x: x['timestamp'], reverse=True)
    return jsonify(logs) # Return the sorted list
