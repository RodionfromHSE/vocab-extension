"""Model interface and implementations for text generation APIs."""

from typing import Dict, Any
import logging
import sys

from .base_model import BaseModel
from .openai_model import OpenAIModel
from .nebius_model import NebiusModel


def _pick_model(config: Dict[str, Any]) -> BaseModel:
    """
    Factory function to create the appropriate model based on configuration.
    
    Args:
        config: Configuration dictionary containing API settings
        
    Returns:
        BaseModel: An instance of the appropriate model class
        
    Raises:
        ValueError: If the API type is not supported
    """
    api_type = config.get("api", {}).get("type", "openai").lower()
    
    if api_type == "openai":
        return OpenAIModel(config)
    elif api_type == "nebius":
        return NebiusModel(config)
    else:
        supported_types = ["openai", "nebius"]
        raise ValueError(f"Unsupported API type '{api_type}'. Supported types: {supported_types}")

def create_model(config: Dict[str, Any]) -> BaseModel:
    """
    Factory function to create the appropriate model based on configuration.
    
    Args:
        config: Configuration dictionary containing API settings
        
    Returns:
        BaseModel: An instance of the appropriate model class
        
    """
    try:
        return _pick_model(config)
    except ValueError as e:
        logging.error(f"Model configuration error: {e}")
        logging.error(f"Make sure 'api.type' in your config is set to either 'openai' or 'nebius'")
        sys.exit(1)
    except Exception as e:
        api_type = config.get("api", {}).get("type", "unknown")
        logging.error(f"Error creating {api_type} model: {e}")
        if api_type == "openai":
            logging.error("Make sure your OPENAI_API_KEY environment variable is set or provided in config")
        elif api_type == "nebius":
            logging.error("Make sure your NEBIUS_API_KEY environment variable is set or provided in config")
        sys.exit(1)


__all__ = ["BaseModel", "OpenAIModel", "NebiusModel", "create_model"]