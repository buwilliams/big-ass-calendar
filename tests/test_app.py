import pytest
import os
import yaml
import tempfile
from app import create_app
from flask import session

@pytest.fixture
def test_config():
    """Create a temporary test configuration file"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        config = {
            "flask": {
                "secret_key": "test-key",
                "debug": False
            },
            "google": {
                "client_id": "test-client-id",
                "client_secret": "test-client-secret"
            },
            "app": {
                "title": "Test Calendar",
                "default_year": 2025
            }
        }
        yaml.dump(config, f)
        config_path = f.name
    
    yield config_path
    
    # Clean up the temporary file
    os.unlink(config_path)

@pytest.fixture
def app(test_config):
    app = create_app(test_config)
    app.config.update({
        "TESTING": True,
    })
    
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_index_route(client):
    response = client.get("/")
    assert response.status_code == 200
    
def test_app_config(client):
    response = client.get("/api/config")
    assert response.status_code == 200
    data = response.get_json()
    assert "title" in data
    assert "defaultYear" in data
    assert data["title"] == "Test Calendar"
    assert data["defaultYear"] == 2025
    
def test_check_auth_unauthenticated(client):
    response = client.get("/check-auth")
    assert response.status_code == 200
    data = response.get_json()
    assert data["authenticated"] is False
    
def test_login_redirect(client):
    response = client.get("/login")
    assert response.status_code == 302  # Redirect to Google OAuth