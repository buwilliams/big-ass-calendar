import os
import sys
from app import create_app

def main():
    """
    Main entry point for the application
    """
    # Check for custom config path from command line
    config_path = None
    if len(sys.argv) > 1:
        config_arg = sys.argv[1]
        if config_arg.startswith('--config='):
            config_path = config_arg.split('=')[1]
            # Validate that the file exists
            if not os.path.exists(config_path):
                print(f"Error: Config file not found at {config_path}")
                sys.exit(1)
    
    # Create the Flask app with optional config path
    app = create_app(config_path)
    
    # Run the app with debug setting from config
    debug = app.config.get('DEBUG', False)
    app.run(debug=debug)

if __name__ == "__main__":
    main()