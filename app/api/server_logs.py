from flask import Blueprint, jsonify
from app.api.sample_log_generator import generate_server_log
import datetime

# Blueprint for server logs API
bp = Blueprint('server_logs_api', __name__, url_prefix='/api/server-logs')

@bp.route('/')
def get_server_logs():
    # Generate a list of logs
    logs = [generate_server_log() for _ in range(50)] # Generate 50 sample logs
    # Sort logs by timestamp (descending - newest first)
    logs.sort(key=lambda x: x['timestamp'], reverse=True)
    return jsonify(logs) # Return the sorted list
