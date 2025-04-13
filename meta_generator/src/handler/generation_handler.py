import time
import logging
from typing import Dict, Any, Optional, List, Union, TypeVar, Generic
import json

from src.handler.base_handler import BaseHandler
from src.model.base_model import BaseModel
from src.prompter.template_prompter import TemplatePrompter
from src.processors.base_processor import BaseProcessor
from src.validators.base_validator import BaseValidator

# Type for processed data - typically a dictionary (JSON) or string
T = TypeVar('T', Dict[str, Any], str)


class GenerationHandler(BaseHandler[T]):
    """
    Handler for text generation workflows.
    
    This class implements the BaseHandler interface to orchestrate
    the entire text generation process, including prompting, model calling,
    response processing, validation, and error handling.
    """
    
    def __init__(
        self,
        config: Dict[str, Any],
        model: BaseModel,
        prompter: TemplatePrompter,
        processor: Optional[BaseProcessor] = None,
        validator: Optional[BaseValidator] = None
    ):
        """
        Initialize the generation handler with components.
        
        Args:
            config: Dictionary containing configuration parameters
            model: The text generation model to use
            prompter: The prompter for formatting input prompts
            processor: Optional processor for post-processing responses
            validator: Optional validator for validating processed responses
        """
        super().__init__(config)
        self.model = model
        self.prompter = prompter
        self.processor = processor
        self.validator = validator
        
    def handle(self, input_data: Dict[str, Any], **kwargs) -> T:
        """
        Handle the generation workflow with input data.
        
        Args:
            input_data: Input data for the generation (e.g., word, part_of_speech)
            **kwargs: Additional parameters for handling
            
        Returns:
            T: The processed and validated result
            
        Raises:
            Exception: If handling fails after all retries
        """
        # Format the prompt template with input data
        formatted_prompt = self.prompter.format_prompt(input_data)
        
        # Try to generate with retries
        attempt = 0
        last_error = None
        
        while attempt < self.retries:
            try:
                # Call the model to generate text
                response = self.model.generate(formatted_prompt, **kwargs)
                
                # Process the response
                processed_response = self._process_response(response)
                
                # Validate the processed response if a validator is available
                if self.validator and not self._validate_response(processed_response):
                    raise ValueError(f"Invalid response: {processed_response}")
                
                return processed_response
                
            except Exception as e:
                attempt += 1
                last_error = e
                logging.warning(f"Generation attempt {attempt} failed: {e}")
                
                if attempt < self.retries:
                    logging.info(f"Retrying in {self.sleep_time} seconds...")
                    time.sleep(self.sleep_time)
        
        # If all attempts fail, raise the last error
        logging.error(f"All {self.retries} generation attempts failed")
        raise last_error or Exception("Generation failed after all retries")
    
    def _process_response(self, response: str) -> T:
        """
        Process the raw response from the model.
        
        Args:
            response: Raw response string from the model
            
        Returns:
            T: Processed response (dictionary or string)
        """
        if not response:
            raise ValueError("Empty response from model")
            
        if self.processor:
            return self.processor.process(response)
        
        # Default processing: attempt to parse as JSON
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            # If not JSON, return as string
            return response
    
    def _validate_response(self, processed_response: T) -> bool:
        """
        Validate the processed response.
        
        Args:
            processed_response: The processed response to validate
            
        Returns:
            bool: True if the response is valid, False otherwise
        """
        if self.validator:
            return self.validator.validate(processed_response)
        
        # Default validation: check if response exists
        return processed_response is not None