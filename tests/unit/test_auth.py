import pytest
from flask import session, url_for, flash, Flask
from werkzeug.security import check_password_hash
import json
import os
from unittest.mock import patch, MagicMock

# Assuming your Flask app instance is created in app/__init__.py
from app import create_app
# Import the functions and variables to be tested from the new auth file
from app.auth import load_users, save_users, login, register, logout, login_required, USERS_FILE

# --- Fixtures ---

@pytest.fixture(autouse=True)
def mock_users_file_path():
    """Ensure USERS_FILE points to a test-specific location."""
    # Patch USERS_FILE in the correct module (app.auth)
    with patch('app.auth.USERS_FILE', 'test_users.json') as mock_path:
        # Clean up the mock file before and after each test
        if os.path.exists(mock_path):
            os.remove(mock_path)
        yield mock_path
        if os.path.exists(mock_path):
            os.remove(mock_path)

@pytest.fixture
def app_context():
    """Create a minimal Flask app context for testing route logic."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'test-secret'
    app.config['SERVER_NAME'] = 'localhost.test' # For url_for

    # Add dummy routes with the correct endpoint names needed for url_for
    # These should match the actual blueprint structure
    @app.route('/auth/login', endpoint='auth.login')
    def dummy_login(): pass
    @app.route('/', endpoint='frontend.dashboard')
    def dummy_dashboard(): pass
    @app.route('/auth/register', endpoint='auth.register')
    def dummy_register(): pass
    @app.route('/auth/logout', endpoint='auth.logout')
    def dummy_logout(): pass

    with app.app_context():
        with app.test_request_context(): # For request object access
            yield app

# --- Tests for load_users and save_users ---

def test_load_users_file_not_exist(mock_users_file_path):
    """Test load_users when the file doesn't exist."""
    assert load_users() == {}

def test_load_users_empty_file(mock_users_file_path):
    """Test load_users with an empty file."""
    with open(mock_users_file_path, 'w') as f:
        f.write('')
    assert load_users() == {}

def test_load_users_invalid_json(mock_users_file_path):
    """Test load_users with invalid JSON."""
    with open(mock_users_file_path, 'w') as f:
        f.write('{invalid json')
    assert load_users() == {}

def test_load_users_success(mock_users_file_path):
    """Test load_users reads valid JSON correctly."""
    users_data = {'user1': {'password': 'hash1'}}
    with open(mock_users_file_path, 'w') as f:
        json.dump(users_data, f)
    assert load_users() == users_data

def test_save_users(mock_users_file_path):
    """Test save_users writes data correctly."""
    users_data = {'user1': {'password': 'hash1'}, 'user2': {'password': 'hash2'}}
    save_users(users_data)
    with open(mock_users_file_path, 'r') as f:
        assert json.load(f) == users_data

# --- Tests for login_required decorator ---

@pytest.fixture
def protected_route(app_context):
    """A dummy route protected by login_required."""
    @login_required
    def dummy_protected_route():
        return "Protected Content", 200
    return dummy_protected_route

def test_login_required_not_logged_in(app_context, protected_route):
    """Test login_required redirects if user not in session."""
    with app_context.test_request_context():
        response = protected_route()
        assert response.status_code == 302
        # Update url_for to point to the auth blueprint
        assert response.location == url_for('auth.login')

def test_login_required_logged_in(app_context, protected_route):
    """Test login_required allows access if user is in session."""
    with app_context.test_request_context():
        # Patch session within the app.auth module where the decorator uses it
        with patch('app.auth.session', {'user_id': 'testuser'}):
             response = protected_route()
             # The decorator should now allow access
             assert response == ("Protected Content", 200)


# --- Tests for route logic (login, register, logout) ---
# These tests focus on the logic within the route functions, mocking external calls
# Update patch targets to 'app.auth'

@patch('app.auth.render_template')
def test_login_get(mock_render, app_context):
    """Test GET request to login route renders template."""
    with app_context.test_request_context(method='GET', path='/auth/login'):
        response = login()
        mock_render.assert_called_once_with('login.html')
        # The route function itself returns the result of render_template
        assert response == mock_render.return_value

@patch('app.auth.load_users')
@patch('app.auth.check_password_hash')
@patch('app.auth.flash')
@patch('app.auth.redirect')
@patch('app.auth.url_for')
@patch('app.auth.session') # Patch session used by app.auth
def test_login_post_success(mock_session, mock_url_for, mock_redirect, mock_flash, mock_check_hash, mock_load_users, app_context):
    """Test successful POST request to login."""
    # Configure mock_session methods for assertion
    mock_session.clear = MagicMock()
    mock_session.__setitem__ = MagicMock()

    mock_load_users.return_value = {'testuser': {'password': 'hashed_password'}}
    mock_check_hash.return_value = True
    mock_url_for.return_value = '/dashboard' # Mock url_for return value
    mock_redirect.return_value = "Redirected to Dashboard" # Mock redirect return value

    with app_context.test_request_context(method='POST', path='/auth/login', data={'username': 'testuser', 'password': 'password'}):
        response = login() # This will use the mocked session

        mock_load_users.assert_called_once()
        mock_check_hash.assert_called_once_with('hashed_password', 'password')
        # Assert that the mocked session object was called correctly
        mock_session.clear.assert_called_once()
        mock_session.__setitem__.assert_called_once_with('user_id', 'testuser')
        mock_flash.assert_called_once_with('Login successful!', 'success')
        # Login redirects to frontend.dashboard
        mock_url_for.assert_called_once_with('frontend.dashboard')
        mock_redirect.assert_called_once_with('/dashboard')
        assert response == "Redirected to Dashboard"

@patch('app.auth.load_users')
@patch('app.auth.check_password_hash')
@patch('app.auth.flash')
@patch('app.auth.render_template')
@patch('app.auth.session', MagicMock())
def test_login_post_wrong_user(mock_render, mock_flash, mock_check_hash, mock_load_users, app_context):
    """Test POST request to login with incorrect username."""
    mock_load_users.return_value = {'anotheruser': {'password': 'hash'}}

    with app_context.test_request_context(method='POST', path='/auth/login', data={'username': 'wronguser', 'password': 'password'}):
        response = login()
        mock_load_users.assert_called_once()
        mock_check_hash.assert_not_called()
        assert 'user_id' not in session
        mock_flash.assert_called_once_with('Incorrect username.', 'danger')
        mock_render.assert_called_once_with('login.html') # Should re-render login
        assert response == mock_render.return_value

@patch('app.auth.load_users')
@patch('app.auth.check_password_hash')
@patch('app.auth.flash')
@patch('app.auth.render_template')
@patch('app.auth.session', MagicMock())
def test_login_post_wrong_password(mock_render, mock_flash, mock_check_hash, mock_load_users, app_context):
    """Test POST request to login with incorrect password."""
    mock_load_users.return_value = {'testuser': {'password': 'hashed_password'}}
    mock_check_hash.return_value = False # Simulate wrong password

    with app_context.test_request_context(method='POST', path='/auth/login', data={'username': 'testuser', 'password': 'wrongpassword'}):
        response = login()
        mock_load_users.assert_called_once()
        mock_check_hash.assert_called_once_with('hashed_password', 'wrongpassword')
        assert 'user_id' not in session
        mock_flash.assert_called_once_with('Incorrect password.', 'danger')
        mock_render.assert_called_once_with('login.html') # Should re-render login
        assert response == mock_render.return_value


@patch('app.auth.render_template')
def test_register_get(mock_render, app_context):
    """Test GET request to register route renders template."""
    with app_context.test_request_context(method='GET', path='/auth/register'):
        response = register()
        mock_render.assert_called_once_with('register.html')
        assert response == mock_render.return_value

@patch('app.auth.load_users')
@patch('app.auth.generate_password_hash')
@patch('app.auth.save_users')
@patch('app.auth.flash')
@patch('app.auth.redirect')
@patch('app.auth.url_for')
def test_register_post_success(mock_url_for, mock_redirect, mock_flash, mock_save_users, mock_gen_hash, mock_load_users, app_context):
    """Test successful POST request to register."""
    mock_load_users.return_value = {} # No existing users
    mock_gen_hash.return_value = 'new_hashed_password'
    mock_url_for.return_value = '/auth/login' # Mock url_for return value
    mock_redirect.return_value = "Redirected to Login"

    with app_context.test_request_context(method='POST', path='/auth/register', data={'username': 'newuser', 'password': 'newpassword'}):
        response = register()

        mock_load_users.assert_called_once()
        mock_gen_hash.assert_called_once_with('newpassword')
        mock_save_users.assert_called_once_with({'newuser': {'password': 'new_hashed_password'}})
        mock_flash.assert_called_once_with('Registration successful! Please log in.', 'success')
        # Register redirects to auth.login
        mock_url_for.assert_called_once_with('auth.login')
        mock_redirect.assert_called_once_with('/auth/login')
        assert response == "Redirected to Login"

@patch('app.auth.load_users')
@patch('app.auth.generate_password_hash')
@patch('app.auth.save_users')
@patch('app.auth.flash')
@patch('app.auth.render_template')
def test_register_post_user_exists(mock_render, mock_flash, mock_save_users, mock_gen_hash, mock_load_users, app_context):
    """Test POST request to register when user already exists."""
    mock_load_users.return_value = {'existinguser': {'password': 'hash'}}

    with app_context.test_request_context(method='POST', path='/auth/register', data={'username': 'existinguser', 'password': 'password'}):
        response = register()

        mock_load_users.assert_called_once()
        mock_gen_hash.assert_not_called()
        mock_save_users.assert_not_called()
        mock_flash.assert_called_once_with('User existinguser is already registered.', 'danger')
        mock_render.assert_called_once_with('register.html')
        assert response == mock_render.return_value

@patch('app.auth.load_users')
@patch('app.auth.flash')
@patch('app.auth.render_template')
def test_register_post_missing_username(mock_render, mock_flash, mock_load_users, app_context):
    """Test POST request to register with missing username."""
    mock_load_users.return_value = {}
    with app_context.test_request_context(method='POST', path='/auth/register', data={'username': '', 'password': 'password'}):
        response = register()
        mock_flash.assert_called_once_with('Username is required.', 'danger')
        mock_render.assert_called_once_with('register.html')
        assert response == mock_render.return_value

@patch('app.auth.load_users')
@patch('app.auth.flash')
@patch('app.auth.render_template')
def test_register_post_missing_password(mock_render, mock_flash, mock_load_users, app_context):
    """Test POST request to register with missing password."""
    mock_load_users.return_value = {}
    with app_context.test_request_context(method='POST', path='/auth/register', data={'username': 'testuser', 'password': ''}):
        response = register()
        mock_flash.assert_called_once_with('Password is required.', 'danger')
        mock_render.assert_called_once_with('register.html')
        assert response == mock_render.return_value


@patch('app.auth.flash')
@patch('app.auth.redirect')
@patch('app.auth.url_for')
@patch('app.auth.session', MagicMock()) # Mock session in auth module
def test_logout(mock_url_for, mock_redirect, mock_flash, app_context):
    """Test logout route clears session and redirects."""
    session['user_id'] = 'testuser' # Simulate logged-in user
    mock_url_for.return_value = '/auth/login' # Mock url_for return value
    mock_redirect.return_value = "Redirected to Login"

    with app_context.test_request_context(method='GET', path='/auth/logout'):
        response = logout()

        assert 'user_id' not in session # Check session is cleared
        mock_flash.assert_called_once_with('You have been logged out.', 'info')
        # Logout redirects to auth.login
        mock_url_for.assert_called_once_with('auth.login')
        mock_redirect.assert_called_once_with('/auth/login')
        assert response == "Redirected to Login"
