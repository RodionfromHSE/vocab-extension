"""Tests for the processors and validators that handle text generation output processing and validation."""
import json
import os
from typing import Dict, Any, Union

import pytest
from unittest.mock import patch, mock_open

from src.processors.codeblock_extractor_processor import CodeBlockExtractorProcessor
from src.validators.json_response_validator import JsonResponseValidator


@pytest.fixture
def processor_setup():
    """Fixture providing a standard CodeBlockExtractorProcessor setup"""
    config = {}
    processor = CodeBlockExtractorProcessor(config, extract_json=True)
    return processor


@pytest.fixture
def validator_setup():
    """Fixture providing a standard JsonResponseValidator setup"""
    config = {
        "validators": {
            "json": {
                "require_schema": False,
                "schema_path": ""
            }
        }
    }
    validator = JsonResponseValidator(config)
    return validator


# Tests for CodeBlockExtractorProcessor
def test_extract_json_codeblock(processor_setup):
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
    
    result = processor_setup.process(response)
    assert result == {"word": "example", "definition": "a thing that illustrates"}


def test_extract_generic_codeblock(processor_setup):
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
    
    result = processor_setup.process(response)
    assert result == {"word": "example", "definition": "a thing that illustrates"}


def test_no_codeblock(processor_setup):
    """Test behavior when no code blocks are present"""
    # Test with no code blocks
    response = """
    {
      "word": "example",
      "definition": "a thing that illustrates"
    }
    """
    
    result = processor_setup.process(response)
    assert result == {"word": "example", "definition": "a thing that illustrates"}


def test_invalid_json(processor_setup):
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
    
    result = processor_setup.process(response)
    # Should return the extracted but invalid JSON string
    assert isinstance(result, str)
    assert "definition: missing quote" in result


def test_extract_without_json_parsing():
    """Test extraction without JSON parsing"""
    # Configure processor to not parse JSON
    config = {}
    processor = CodeBlockExtractorProcessor(config, extract_json=False)
    
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
    assert isinstance(result, str)
    assert '"word": "example"' in result


def test_empty_response(processor_setup):
    """Test handling of empty responses"""
    result = processor_setup.process("")
    assert result == {}


# Tests for JsonResponseValidator
def test_valid_json_dict(validator_setup):
    """Test validation of a valid JSON dictionary"""
    data = {"word": "example", "definition": "a thing"}
    assert validator_setup.validate(data) is True


def test_valid_json_string(validator_setup):
    """Test validation of a valid JSON string"""
    data = '{"word": "example", "definition": "a thing"}'
    assert validator_setup.validate(data) is True


def test_invalid_json_string(validator_setup):
    """Test validation of an invalid JSON string"""
    data = '{"word": "example", "definition: missing quote}'
    assert validator_setup.validate(data) is False


def test_non_json_input(validator_setup):
    """Test validation of non-JSON input"""
    data = "This is not JSON"
    assert validator_setup.validate(data) is False


def test_schema_validation_success():
    """Test schema validation with valid data"""
    config = {
        "validators": {
            "json": {
                "require_schema": False,
                "schema_path": ""
            }
        }
    }
    schema = {
        "type": "object",
        "required": ["word", "definition"],
        "properties": {
            "word": {"type": "string"},
            "definition": {"type": "string"}
        }
    }
    
    validator = JsonResponseValidator(config, schema=schema)
    
    # Valid data according to schema
    data = {"word": "example", "definition": "a thing"}
    assert validator.validate(data) is True


def test_schema_validation_failure():
    """Test schema validation with invalid data"""
    config = {
        "validators": {
            "json": {
                "require_schema": False,
                "schema_path": ""
            }
        }
    }
    schema = {
        "type": "object",
        "required": ["word", "definition"],
        "properties": {
            "word": {"type": "string"},
            "definition": {"type": "string"}
        }
    }
    
    validator = JsonResponseValidator(config, schema=schema)
    
    # Invalid data: missing required field
    data = {"word": "example"}
    assert validator.validate(data) is False
    
    # Invalid data: wrong type
    data = {"word": "example", "definition": 123}
    assert validator.validate(data) is False


@patch("builtins.open", new_callable=mock_open)
@patch("os.path.exists")
def test_schema_loading_from_file(mock_exists, mock_file):
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
    assert validator.validate({"word": "example"}) is True
    assert validator.validate({"not_word": "example"}) is False


def test_is_valid_json_static_method():
    """Test the static is_valid_json method"""
    # Valid JSON
    assert JsonResponseValidator.is_valid_json('{"key": "value"}') is True
    
    # Invalid JSON
    assert JsonResponseValidator.is_valid_json('{"key": value}') is False
    
    # Non-string input
    assert JsonResponseValidator.is_valid_json(123) is False
    assert JsonResponseValidator.is_valid_json(None) is False