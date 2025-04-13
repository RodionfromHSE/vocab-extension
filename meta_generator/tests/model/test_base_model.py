"""Tests for the BaseModel abstract class that defines the interface for text generation models."""
import os
import json
from typing import Dict, Any

import pytest
from unittest.mock import patch, MagicMock

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


@pytest.fixture
def mock_model():
    """Fixture providing a MockModel instance with test config"""
    config = {"api": {"key": "test_key", "model": "test-model"}}
    return MockModel(config), config


def test_base_model_initialization(mock_model):
    """Test that the base model initializes correctly with config"""
    model, config = mock_model
    assert model.config == config


def test_mock_model_generate(mock_model):
    """Test that our mock implementation works as expected"""
    model, _ = mock_model
    prompt = "Hello, world!"
    response = model.generate(prompt)
    assert response == f"Mock response for: {prompt}"
    assert model.call_count == 1


def test_model_with_empty_config():
    """Test handling of empty config"""
    # Empty config
    empty_config = {}
    mock_model = MockModel(empty_config)
    assert mock_model.config == {}


def test_model_with_none_config():
    """Test handling of None config (should raise TypeError)"""
    # None config (should raise TypeError)
    with pytest.raises(TypeError):
        # The BaseModel requires a dict for config
        mock_model = MockModel(None)
