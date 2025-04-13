import os
from typing import Dict, Any
from openai import OpenAI
import logging

from src.model.base_model import BaseModel

# Global variable for default parameters
DEFAULT_PARAMS = {
    "model": "gpt-3.5-turbo",
    "max_tokens": 1000,  # Increased from 100 to 1000 to allow for complete responses
    "temperature": 0.7,
    "timeout": 30,
}


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
        self.client = self.setup_client()
        self.generation_params = self.initialize_generation_params()
    
    def setup_client(self) -> OpenAI:
        """
        Set up the OpenAI client with API key from config.
        
        Returns:
            OpenAI: The initialized OpenAI client
        
        Raises:
            ValueError: If the API key is not provided
        """
        api_key = self.config.get("api", {}).get("key")
        
        # Use API key from config or environment variable
        if api_key and api_key != "your_openai_api_key":
            client = OpenAI(api_key=api_key)
        else:
            # Try to get API key from environment variable
            api_key = os.environ.get("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OpenAI API key not provided in config or environment variables")
            client = OpenAI(api_key=api_key)
        
        return client
    
    def initialize_generation_params(self) -> Dict[str, Any]:
        """
        Initialize generation parameters from the configuration or use defaults.
        
        Returns:
            Dict[str, Any]: A dictionary of generation parameters.
        """
        params = DEFAULT_PARAMS.copy()
        
        # Get API section and its params subsection
        api_config = self.config.get("api", {})
        api_params = api_config.get("params", {})
        
        # Override default parameters with config values if provided
        params["model"] = api_config.get("model", params["model"])
        params["max_tokens"] = api_params.get("max_tokens", params["max_tokens"])
        params["temperature"] = api_params.get("temperature", params["temperature"])
        params["timeout"] = api_params.get("timeout", params["timeout"])
        
        return params
    
    def validate_config(self) -> bool:
        """
        Validate that the configuration has all required parameters.
        
        Returns:
            bool: True if the configuration is valid, False otherwise
        """
        # Check if API key is available (client was created successfully)
        if not hasattr(self, 'client'):
            return False
        
        # Check if model name is specified
        model_name = self.config.get("api", {}).get("model")
        if not model_name:
            return False
            
        return True
    
    def generate(self, prompt: str) -> str:
        """
        Generate text using the OpenAI API based on the provided prompt.
        
        Args:
            prompt: The input prompt for text generation
            
        Returns:
            str: The generated text response
            
        Raises:
            Exception: If the API call fails
        """
        if not self.validate_config():
            raise ValueError("Invalid configuration for OpenAI model")
        
        try:
            # Create message payload for the API call
            messages = [{"role": "user", "content": prompt}]
            
            # Make the API call using the new client API
            response = self.client.chat.completions.create(
                model=self.generation_params["model"],
                messages=messages,
                max_tokens=self.generation_params["max_tokens"],
                temperature=self.generation_params["temperature"],
                timeout=self.generation_params["timeout"]
            )
            
            # Extract the generated text from the response
            generated_text = response.choices[0].message.content.strip()
            return generated_text
            
        except Exception as e:
            logging.error(f"Error generating text with OpenAI API: {e}")
            raise Exception(f"OpenAI API error: {str(e)}")