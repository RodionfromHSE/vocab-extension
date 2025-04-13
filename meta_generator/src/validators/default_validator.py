"""Default validator implementation that provides basic existence validation."""
from typing import Dict, Any, TypeVar, Union

from src.validators.base_validator import BaseValidator

# Generic type for validated data
T = TypeVar('T')

class DefaultValidator(BaseValidator[T]):
    """
    Default validator implementation providing basic validation.
    
    This validator simply checks if the response exists (is not None).
    """
    
    def validate(self, response: T) -> bool:
        """
        Validate that the response exists.
        
        Args:
            response: The processed response to validate
            
        Returns:
            bool: True if the response is not None, False otherwise
            
        Examples:
            >>> validator = DefaultValidator({})
            >>> validator.validate({"word": "example"})
            True
            >>> validator.validate("text response")
            True
            >>> validator.validate(None)
            False
        """
        return response is not None