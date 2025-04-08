from flask import Blueprint, jsonify
from app.api.sample_log_generator import generate_inmate_threat_log
import datetime

# Blueprint for inmate threats logs API
bp = Blueprint('inmate_threats_api', __name__, url_prefix='/api/inmate-threats')

@bp.route('/')
def get_inmate_threats_logs():
    # Generate a list of logs
    logs = [generate_inmate_threat_log() for _ in range(50)] # Generate 50 sample logs
    # Sort logs by timestamp (descending - newest first)
    logs.sort(key=lambda x: x['timestamp'], reverse=True)
    return jsonify(logs) # Return the sorted list
