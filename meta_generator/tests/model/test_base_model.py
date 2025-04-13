import unittest
from unittest.mock import patch, MagicMock
import os
import json
from typing import Dict, Any

from src.model.base_model import BaseModel


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
    
    def test_model_without_config(self):
        """Test handling of empty or invalid config"""
        # Empty config
        empty_config = {}
        mock_model = MockModel(empty_config)
        self.assertEqual(mock_model.config, {})
        
        # None config (should default to empty dict)
        with self.assertRaises(TypeError):
            # The BaseModel requires a dict for config
            mock_model = MockModel(None)


if __name__ == '__main__':
    unittest.main()
