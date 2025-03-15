from flask import Flask
from flask_cors import CORS
import os
from app.config import load_config, load_google_client

# Allow OAuth to work in development environment
if os.environ.get('FLASK_ENV') == 'development' or os.environ.get('DEBUG'):
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

def create_app(config_path=None, google_client_path=None):
    """
    Create and configure the Flask application
    
    Args:
        config_path: Optional path to the config.yaml file
        google_client_path: Optional path to the google_client.json file
        
    Returns:
        Configured Flask application
    """
    app = Flask(__name__)
    CORS(app)
    
    # Load configuration from YAML file
    try:
        config = load_config(config_path)
        
        # Configure Flask
        app.config["SECRET_KEY"] = config.get("flask", {}).get(
            "secret_key", "dev-key-change-in-production"
        )
        app.config["DEBUG"] = config.get("flask", {}).get("debug", False)
        
        # Configure app settings
        app.config["APP_TITLE"] = config.get("app", {}).get("title", "The Big A$$ Calendar")
        app.config["DEFAULT_YEAR"] = config.get("app", {}).get("default_year", 2025)
        
    except FileNotFoundError as e:
        app.logger.warning(f"Configuration error: {e}")
        app.logger.warning("Using default configuration values")
        
        # Set default values if config file is not found
        app.config["SECRET_KEY"] = "dev-key-change-in-production"
        app.config["DEBUG"] = True
        app.config["APP_TITLE"] = "The Big A$$ Calendar"
        app.config["DEFAULT_YEAR"] = 2025
    
    # Load Google client configuration
    google_client_config, from_file = load_google_client(google_client_path)
    
    if from_file:
        app.logger.info("Using Google client configuration from google_client.json")
        app.config["GOOGLE_CLIENT_CONFIG"] = google_client_config
        
        # For backwards compatibility, also set individual keys
        if "web" in google_client_config:
            app.config["GOOGLE_CLIENT_ID"] = google_client_config["web"].get("client_id")
            app.config["GOOGLE_CLIENT_SECRET"] = google_client_config["web"].get("client_secret")
    else:
        app.logger.info("Google client JSON file not found, using config from YAML")
        # Use Google config from YAML if JSON file wasn't found
        app.config["GOOGLE_CLIENT_ID"] = config.get("google", {}).get("client_id")
        app.config["GOOGLE_CLIENT_SECRET"] = config.get("google", {}).get("client_secret")
        
        # Create a minimal client config for auth routes
        app.config["GOOGLE_CLIENT_CONFIG"] = {
            "web": {
                "client_id": app.config["GOOGLE_CLIENT_ID"],
                "client_secret": app.config["GOOGLE_CLIENT_SECRET"],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        }
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.calendar import calendar_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(calendar_bp)
    
    return app