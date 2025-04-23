import pytest
from app import create_app
from flask import url_for
import os
import json

# Define the path to the users file relative to this test file
# Assuming tests/integration/ is one level down from the project root where app/ is
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
USERS_FILE = os.path.join(BASE_DIR, 'app', 'users.json')

@pytest.fixture
def client():
    # Ensure a clean state for users file before each test
    if os.path.exists(USERS_FILE):
        os.remove(USERS_FILE)
    with open(USERS_FILE, 'w') as f:
        json.dump({}, f)

    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False # Disable CSRF for testing forms easily
    app.config['SECRET_KEY'] = 'test-secret-key' # Use a consistent test key
    app.config['SERVER_NAME'] = 'localhost.test' # Add SERVER_NAME for url_for outside request context

    with app.test_client() as client:
        with app.app_context(): # Ensure context for operations within the fixture if needed
             yield client

    # Clean up users file after test run
    if os.path.exists(USERS_FILE):
        os.remove(USERS_FILE)


def test_dashboard_page_loads_unauthenticated(client):
    """Test that accessing dashboard redirects to login when not logged in."""
    response = client.get(url_for('frontend.dashboard'))
    assert response.status_code == 302 # Should redirect
    assert url_for('auth.login') in response.location # Should redirect to login


def test_dashboard_page_loads_authenticated(client):
    """Test that the dashboard loads successfully after login."""
    # Register a test user
    register_response = client.post(url_for('auth.register'), data={
        'username': 'testuser',
        'password': 'password'
    }, follow_redirects=True)
    assert register_response.status_code == 200 # Should redirect to login page
    assert b"Registration successful! Please log in." in register_response.data

    # Log in the test user
    login_response = client.post(url_for('auth.login'), data={
        'username': 'testuser',
        'password': 'password'
    }, follow_redirects=True)
    assert login_response.status_code == 200 # Should redirect to dashboard
    assert b"Login successful!" in login_response.data
    assert b"Arkham Asylum Security Dashboard" in login_response.data # Check for dashboard content

    # Now access the dashboard directly (should be logged in)
    dashboard_response = client.get(url_for('frontend.dashboard'))
    assert dashboard_response.status_code == 200
    assert b"Arkham Asylum Security Dashboard" in dashboard_response.data
    assert b"Welcome, testuser!" in dashboard_response.data # Check for welcome message
