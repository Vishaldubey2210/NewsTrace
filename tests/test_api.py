"""Integration tests for NewsTrace Flask REST endpoints."""
import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_endpoint(client):
    res = client.get('/api/health')
    assert res.status_code == 200

def test_home_page(client):
    res = client.get('/')
    assert res.status_code in [200, 302]
