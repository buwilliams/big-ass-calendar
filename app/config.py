import os
import yaml
from typing import Dict, Any, Optional

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