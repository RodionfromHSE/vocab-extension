from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class BaseModel(ABC):
    """
    Abstract base class for text generation models.
    
    This class defines the interface for text generation, allowing for 
    different model implementations (e.g., OpenAI, local models, etc.)
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the base model with configuration.
        
        Args:
            config: Dictionary containing configuration parameters for the model
            
        Raises:
            TypeError: If config is not a dictionary
        """
        if not isinstance(config, dict):
            raise TypeError("Config must be a dictionary")
        self.config = config
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate text based on the provided prompt.
        
        Args:
            prompt: The input prompt for text generation
            **kwargs: Additional parameters specific to the model implementation
            
        Returns:
            str: The generated text response
            
        Raises:
            Exception: If the text generation fails
        """
        pass
    
    @abstractmethod
    def validate_config(self) -> bool:
        """
        Validate that the configuration has all required parameters.
        
        Returns:
            bool: True if the configuration is valid, False otherwise
        """
        pass