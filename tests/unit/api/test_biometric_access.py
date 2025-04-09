import pytest
from flask import Flask
from app import create_app  # assuming factory pattern, else import app directly
import json

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_biometric_access_logs(client):
    response = client.get('/api/biometric-access/')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 50
    for item in data:
        assert isinstance(item, dict)
        for key in ["scanner_id", "user_id", "access_result", "reason", "location", "timestamp"]:
            assert key in item
