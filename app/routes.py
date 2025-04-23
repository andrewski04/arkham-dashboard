from flask import Blueprint, render_template
from .auth import login_required # Import the decorator from auth.py

# This is the blueprint for the frontend app, and where the routes for it are declared.
# Currently, it loads the dashboard template, which uses javascript to make API calls.

bp = Blueprint('frontend', __name__, template_folder='templates')


@bp.route('/')
@login_required
def dashboard():
    """Main dashboard overview page."""
    return render_template('dashboard.html')


# Protect other routes as well
@bp.route('/network')
@login_required
def network_logs():
    """Page for viewing network logs."""
    return render_template('network.html')

@bp.route('/server-logs')
@login_required
def server_logs():
    """Page for viewing server logs."""
    return render_template('server_logs.html')

@bp.route('/video-surveillance')
@login_required
def video_surveillance_logs():
    """Page for viewing video surveillance logs."""
    return render_template('video_surveillance.html')

@bp.route('/biometric-access')
@login_required
def biometric_access_logs():
    """Page for viewing biometric access logs."""
    return render_template('biometric_access.html')

@bp.route('/physical-security')
@login_required
def physical_security_logs():
    """Page for viewing physical security logs."""
    return render_template('physical_security.html')

@bp.route('/internal-comms')
@login_required
def internal_comms_logs():
    """Page for viewing internal communication logs."""
    return render_template('internal_comms.html')

@bp.route('/inmate-threats')
@login_required
def inmate_threats_logs():
    """Page for viewing inmate threat logs."""
    return render_template('inmate_threats.html')
