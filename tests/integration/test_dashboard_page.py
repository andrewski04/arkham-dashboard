import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_dashboard_page_loads(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Dashboard" in response.data or b"dashboard" in response.data
