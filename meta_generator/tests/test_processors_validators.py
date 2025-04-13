import unittest
from unittest.mock import patch, mock_open
import json
import os
from typing import Dict, Any, Union

from src.processors.codeblock_extractor_processor import CodeBlockExtractorProcessor
from src.validators.json_response_validator import JsonResponseValidator


class TestCodeBlockExtractorProcessor(unittest.TestCase):
    """Test cases for the CodeBlockExtractorProcessor class"""
    
    def setUp(self):
        self.config = {}
        self.processor = CodeBlockExtractorProcessor(self.config, extract_json=True)
        
    def test_extract_json_codeblock(self):
        """Test extracting JSON from code blocks"""
        # Test with ```json code block
        response = """
        Here is some explanation:
        
        ```json
        {
          "word": "example",
          "definition": "a thing that illustrates"
        }
        ```
        
        Hope that helps!
        """
        
        result = self.processor.process(response)
        self.assertEqual(result, {"word": "example", "definition": "a thing that illustrates"})
        
    def test_extract_generic_codeblock(self):
        """Test extracting content from generic code blocks"""
        # Test with generic ``` code block
        response = """
        Here is the output:
        
        ```
        {
          "word": "example",
          "definition": "a thing that illustrates"
        }
        ```
        """
        
        result = self.processor.process(response)
        self.assertEqual(result, {"word": "example", "definition": "a thing that illustrates"})
        
    def test_no_codeblock(self):
        """Test behavior when no code blocks are present"""
        # Test with no code blocks
        response = """
        {
          "word": "example",
          "definition": "a thing that illustrates"
        }
        """
        
        result = self.processor.process(response)
        self.assertEqual(result, {"word": "example", "definition": "a thing that illustrates"})
        
    def test_invalid_json(self):
        """Test handling of invalid JSON content"""
        # Test with invalid JSON
        response = """
        ```json
        {
          "word": "example",
          "definition: missing quote
        }
        ```
        """
        
        result = self.processor.process(response)
        # Should return the extracted but invalid JSON string
        self.assertIsInstance(result, str)
        self.assertIn("definition: missing quote", result)
        
    def test_extract_without_json_parsing(self):
        """Test extraction without JSON parsing"""
        # Configure processor to not parse JSON
        processor = CodeBlockExtractorProcessor(self.config, extract_json=False)
        
        response = """
        ```json
        {
          "word": "example",
          "definition": "a thing that illustrates"
        }
        ```
        """
        
        result = processor.process(response)
        # Should return the raw extracted string
        self.assertIsInstance(result, str)
        self.assertIn('"word": "example"', result)
        
    def test_empty_response(self):
        """Test handling of empty responses"""
        result = self.processor.process("")
        self.assertEqual(result, {})


class TestJsonResponseValidator(unittest.TestCase):
    """Test cases for the JsonResponseValidator class"""
    
    def setUp(self):
        self.config = {
            "validators": {
                "json": {
                    "require_schema": False,
                    "schema_path": ""
                }
            }
        }
        self.validator = JsonResponseValidator(self.config)
        
    def test_valid_json_dict(self):
        """Test validation of a valid JSON dictionary"""
        data = {"word": "example", "definition": "a thing"}
        self.assertTrue(self.validator.validate(data))
        
    def test_valid_json_string(self):
        """Test validation of a valid JSON string"""
        data = '{"word": "example", "definition": "a thing"}'
        self.assertTrue(self.validator.validate(data))
        
    def test_invalid_json_string(self):
        """Test validation of an invalid JSON string"""
        data = '{"word": "example", "definition: missing quote}'
        self.assertFalse(self.validator.validate(data))
        
    def test_non_json_input(self):
        """Test validation of non-JSON input"""
        data = "This is not JSON"
        self.assertFalse(self.validator.validate(data))
        
    def test_schema_validation_success(self):
        """Test schema validation with valid data"""
        schema = {
            "type": "object",
            "required": ["word", "definition"],
            "properties": {
                "word": {"type": "string"},
                "definition": {"type": "string"}
            }
        }
        
        validator = JsonResponseValidator(self.config, schema=schema)
        
        # Valid data according to schema
        data = {"word": "example", "definition": "a thing"}
        self.assertTrue(validator.validate(data))
        
    def test_schema_validation_failure(self):
        """Test schema validation with invalid data"""
        schema = {
            "type": "object",
            "required": ["word", "definition"],
            "properties": {
                "word": {"type": "string"},
                "definition": {"type": "string"}
            }
        }
        
        validator = JsonResponseValidator(self.config, schema=schema)
        
        # Invalid data: missing required field
        data = {"word": "example"}
        self.assertFalse(validator.validate(data))
        
        # Invalid data: wrong type
        data = {"word": "example", "definition": 123}
        self.assertFalse(validator.validate(data))
        
    @patch("builtins.open", new_callable=mock_open)
    @patch("os.path.exists")
    def test_schema_loading_from_file(self, mock_exists, mock_file):
        """Test loading schema from a file"""
        # Setup config with schema path
        config = {
            "validators": {
                "json": {
                    "require_schema": True,
                    "schema_path": "schema.json"
                }
            }
        }
        
        # Mock schema file
        schema_json = """
        {
            "type": "object",
            "required": ["word"],
            "properties": {
                "word": {"type": "string"}
            }
        }
        """
        mock_exists.return_value = True
        mock_file.return_value.read.return_value = schema_json
        
        # Create validator that loads schema from file
        validator = JsonResponseValidator(config)
        
        # Test validation
        self.assertTrue(validator.validate({"word": "example"}))
        self.assertFalse(validator.validate({"not_word": "example"}))
        
    def test_is_valid_json_static_method(self):
        """Test the static is_valid_json method"""
        # Valid JSON
        self.assertTrue(JsonResponseValidator.is_valid_json('{"key": "value"}'))
        
        # Invalid JSON
        self.assertFalse(JsonResponseValidator.is_valid_json('{"key": value}'))
        
        # Non-string input
        self.assertFalse(JsonResponseValidator.is_valid_json(123))
        self.assertFalse(JsonResponseValidator.is_valid_json(None))


if __name__ == "__main__":
    unittest.main()