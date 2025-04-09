import pytest
from flask import Flask
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_network_logs(client):
    response = client.get('/api/network-monitoring/') # Corrected URL prefix
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 50
    for item in data:
        assert isinstance(item, dict)
        for key in ["source_ip", "destination_ip", "protocol", "port", "action", "threat_level", "timestamp"]:
            assert key in item
