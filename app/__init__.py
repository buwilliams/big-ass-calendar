from flask import Flask
from flask_cors import CORS
import os
from app.config import load_config

def create_app(config_path=None):
    """
    Create and configure the Flask application
    
    Args:
        config_path: Optional path to the config.yaml file
        
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
        
        # Configure Google API settings
        app.config["GOOGLE_CLIENT_ID"] = config.get("google", {}).get("client_id")
        app.config["GOOGLE_CLIENT_SECRET"] = config.get("google", {}).get("client_secret")
        
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
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.calendar import calendar_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(calendar_bp)
    
    return app