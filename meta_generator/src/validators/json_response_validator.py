import json
import os
import logging
from typing import Dict, Any, Optional, Union
import jsonschema
from jsonschema import validate, ValidationError, Draft7Validator

from src.validators.base_validator import BaseValidator

# Default validator settings (moved from config.yaml)
DEFAULT_REQUIRE_SCHEMA = False
DEFAULT_SCHEMA_PATH = ""


class JsonResponseValidator(BaseValidator[Union[Dict[str, Any], str]]):
    """
    Validator for ensuring responses are valid JSON and optionally conform to a schema.
    
    This validator checks whether processed responses are properly formatted JSON
    and can optionally validate the JSON structure against a provided schema.
    """
    
    def __init__(
        self, 
        config: Dict[str, Any], 
        schema: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize the JSON response validator.
        
        Args:
            config: Dictionary containing configuration parameters
            schema: Optional JSON schema to validate against
        """
        super().__init__(config)
        self.schema = schema
        self.require_schema = config.get("validators", {}).get("json", {}).get("require_schema", DEFAULT_REQUIRE_SCHEMA)
        
        schema_path = config.get("validators", {}).get("json", {}).get("schema_path", DEFAULT_SCHEMA_PATH)
        if not self.schema and schema_path and os.path.exists(schema_path):
            try:
                with open(schema_path, 'r', encoding='utf-8') as file:
                    self.schema = json.load(file)
            except Exception as e:
                logging.error(f"Error loading JSON schema from {schema_path}: {e}")
                if self.require_schema:
                    raise ValueError(f"Required JSON schema could not be loaded: {e}")
    
    def validate(self, response: Union[Dict[str, Any], str]) -> bool:
        """
        Validate that the response is valid JSON and optionally conforms to schema.
        
        This method validates responses in two steps:
        1. Ensures the response is valid JSON (if string) or already a dictionary
        2. If a schema is provided, validates the JSON structure against that schema
        
        Args:
            response: The processed response to validate (dict or string)
            
        Returns:
            bool: True if the response is valid, False otherwise
            
        Examples:
            Basic JSON validation with a dictionary:
            >>> validator = JsonResponseValidator({"validators": {"json": {}}})
            >>> validator.validate({"word": "example", "definition": "a thing"})
            True
            
            Validation with a string containing JSON:
            >>> validator.validate('{"word": "example", "definition": "a thing"}')
            True
            
            Validation with an invalid JSON string:
            >>> validator.validate('{"word": "example", "definition": missing quotes}')
            False
            
            Schema validation - with valid response:
            >>> schema = {
            ...     "type": "object",
            ...     "required": ["word", "definition"],
            ...     "properties": {
            ...         "word": {"type": "string"},
            ...         "definition": {"type": "string"}
            ...     }
            ... }
            >>> validator = JsonResponseValidator({"validators": {"json": {}}}, schema=schema)
            >>> validator.validate({"word": "example", "definition": "a thing"})
            True
            
            Schema validation - with invalid response (missing required field):
            >>> validator.validate({"word": "example"})
            False
        """
        # If response is already a dictionary, we know it's valid JSON
        if isinstance(response, dict):
            json_data = response
        else:
            # If it's a string, try to parse as JSON
            try:
                json_data = json.loads(response)
            except json.JSONDecodeError:
                logging.error("Invalid JSON format")
                return False
        
        # If schema validation is required but no schema is available, fail
        if self.require_schema and not self.schema:
            logging.error("JSON schema validation required but no schema provided")
            return False
        
        # Validate against schema if provided
        if self.schema:
            try:
                validate(instance=json_data, schema=self.schema)
            except ValidationError as e:
                logging.error(f"JSON schema validation failed: {e}")
                return False
        
        return True
    
    @staticmethod
    def is_valid_json(json_str: str) -> bool:
        """
        Simple static method to check if a string is valid JSON.
        
        Args:
            json_str: String to validate as JSON
            
        Returns:
            bool: True if the string is valid JSON, False otherwise
            
        Examples:
            >>> JsonResponseValidator.is_valid_json('{"key": "value"}')
            True
            >>> JsonResponseValidator.is_valid_json('{"key": value}')  # Missing quotes
            False
            >>> JsonResponseValidator.is_valid_json(123)  # Not a string
            False
        """
        if not isinstance(json_str, str):
            return False
            
        try:
            json.loads(json_str)
            return True
        except json.JSONDecodeError:
            return False