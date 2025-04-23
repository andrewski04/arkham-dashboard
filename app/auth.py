import functools
import json
import os
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

bp = Blueprint('auth', __name__, url_prefix='/auth')

# Path to the users file
USERS_FILE = os.path.join(os.path.dirname(__file__), 'users.json')

def load_users():
    """Loads users from the JSON file."""
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {} # Return empty dict if file is empty or invalid

def save_users(users):
    """Saves users to the JSON file."""
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

@bp.route('/register', methods=('GET', 'POST'))
def register():
    """Handles user registration."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif username in users:
            error = f"User {username} is already registered."

        if error is None:
            users[username] = {'password': generate_password_hash(password)}
            save_users(users)
            flash('Registration successful! Please log in.', 'success')
            # Redirect to the auth blueprint's login view
            return redirect(url_for('auth.login'))

        flash(error, 'danger')

    # If GET request or registration failed, show the registration page
    # Assuming the template is still in the main templates folder
    return render_template('register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    """Handles user login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        error = None

        user_data = users.get(username)

        if user_data is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user_data['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = username
            flash('Login successful!', 'success')
            # Redirect to the main dashboard after login
            return redirect(url_for('frontend.dashboard'))

        flash(error, 'danger')

    # If GET request or login failed, show the login page
    # Assuming the template is still in the main templates folder
    return render_template('login.html')


@bp.route('/logout')
def logout():
    """Logs the user out."""
    session.clear()
    flash('You have been logged out.', 'info')
    # Redirect to the auth blueprint's login view
    return redirect(url_for('auth.login'))


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session.get('user_id') is None:
            # Redirect to the auth blueprint's login view
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
