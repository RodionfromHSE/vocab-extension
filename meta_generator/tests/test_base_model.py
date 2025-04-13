import unittest
from unittest.mock import patch, MagicMock
import os
import json
from typing import Dict, Any

from src.model.base_model import BaseModel
from src.model.openai_model import OpenAIModel


class MockModel(BaseModel):
    """Mock implementation of BaseModel for testing"""
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.call_count = 0
    
    def generate(self, prompt: str, **kwargs) -> str:
        self.call_count += 1
        return f"Mock response for: {prompt}"
    
    def validate_config(self) -> bool:
        return True


class TestBaseModel(unittest.TestCase):
    """Test cases for the BaseModel abstract class"""
    
    def setUp(self):
        self.config = {"api": {"key": "test_key", "model": "test-model"}}
        self.mock_model = MockModel(self.config)
    
    def test_base_model_initialization(self):
        """Test that the base model initializes correctly with config"""
        self.assertEqual(self.mock_model.config, self.config)
    
    def test_mock_model_generate(self):
        """Test that our mock implementation works as expected"""
        prompt = "Hello, world!"
        response = self.mock_model.generate(prompt)
        self.assertEqual(response, f"Mock response for: {prompt}")
        self.assertEqual(self.mock_model.call_count, 1)


class TestOpenAIModel(unittest.TestCase):
    """Test cases for the OpenAIModel implementation"""
    
    def setUp(self):
        self.config = {
            "api": {
                "key": "test_key",
                "model": "gpt-3.5-turbo"
            },
            "handler": {
                "max_tokens": 100,
                "temperature": 0.7,
                "timeout": 10
            }
        }
    
    @patch('openai.ChatCompletion.create')
    def test_openai_model_generate(self, mock_create):
        """Test that OpenAIModel.generate makes correct API calls"""
        # Set up the mock response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test response"
        mock_create.return_value = mock_response
        
        # Create model and generate
        model = OpenAIModel(self.config)
        response = model.generate("Test prompt")
        
        # Verify the response
        self.assertEqual(response, "Test response")
        
        # Verify API call
        mock_create.assert_called_once()
        args, kwargs = mock_create.call_args
        self.assertEqual(kwargs['model'], "gpt-3.5-turbo")
        self.assertEqual(kwargs['max_tokens'], 100)
        self.assertEqual(kwargs['temperature'], 0.7)
        self.assertEqual(kwargs['timeout'], 10)
        self.assertEqual(kwargs['messages'], [{"role": "user", "content": "Test prompt"}])
    
    def test_validate_config_no_api_key(self):
        """Test that validate_config fails when no API key is provided"""
        # Create config without API key
        invalid_config = {
            "api": {"model": "gpt-3.5-turbo"}
        }
        
        # Patch setup_client to avoid raising ValueError during initialization
        with patch('src.model.openai_model.OpenAIModel.setup_client'), patch('openai.api_key', None):
            model = OpenAIModel(invalid_config)
            self.assertFalse(model.validate_config())
    
    def test_validate_config_no_model(self):
        """Test that validate_config fails when no model is provided"""
        # Create config without model
        invalid_config = {
            "api": {"key": "test_key"}
        }
        
        with patch('openai.api_key', "test_key"):
            model = OpenAIModel(invalid_config)
            self.assertFalse(model.validate_config())


if __name__ == '__main__':
    unittest.main()