from flask import Blueprint, jsonify
import random

# ensure that you set a URL prefix for the endpoint's route
bp = Blueprint('server_logs', __name__, url_prefix='/api/server-logs')

@bp.route('/')
def get_server_logs():
    data = {
        "server": "auth-node-3",
        "event": "Multiple failed SSH login attempts",
        "attempts": 7,
        "status": "investigating",
        "timestamp": "2025-04-03T10:21:15Z"
    }
    return jsonify(data)
