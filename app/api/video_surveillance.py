from flask import Blueprint, jsonify
from app.api.sample_log_generator import generate_video_surveillance_log
import datetime

# Blueprint for video surveillance logs API
bp = Blueprint('video_surveillance_api', __name__, url_prefix='/api/video-surveillance')

@bp.route('/')
def get_video_surveillance_logs():
    # Generate a list of logs
    logs = [generate_video_surveillance_log() for _ in range(50)] # Generate 50 sample logs
    # Sort logs by timestamp (descending - newest first)
    logs.sort(key=lambda x: x['timestamp'], reverse=True)
    return jsonify(logs) # Return the sorted list
