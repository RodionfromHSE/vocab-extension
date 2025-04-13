import os
from typing import Dict, Any, Optional, List
import openai
import logging

from src.model.base_model import BaseModel


class OpenAIModel(BaseModel):
    """
    OpenAI-specific model implementation for text generation.
    
    This class implements the BaseModel interface to handle
    text generation using the OpenAI API.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the OpenAI model with configuration.
        
        Args:
            config: Dictionary containing configuration parameters for the model,
                   including API key, model name, and other settings.
        """
        super().__init__(config)
        self.setup_client()
    
    def setup_client(self) -> None:
        """
        Set up the OpenAI client with API key from config.
        
        Raises:
            ValueError: If the API key is not provided
        """
        api_key = self.config.get("api", {}).get("key")
        
        # Use API key from config or environment variable
        if api_key and api_key != "your_openai_api_key":
            openai.api_key = api_key
        else:
            # Try to get API key from environment variable
            api_key = os.environ.get("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OpenAI API key not provided in config or environment variables")
            openai.api_key = api_key
    
    def validate_config(self) -> bool:
        """
        Validate that the configuration has all required parameters.
        
        Returns:
            bool: True if the configuration is valid, False otherwise
        """
        # Check if API key is available
        if not openai.api_key:
            return False
        
        # Check if model name is specified
        model_name = self.config.get("api", {}).get("model")
        if not model_name:
            return False
            
        return True
    
    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate text using the OpenAI API based on the provided prompt.
        
        Args:
            prompt: The input prompt for text generation
            **kwargs: Additional parameters for the OpenAI API call
            
        Returns:
            str: The generated text response
            
        Raises:
            Exception: If the API call fails
        """
        if not self.validate_config():
            raise ValueError("Invalid configuration for OpenAI model")
        
        try:
            model_name = self.config.get("api", {}).get("model", "gpt-3.5-turbo")
            max_tokens = self.config.get("handler", {}).get("max_tokens", 1000)
            temperature = self.config.get("handler", {}).get("temperature", 0.7)
            timeout = self.config.get("handler", {}).get("timeout", 30)
            
            # Override config with kwargs if provided
            model_name = kwargs.get("model", model_name)
            max_tokens = kwargs.get("max_tokens", max_tokens)
            temperature = kwargs.get("temperature", temperature)
            timeout = kwargs.get("timeout", timeout)
            
            # Create message payload for the API call
            messages = [{"role": "user", "content": prompt}]
            
            # Make the API call
            response = openai.ChatCompletion.create(
                model=model_name,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                timeout=timeout
            )
            
            # Extract the generated text from the response
            generated_text = response.choices[0].message.content.strip()
            return generated_text
            
        except Exception as e:
            logging.error(f"Error generating text with OpenAI API: {e}")
            raise Exception(f"OpenAI API error: {str(e)}")