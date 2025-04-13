import unittest
from unittest.mock import patch, MagicMock, call
import json
import time
from typing import Dict, Any, Union

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


class TestGenerationHandler(unittest.TestCase):
    """Test cases for the GenerationHandler class"""
    
    def setUp(self):
        self.config = {
            "handler": {
                "retries": 3,
                "sleep_time": 0.01  # Use small value for tests
            }
        }
        self.model = MockModel(self.config)
        self.prompter = MockPrompter()
        self.processor = MockProcessor(self.config)
        self.validator = MockValidator(self.config)
        
        self.handler = GenerationHandler(
            self.config,
            self.model,
            self.prompter,
            self.processor,
            self.validator
        )
        
        self.input_data = {
            "word": "example",
            "part_of_speech": "noun"
        }
    
    def test_successful_generation(self):
        """Test successful generation workflow"""
        # Setup model to return JSON string
        json_response = '{"word": "example", "definition": "a thing"}'
        self.model.responses = [json_response]
        
        # Handle generation
        result = self.handler.handle(self.input_data)
        
        # Verify result
        self.assertEqual(result, {"word": "example", "definition": "a thing"})
        
        # Verify component calls
        self.assertEqual(self.model.call_count, 1)
        self.assertEqual(self.prompter.format_count, 1)
        self.assertEqual(self.processor.call_count, 1)
        self.assertEqual(self.validator.call_count, 1)
        
        # Verify prompt format
        expected_prompt = "Test template with example and noun"
        self.assertEqual(self.model.prompts[0], expected_prompt)
    
    def test_retry_on_failure(self):
        """Test that handler retries on model failure"""
        # Setup model to fail twice then succeed
        self.model.fail_count = 2
        self.model.responses = ["Success on third try"]
        
        # Mock sleep to avoid actual delays
        with patch('time.sleep') as mock_sleep:
            result = self.handler.handle(self.input_data)
        
        # Verify result
        self.assertEqual(result, "Success on third try")
        
        # Verify retry attempts
        self.assertEqual(self.model.call_count, 3)
        self.assertEqual(mock_sleep.call_count, 2)
        
        # Verify validator was only called for successful response
        self.assertEqual(self.validator.call_count, 1)
    
    def test_processor_error_handling(self):
        """Test handling of processor errors"""
        # Setup model response
        self.model.responses = ['{"invalid": JSON}']  # Invalid JSON to trigger processor error
        
        # Setup processor to always raise an error
        def failing_process(response):
            raise ValueError("Processor error")
        
        self.processor.process_func = failing_process
        
        # Mock sleep to avoid delays
        with patch('time.sleep'):
            with self.assertRaises(ValueError):
                self.handler.handle(self.input_data)
        
        # Verify retry attempts
        self.assertEqual(self.model.call_count, self.config["handler"]["retries"])
    
    def test_validation_failure(self):
        """Test handling of validation failures"""
        # Setup validator to fail
        self.validator.validate_func = lambda x: False
        
        # Mock sleep to avoid delays
        with patch('time.sleep'):
            with self.assertRaises(ValueError):
                self.handler.handle(self.input_data)
        
        # Verify retry attempts
        self.assertEqual(self.model.call_count, self.config["handler"]["retries"])
        self.assertEqual(self.validator.call_count, self.config["handler"]["retries"])
    
    def test_no_processor(self):
        """Test handler behavior when no processor is provided"""
        # Setup handler without processor
        handler = GenerationHandler(
            self.config,
            self.model,
            self.prompter,
            processor=None,
            validator=self.validator
        )
        
        # Setup model to return JSON string
        self.model.responses = ['{"word": "example", "definition": "a thing"}']
        
        # Handle generation
        result = handler.handle(self.input_data)
        
        # Verify result is parsed even without processor
        self.assertEqual(result, {"word": "example", "definition": "a thing"})
    
    def test_no_validator(self):
        """Test handler behavior when no validator is provided"""
        # Setup handler without validator
        handler = GenerationHandler(
            self.config,
            self.model,
            self.prompter,
            processor=self.processor,
            validator=None
        )
        
        # Setup model response
        self.model.responses = ['{"word": "example"}']
        
        # Handle generation
        result = handler.handle(self.input_data)
        
        # Verify result
        self.assertEqual(result, {"word": "example"})
    
    def test_non_json_response(self):
        """Test handling of non-JSON responses"""
        # Setup model to return plain text
        plain_text = "This is not JSON"
        self.model.responses = [plain_text]
        
        # Setup processor to pass through text
        self.processor.process_func = lambda x: x
        
        # Handle generation
        result = self.handler.handle(self.input_data)
        
        # Verify result
        self.assertEqual(result, plain_text)


if __name__ == "__main__":
    unittest.main()