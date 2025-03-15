import os
import sys
from app import create_app
import argparse

def main():
    """
    Main entry point for the application
    """
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Run the Big Ass Calendar application')
    parser.add_argument('--config', 
                      help='Path to the configuration YAML file')
    parser.add_argument('--google-client', 
                      help='Path to the Google client JSON credentials file')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Validate config path if provided
    config_path = args.config
    if config_path and not os.path.exists(config_path):
        print(f"Error: Config file not found at {config_path}")
        sys.exit(1)
        
    # Validate Google client path if provided
    google_client_path = args.google_client
    if google_client_path and not os.path.exists(google_client_path):
        print(f"Error: Google client file not found at {google_client_path}")
        sys.exit(1)
    
    # Create the Flask app with optional config paths
    app = create_app(config_path, google_client_path)
    
    # Run the app with debug setting from config
    debug = app.config.get('DEBUG', False)
    app.run(debug=debug)

if __name__ == "__main__":
    main()