from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, TypeVar, Generic

# Define a generic type for processor results
T = TypeVar('T')


class BaseProcessor(ABC, Generic[T]):
    """
    Abstract base class for response processing.
    
    This class defines the interface for processors that handle
    post-processing of raw model responses before validation.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the base processor with configuration.
        
        Args:
            config: Dictionary containing configuration parameters
        """
        self.config = config
    
    @abstractmethod
    def process(self, response: str) -> T:
        """
        Process the raw response from the model.
        
        Args:
            response: Raw response string from the model
            
        Returns:
            T: Processed result
            
        Raises:
            Exception: If processing fails
        """
        pass