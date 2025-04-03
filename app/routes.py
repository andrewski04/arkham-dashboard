from flask import Blueprint, render_template

# This is the blueprint for the frontend app, and where the routes for it are declared.
# Currently, it loads the dashboard template, which uses javascript to make API calls.

bp = Blueprint('frontend', __name__)

@bp.route('/')
def dashboard():
    return render_template('dashboard.html')
