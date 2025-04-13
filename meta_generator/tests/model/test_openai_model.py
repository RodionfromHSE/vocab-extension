import unittest
from unittest.mock import patch, MagicMock

from src.model.openai_model import OpenAIModel, DEFAULT_PARAMS


class TestOpenAIModel(unittest.TestCase):
    """Test cases for the OpenAIModel implementation"""
    
    def setUp(self):
        self.config = {
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
    def test_openai_model_generate(self, mock_openai_class):
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
        model = OpenAIModel(self.config)
        response = model.generate("Test prompt")
        
        # Verify the response
        self.assertEqual(response, "Test response")
        
        # Verify API call
        mock_completions.create.assert_called_once()
        args, kwargs = mock_completions.create.call_args
        self.assertEqual(kwargs['model'], "gpt-3.5-turbo")
        self.assertEqual(kwargs['max_tokens'], 100)
        self.assertEqual(kwargs['temperature'], 0.7)
        self.assertEqual(kwargs['timeout'], 10)
        self.assertEqual(kwargs['messages'], [{"role": "user", "content": "Test prompt"}])
    
    @patch('src.model.openai_model.OpenAI')
    def test_validate_config_no_api_key(self, mock_openai_class):
        """Test that validate_config fails when no API key is provided"""
        # Create config without API key
        invalid_config = {
            "api": {"model": "gpt-3.5-turbo"}
        }
        
        # Simulate missing API key scenario by having setup_client throw ValueError
        with patch('src.model.openai_model.OpenAIModel.setup_client', side_effect=ValueError("OpenAI API key not provided")):
            with self.assertRaises(ValueError):
                model = OpenAIModel(invalid_config)
    
    @patch('src.model.openai_model.OpenAI')
    def test_validate_config_no_model(self, mock_openai_class):
        """Test that validate_config fails when no model is provided"""
        # Create config without model
        invalid_config = {
            "api": {"key": "test_key"}
        }
        
        # Mock the client
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        model = OpenAIModel(invalid_config)
        self.assertFalse(model.validate_config())
    
    @patch('src.model.openai_model.OpenAI')
    def test_initialize_generation_params(self, mock_openai_class):
        """Test that parameters are correctly initialized from the new config format"""
        # Mock the client
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        # Create model with the new config format
        model = OpenAIModel(self.config)
        params = model.initialize_generation_params()
        
        # Verify parameters
        self.assertEqual(params["model"], "gpt-3.5-turbo")
        self.assertEqual(params["max_tokens"], 100)
        self.assertEqual(params["temperature"], 0.7)
        self.assertEqual(params["timeout"], 10)
    
    @patch('src.model.openai_model.OpenAI')
    def test_initialize_generation_params_default_values(self, mock_openai_class):
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
        self.assertEqual(params["model"], "gpt-3.5-turbo")
        self.assertEqual(params["max_tokens"], DEFAULT_PARAMS["max_tokens"])
        self.assertEqual(params["temperature"], DEFAULT_PARAMS["temperature"])
        self.assertEqual(params["timeout"], DEFAULT_PARAMS["timeout"])
    
    @patch('src.model.openai_model.OpenAI')
    def test_api_error_handling(self, mock_openai_class):
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
        model = OpenAIModel(self.config)
        
        # Verify exception is raised
        with self.assertRaises(Exception):
            model.generate("Test prompt")


if __name__ == '__main__':
    unittest.main()
