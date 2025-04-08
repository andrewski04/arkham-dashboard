from flask import Blueprint, jsonify
from app.api.sample_log_generator import (
    generate_server_log,
    generate_physical_security_log,
    generate_biometric_access_log,
    generate_inmate_threat_log,
    generate_internal_comms_log,
    generate_network_log,
    generate_video_surveillance_log
)

bp = Blueprint('sample_logs', __name__, url_prefix='/api/sample-logs')

@bp.route('/')
def get_sample_logs():
    """Returns a single sample log from each category."""
    data = {
        "server_log": generate_server_log(),
        "physical_security_log": generate_physical_security_log(),
        "biometric_access_log": generate_biometric_access_log(),
        "inmate_threat_log": generate_inmate_threat_log(),
        "internal_comms_log": generate_internal_comms_log(),
        "network_log": generate_network_log(),
        "video_surveillance_log": generate_video_surveillance_log()
    }
    return jsonify(data)
