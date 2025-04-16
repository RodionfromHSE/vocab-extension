"""Default processor implementation that provides basic JSON parsing functionality."""
import json
from typing import Dict, Any, Union

from src.processors.base_processor import BaseProcessor


class DefaultProcessor(BaseProcessor[Union[Dict[str, Any], str]]):
    """
    Default processor implementation for handling raw text responses.
    
    This processor attempts to parse responses as JSON, falling back to 
    returning the original string if JSON parsing fails.
    """
    
    def process(self, response: str) -> Union[Dict[str, Any], str]:
        """
        Process the raw response by attempting to parse it as JSON.
        
        Args:
            response: Raw response string from the model
            
        Returns:
            Union[Dict[str, Any], str]: JSON object if parsing succeeds,
                                       otherwise the original string
            
        Raises:
            ValueError: If the response is empty
            
        Examples:
            >>> processor = DefaultProcessor({})
            >>> processor.process('{"word": "example", "definition": "a thing"}')
            {'word': 'example', 'definition': 'a thing'}
            
            >>> processor.process('This is not JSON')
            'This is not JSON'
            
            >>> processor.process('')
            Traceback (most recent call last):
                ...
            ValueError: Empty response from model
        """
        if not response:
            raise ValueError("Empty response from model")
            
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            # If not JSON, return as string
            return response