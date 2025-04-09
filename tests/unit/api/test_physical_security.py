import pytest
from flask import Flask
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_physical_security_logs(client):
    response = client.get('/api/physical-security/')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 50
    for item in data:
        assert isinstance(item, dict)
        for key in ["system", "location", "status", "trigger_reason", "timestamp"]:
            assert key in item
