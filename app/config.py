import os
import yaml
import json
from typing import Dict, Any, Optional, Tuple

def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Load configuration from a YAML file.
    
    Args:
        config_path: Path to the config.yaml file. If None, will look in the 
                     project root directory.
    
    Returns:
        Dict containing configuration values
    
    Raises:
        FileNotFoundError: If the config file doesn't exist
    """
    if config_path is None:
        # Default to looking in the project root
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(base_dir, 'config.yaml')
    
    if not os.path.exists(config_path):
        raise FileNotFoundError(
            f"Configuration file not found at {config_path}. "
            f"Please create one based on config_sample.yaml"
        )
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    return config

def load_google_client(file_path: Optional[str] = None) -> Tuple[Dict[str, Any], bool]:
    """
    Load Google client configuration from JSON file.
    
    Args:
        file_path: Path to the google_client.json file. If None, will look
                  in the project root directory.
    
    Returns:
        Tuple of (client_config, from_file)
        - client_config: Dict containing Google client configuration
        - from_file: Boolean indicating if config was loaded from file
    """
    if file_path is None:
        # Default to looking in the project root
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(base_dir, 'google_client.json')
    
    # If the file exists, load it
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f), True
    
    # Return an empty config if file doesn't exist
    return {"web": {}}, False