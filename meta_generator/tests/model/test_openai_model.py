"""Tests for the OpenAIModel implementation that provides OpenAI API integration."""
import pytest
from unittest.mock import patch, MagicMock

from src.model.openai_model import OpenAIModel, DEFAULT_PARAMS


@pytest.fixture
def test_config():
    """Test configuration for OpenAIModel tests"""
    return {
        "api": {
            "key": "test_key",
            "model": "gpt-3.5-turbo",
            "params": {
                "max_tokens": 100,
                "temperature": 0.7,
                "timeout": 10
            }
        }
    }


@patch('src.model.openai_model.OpenAI')
def test_openai_model_generate(mock_openai_class, test_config):
    """Test that OpenAIModel.generate makes correct API calls"""
    # Set up the mock response
    mock_client = MagicMock()
    mock_openai_class.return_value = mock_client
    
    mock_chat = MagicMock()
    mock_client.chat = mock_chat
    
    mock_completions = MagicMock()
    mock_chat.completions = mock_completions
    
    mock_response = MagicMock()
    mock_completions.create.return_value = mock_response
    
    mock_choice = MagicMock()
    mock_response.choices = [mock_choice]
    
    mock_choice.message.content = "Test response"
    
    # Create model and generate
    model = OpenAIModel(test_config)
    response = model.generate("Test prompt")
    
    # Verify the response
    assert response == "Test response"
    
    # Verify API call
    mock_completions.create.assert_called_once()
    args, kwargs = mock_completions.create.call_args
    assert kwargs['model'] == "gpt-3.5-turbo"
    assert kwargs['max_tokens'] == 100
    assert kwargs['temperature'] == 0.7
    assert kwargs['timeout'] == 10
    assert kwargs['messages'] == [{"role": "user", "content": "Test prompt"}]


@patch('src.model.openai_model.OpenAI')
def test_validate_config_no_api_key(mock_openai_class):
    """Test that validate_config fails when no API key is provided"""
    # Create config without API key
    invalid_config = {
        "api": {"model": "gpt-3.5-turbo"}
    }
    
    # Simulate missing API key scenario by having setup_client throw ValueError
    with patch('src.model.openai_model.OpenAIModel.setup_client', side_effect=ValueError("OpenAI API key not provided")):
        with pytest.raises(ValueError):
            model = OpenAIModel(invalid_config)


@patch('src.model.openai_model.OpenAI')
def test_validate_config_no_model(mock_openai_class):
    """Test that validate_config fails when no model is provided"""
    # Create config without model
    invalid_config = {
        "api": {"key": "test_key"}
    }
    
    # Mock the client
    mock_client = MagicMock()
    mock_openai_class.return_value = mock_client
    
    model = OpenAIModel(invalid_config)
    assert model.validate_config() is False


@patch('src.model.openai_model.OpenAI')
def test_initialize_generation_params(mock_openai_class, test_config):
    """Test that parameters are correctly initialized from the new config format"""
    # Mock the client
    mock_client = MagicMock()
    mock_openai_class.return_value = mock_client
    
    # Create model with the new config format
    model = OpenAIModel(test_config)
    params = model.initialize_generation_params()
    
    # Verify parameters
    assert params["model"] == "gpt-3.5-turbo"
    assert params["max_tokens"] == 100
    assert params["temperature"] == 0.7
    assert params["timeout"] == 10


@patch('src.model.openai_model.OpenAI')
def test_initialize_generation_params_default_values(mock_openai_class):
    """Test that default parameters are used when not specified in config"""
    # Mock the client
    mock_client = MagicMock()
    mock_openai_class.return_value = mock_client
    
    # Create minimal config
    minimal_config = {
        "api": {
            "key": "test_key",
            "model": "gpt-3.5-turbo"
        }
    }
    
    model = OpenAIModel(minimal_config)
    params = model.initialize_generation_params()
    
    # Verify default parameters are used
    assert params["model"] == "gpt-3.5-turbo"
    assert params["max_tokens"] == DEFAULT_PARAMS["max_tokens"]
    assert params["temperature"] == DEFAULT_PARAMS["temperature"]
    assert params["timeout"] == DEFAULT_PARAMS["timeout"]


@patch('src.model.openai_model.OpenAI')
def test_api_error_handling(mock_openai_class, test_config):
    """Test that API errors are properly caught and raised"""
    # Mock the client
    mock_client = MagicMock()
    mock_openai_class.return_value = mock_client
    
    # Set up mock completions to raise an exception
    mock_chat = MagicMock()
    mock_client.chat = mock_chat
    
    mock_completions = MagicMock()
    mock_chat.completions = mock_completions
    
    mock_completions.create.side_effect = Exception("API Error")
    
    # Create model
    model = OpenAIModel(test_config)
    
    # Verify exception is raised
    with pytest.raises(Exception):
        model.generate("Test prompt")
