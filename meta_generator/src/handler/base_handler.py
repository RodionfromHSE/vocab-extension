from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, Callable, TypeVar, Generic

# Define a generic type for processor and validator results
T = TypeVar('T')


class BaseHandler(ABC, Generic[T]):
    """
    Abstract base class for handling text generation workflows.
    
    This class defines the interface for handlers that orchestrate
    text generation, error handling, retries, and post-processing.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the base handler with configuration.
        
        Args:
            config: Dictionary containing configuration parameters
        """
        self.config = config
        self.retries = config.get("handler", {}).get("retries", 3)
        self.sleep_time = config.get("handler", {}).get("sleep_time", 2)
    
    @abstractmethod
    def handle(self, input_data: Dict[str, Any], **kwargs) -> T:
        """
        Handle the generation workflow with input data.
        
        Args:
            input_data: Input data for the generation
            **kwargs: Additional parameters for handling
            
        Returns:
            T: The processed and validated result
            
        Raises:
            Exception: If handling fails
        """
        pass
    
    @abstractmethod
    def _process_response(self, response: str) -> T:
        """
        Process the raw response from the model.
        
        Args:
            response: Raw response string from the model
            
        Returns:
            T: Processed response
        """
        pass
    
    @abstractmethod
    def _validate_response(self, processed_response: T) -> bool:
        """
        Validate the processed response.
        
        Args:
            processed_response: The processed response to validate
            
        Returns:
            bool: True if the response is valid, False otherwise
        """
        pass