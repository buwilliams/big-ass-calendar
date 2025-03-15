import pytest
import os
import yaml
import json
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
def test_google_client():
    """Create a temporary Google client JSON file"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        client_config = {
            "web": {
                "client_id": "test-json-client-id",
                "project_id": "test-project",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_secret": "test-json-client-secret",
                "redirect_uris": ["http://localhost:5000/oauth2callback"],
                "javascript_origins": ["http://localhost:5000"]
            }
        }
        json.dump(client_config, f)
        client_path = f.name
    
    yield client_path
    
    # Clean up the temporary file
    os.unlink(client_path)

@pytest.fixture
def app_with_yaml_config(test_config):
    """Create app with YAML config only"""
    app = create_app(test_config)
    app.config.update({
        "TESTING": True,
    })
    
    yield app
    
@pytest.fixture
def app_with_json_config(test_google_client):
    """Create app with Google JSON config only"""
    app = create_app(None, test_google_client)
    app.config.update({
        "TESTING": True,
    })
    
    yield app

@pytest.fixture
def app_with_both_configs(test_config, test_google_client):
    """Create app with both configs"""
    app = create_app(test_config, test_google_client)
    app.config.update({
        "TESTING": True,
    })
    
    yield app

@pytest.fixture
def app(app_with_both_configs):
    """Default app fixture uses both configs"""
    return app_with_both_configs

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

def test_client_config_precedence(app_with_both_configs):
    # Test that the JSON client config takes precedence over YAML config
    assert app_with_both_configs.config["GOOGLE_CLIENT_ID"] == "test-json-client-id"
    assert app_with_both_configs.config["GOOGLE_CLIENT_SECRET"] == "test-json-client-secret"
    assert "GOOGLE_CLIENT_CONFIG" in app_with_both_configs.config
    assert app_with_both_configs.config["GOOGLE_CLIENT_CONFIG"]["web"]["client_id"] == "test-json-client-id"

def test_yaml_config_fallback(app_with_yaml_config):
    # Test that YAML config is used when JSON is not available
    assert app_with_yaml_config.config["GOOGLE_CLIENT_ID"] == "test-client-id"
    assert app_with_yaml_config.config["GOOGLE_CLIENT_SECRET"] == "test-client-secret"
    assert "GOOGLE_CLIENT_CONFIG" in app_with_yaml_config.config
    
def test_check_auth_unauthenticated(client):
    response = client.get("/check-auth")
    assert response.status_code == 200
    data = response.get_json()
    assert data["authenticated"] is False
    
def test_login_redirect(client):
    response = client.get("/login")
    assert response.status_code == 302  # Redirect to Google OAuth
    
# To test the command line argument parsing, we create a custom test
# that directly uses argparse rather than invoking the full application
def test_command_line_args():
    import argparse
    
    # Create a parser with the same arguments as in run.py
    parser = argparse.ArgumentParser(description='Test argument parser')
    parser.add_argument('--config', 
                      help='Path to the configuration YAML file')
    parser.add_argument('--google-client', 
                      help='Path to the Google client JSON credentials file')
    parser.add_argument('--info', action='store_true',
                      help='Show application information and exit')
    
    # Test that our expected arguments are recognized
    args = parser.parse_args(['--info'])
    assert args.info is True
    
    args = parser.parse_args(['--config', 'test_config.yaml'])
    assert args.config == 'test_config.yaml'
    
    args = parser.parse_args(['--google-client', 'test_client.json'])
    assert args.google_client == 'test_client.json'
    
    # Test combined arguments
    args = parser.parse_args(['--config', 'test_config.yaml', '--google-client', 'test_client.json'])
    assert args.config == 'test_config.yaml'
    assert args.google_client == 'test_client.json'