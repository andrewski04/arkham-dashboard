import pytest
from flask import Flask
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_inmate_threats_logs(client):
    response = client.get('/api/inmate-threats/')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 50
    for item in data:
        assert isinstance(item, dict)
        for key in ["inmate_id", "name", "threat_level", "last_known_location", "incident_flag", "recommendation", "timestamp"]:
            assert key in item
