from flask import Blueprint, jsonify
import random

# ensure that you set a URL prefix for the endpoint's route
bp = Blueprint('video_surveillance', __name__, url_prefix='/api/video-surveillance')

@bp.route('/')
def get_video_surveillance_logs():
    data = {
        "location": "armory",
        "level": "severe",
        "activity": "unauthorized person detected",
        "timestamp": "2025-04-03T10:25:42Z"
    }
    return jsonify(data)
