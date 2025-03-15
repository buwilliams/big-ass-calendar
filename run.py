import os
import sys
import logging
from app import create_app
import argparse

# Configure logging for OAuth debugging
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # Allow OAuth over HTTP for development
logging.basicConfig(level=logging.INFO)
logging.getLogger('oauthlib').setLevel(logging.DEBUG)
logging.getLogger('google.auth.transport.requests').setLevel(logging.DEBUG)

def print_app_info():
    """Print information about the Big Ass Calendar application"""
    print("\nBig Ass Calendar Application")
    print("===========================")
    print("\nA year-at-a-glance calendar with Google Calendar integration")
    print("\nOptions:")
    print("  Run with default settings:      python run.py")
    print("  Show detailed help:             python run.py --help")
    print("  Custom config file:             python run.py --config=path/to/config.yaml")
    print("  Custom Google credentials:      python run.py --google-client=path/to/credentials.json")
    print("  Both custom configs:            python run.py --config=path/to/config.yaml --google-client=path/to/credentials.json")
    print("\nDefault behavior will look for:")
    print("  - config.yaml in the current directory")
    print("  - google_client.json in the current directory")
    print("\nSee README.md for detailed setup instructions.")

def main():
    """
    Main entry point for the application
    """
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(
        description='Run the Big Ass Calendar application',
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument('--config', 
                      help='Path to the configuration YAML file\n'
                           'Default: ./config.yaml')
    parser.add_argument('--google-client', 
                      help='Path to the Google client JSON credentials file\n'
                           'Default: ./google_client.json')
    parser.add_argument('--info', action='store_true',
                      help='Show application information and exit')
    
    # Parse arguments
    args = parser.parse_args()
    
    # If --info flag is provided, show app info and exit
    if args.info:
        print_app_info()
        sys.exit(0)
    
    # Always show basic app info 
    print("Big Ass Calendar Application")
    print("Run with --info for more details about configuration options")
    print("Run with --help for command-line argument help")
    
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
    
    # Show where the app is running
    print(f"\nRunning on http://127.0.0.1:5000 (Press CTRL+C to quit)")
    print(f"Debug mode: {'on' if debug else 'off'}")
    
    app.run(debug=debug)

if __name__ == "__main__":
    main()