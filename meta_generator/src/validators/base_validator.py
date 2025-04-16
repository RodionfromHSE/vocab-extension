from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, TypeVar, Generic, Union

# Type for validated data
T = TypeVar('T')


class BaseValidator(ABC, Generic[T]):
    """
    Abstract base class for response validation.
    
    This class defines the interface for validators that ensure
    responses meet required formatting and content criteria.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the base validator with configuration.
        
        Args:
            config: Dictionary containing configuration parameters
        """
        self.config = config
    
    @abstractmethod
    def validate(self, response: T) -> bool:
        """
        Validate the processed response.
        
        Args:
            response: The processed response to validate
            
        Returns:
            bool: True if the response is valid, False otherwise
        """
        pass