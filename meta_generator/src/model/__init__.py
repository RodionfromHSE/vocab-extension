"""Model interface and implementations for text generation APIs."""

import logging
import sys
from typing import Any

from .base_model import BaseModel
from .fireworks_model import FireworksModel
from .nebius_model import NebiusModel
from .openai_model import OpenAIModel

logger = logging.getLogger(__name__)


def _pick_model(config: dict[str, Any]) -> BaseModel:
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

    if api_type == "fireworks":
        return FireworksModel(config)
    elif api_type == "openai":
        return OpenAIModel(config)
    elif api_type == "nebius":
        return NebiusModel(config)
    else:
        supported_types = ["fireworks", "openai", "nebius"]
        raise ValueError(
            f"Unsupported API type '{api_type}'. Supported types: {supported_types}"
        )


def create_model(config: dict[str, Any]) -> BaseModel:
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
        logger.error("Model configuration error: %s", e)
        logger.error("Set 'api.type' to one of: fireworks, openai, nebius")
        sys.exit(1)
    except Exception as e:
        api_type = config.get("api", {}).get("type", "unknown")
        logger.error("Error creating %s model: %s", api_type, e)
        if api_type == "fireworks":
            logger.error("Make sure your FIREWORKS_API_KEY environment variable is set")
        elif api_type == "openai":
            logger.error(
                "Make sure your OPENAI_API_KEY environment variable is set or provided in config"
            )
        elif api_type == "nebius":
            logger.error(
                "Make sure your NEBIUS_API_KEY environment variable is set or provided in config"
            )
        sys.exit(1)


__all__ = [
    "BaseModel",
    "FireworksModel",
    "NebiusModel",
    "OpenAIModel",
    "create_model",
]
