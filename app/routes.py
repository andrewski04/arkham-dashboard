from flask import Blueprint, render_template

# This is the blueprint for the frontend app, and where the routes for it are declared.
# Currently, it loads the dashboard template, which uses javascript to make API calls.

bp = Blueprint('frontend', __name__)

@bp.route('/')
def dashboard():
    """Main dashboard overview page."""
    return render_template('dashboard.html')

@bp.route('/network')
def network_logs():
    """Page for viewing network logs."""
    return render_template('network.html')

@bp.route('/server-logs')
def server_logs():
    """Page for viewing server logs."""
    return render_template('server_logs.html')

@bp.route('/video-surveillance')
def video_surveillance_logs():
    """Page for viewing video surveillance logs."""
    return render_template('video_surveillance.html')

@bp.route('/biometric-access')
def biometric_access_logs():
    """Page for viewing biometric access logs."""
    return render_template('biometric_access.html')

@bp.route('/physical-security')
def physical_security_logs():
    """Page for viewing physical security logs."""
    return render_template('physical_security.html')

@bp.route('/internal-comms')
def internal_comms_logs():
    """Page for viewing internal communication logs."""
    return render_template('internal_comms.html')

@bp.route('/inmate-threats')
def inmate_threats_logs():
    """Page for viewing inmate threat logs."""
    return render_template('inmate_threats.html')
