"""Tests for the GenerationHandler component that manages the text generation workflow."""
import json
import time
from typing import Dict, Any, Union

import pytest
from unittest.mock import patch, MagicMock, call

from src.handler.generation_handler import GenerationHandler
from src.model.base_model import BaseModel
from src.prompter.template_prompter import TemplatePrompter
from src.processors.base_processor import BaseProcessor
from src.validators.base_validator import BaseValidator


class MockModel(BaseModel):
    """Mock model for testing"""
    def __init__(self, config, responses=None, fail_count=0):
        super().__init__(config)
        self.responses = responses or ["Mock response"]
        self.call_count = 0
        self.fail_count = fail_count
        self.prompts = []
    
    def generate(self, prompt, **kwargs):
        self.prompts.append(prompt)
        self.call_count += 1
        
        if self.call_count <= self.fail_count:
            raise Exception(f"Mock failure {self.call_count}")
        
        if isinstance(self.responses, list):
            if self.call_count - self.fail_count - 1 < len(self.responses):
                return self.responses[self.call_count - self.fail_count - 1]
            return self.responses[-1]
        return self.responses
    
    def validate_config(self):
        return True


class MockPrompter:
    """Mock prompter for testing"""
    def __init__(self, template="Test template with {word} and {part_of_speech}"):
        self.template = template
        self.format_count = 0
    
    def format_prompt(self, variables):
        self.format_count += 1
        result = self.template
        for key, value in variables.items():
            result = result.replace(f"{{{key}}}", str(value))
        return result


class MockProcessor(BaseProcessor):
    """Mock processor for testing"""
    def __init__(self, config, process_func=None):
        super().__init__(config)
        self.process_func = process_func
        self.call_count = 0
    
    def process(self, response):
        self.call_count += 1
        if self.process_func:
            return self.process_func(response)
        
        # Default behavior: try to parse JSON, fall back to original
        try:
            return json.loads(response)
        except:
            return response


class MockValidator(BaseValidator):
    """Mock validator for testing"""
    def __init__(self, config, validate_func=None):
        super().__init__(config)
        self.validate_func = validate_func
        self.call_count = 0
        self.last_input = None
    
    def validate(self, response):
        self.call_count += 1
        self.last_input = response
        
        if self.validate_func:
            return self.validate_func(response)
        
        # Default behavior: always valid
        return True


@pytest.fixture
def handler_setup():
    """Fixture providing a standard GenerationHandler setup with mocks"""
    config = {
        "handler": {
            "retries": 3,
            "sleep_time": 0.01  # Use small value for tests
        }
    }
    model = MockModel(config)
    prompter = MockPrompter()
    processor = MockProcessor(config)
    validator = MockValidator(config)
    
    handler = GenerationHandler(
        config,
        model,
        prompter,
        processor,
        validator
    )
    
    input_data = {
        "word": "example",
        "part_of_speech": "noun"
    }
    
    return {
        "config": config,
        "model": model,
        "prompter": prompter,
        "processor": processor,
        "validator": validator,
        "handler": handler,
        "input_data": input_data
    }


def test_successful_generation(handler_setup):
    """Test successful generation workflow"""
    # Setup model to return JSON string
    json_response = '{"word": "example", "definition": "a thing"}'
    handler_setup["model"].responses = [json_response]
    
    # Handle generation
    result = handler_setup["handler"].handle(handler_setup["input_data"])
    
    # Verify result
    assert result == {"word": "example", "definition": "a thing"}
    
    # Verify component calls
    assert handler_setup["model"].call_count == 1
    assert handler_setup["prompter"].format_count == 1
    assert handler_setup["processor"].call_count == 1
    assert handler_setup["validator"].call_count == 1
    
    # Verify prompt format
    expected_prompt = "Test template with example and noun"
    assert handler_setup["model"].prompts[0] == expected_prompt


def test_retry_on_failure(handler_setup):
    """Test that handler retries on model failure"""
    # Setup model to fail twice then succeed
    handler_setup["model"].fail_count = 2
    handler_setup["model"].responses = ["Success on third try"]
    
    # Mock sleep to avoid actual delays
    with patch('time.sleep') as mock_sleep:
        result = handler_setup["handler"].handle(handler_setup["input_data"])
    
    # Verify result
    assert result == "Success on third try"
    
    # Verify retry attempts
    assert handler_setup["model"].call_count == 3
    assert mock_sleep.call_count == 2
    
    # Verify validator was only called for successful response
    assert handler_setup["validator"].call_count == 1


def test_processor_error_handling(handler_setup):
    """Test handling of processor errors"""
    # Setup model response
    handler_setup["model"].responses = ['{"invalid": JSON}']  # Invalid JSON to trigger processor error
    
    # Setup processor to always raise an error
    def failing_process(response):
        raise ValueError("Processor error")
    
    handler_setup["processor"].process_func = failing_process
    
    # Mock sleep to avoid delays
    with patch('time.sleep'):
        with pytest.raises(ValueError):
            handler_setup["handler"].handle(handler_setup["input_data"])
    
    # Verify retry attempts
    assert handler_setup["model"].call_count == handler_setup["config"]["handler"]["retries"]


def test_validation_failure(handler_setup):
    """Test handling of validation failures"""
    # Setup validator to fail
    handler_setup["validator"].validate_func = lambda x: False
    
    # Mock sleep to avoid delays
    with patch('time.sleep'):
        with pytest.raises(ValueError):
            handler_setup["handler"].handle(handler_setup["input_data"])
    
    # Verify retry attempts
    assert handler_setup["model"].call_count == handler_setup["config"]["handler"]["retries"]
    assert handler_setup["validator"].call_count == handler_setup["config"]["handler"]["retries"]


def test_no_processor(handler_setup):
    """Test handler behavior when no processor is provided"""
    # Setup handler without processor
    handler = GenerationHandler(
        handler_setup["config"],
        handler_setup["model"],
        handler_setup["prompter"],
        processor=None,
        validator=handler_setup["validator"]
    )
    
    # Setup model to return JSON string
    handler_setup["model"].responses = ['{"word": "example", "definition": "a thing"}']
    
    # Handle generation
    result = handler.handle(handler_setup["input_data"])
    
    # Verify result is parsed even without processor
    assert result == {"word": "example", "definition": "a thing"}


def test_no_validator(handler_setup):
    """Test handler behavior when no validator is provided"""
    # Setup handler without validator
    handler = GenerationHandler(
        handler_setup["config"],
        handler_setup["model"],
        handler_setup["prompter"],
        processor=handler_setup["processor"],
        validator=None
    )
    
    # Setup model response
    handler_setup["model"].responses = ['{"word": "example"}']
    
    # Handle generation
    result = handler.handle(handler_setup["input_data"])
    
    # Verify result
    assert result == {"word": "example"}


def test_non_json_response(handler_setup):
    """Test handling of non-JSON responses"""
    # Setup model to return plain text
    plain_text = "This is not JSON"
    handler_setup["model"].responses = [plain_text]
    
    # Setup processor to pass through text
    handler_setup["processor"].process_func = lambda x: x
    
    # Handle generation
    result = handler_setup["handler"].handle(handler_setup["input_data"])
    
    # Verify result
    assert result == plain_text