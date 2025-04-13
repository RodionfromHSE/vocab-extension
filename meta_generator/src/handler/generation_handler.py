import time
import logging
from typing import Dict, Any, Optional, List, Union, TypeVar, Generic

from src.handler.base_handler import BaseHandler
from src.model.base_model import BaseModel
from src.prompter.template_prompter import TemplatePrompter
from src.processors.base_processor import BaseProcessor
from src.processors.default_processor import DefaultProcessor
from src.validators.base_validator import BaseValidator
from src.validators.default_validator import DefaultValidator

# Type for processed data - typically a dictionary (JSON) or string
T = TypeVar('T', Dict[str, Any], str)

# Default handler settings (moved from config.yaml)
DEFAULT_RETRIES = 3
DEFAULT_SLEEP_TIME = 2


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
            processor: Optional processor for post-processing responses (defaults to DefaultProcessor)
            validator: Optional validator for validating processed responses (defaults to DefaultValidator)
        """
        super().__init__(config)
        self.model = model
        self.prompter = prompter
        
        # Initialize processor and validator with default implementations if not provided
        self.processor = processor if processor is not None else DefaultProcessor(config)
        self.validator = validator if validator is not None else DefaultValidator(config)
        
        # Initialize retry settings from either config or defaults
        self.retries = config.get("handler", {}).get("retries", DEFAULT_RETRIES)
        self.sleep_time = config.get("handler", {}).get("sleep_time", DEFAULT_SLEEP_TIME)
        
    def handle(self, input_data: Dict[str, Any], **kwargs) -> T:
        """
        Handle the generation workflow with input data.
        
        By default, if no custom processor or validator is provided in the constructor,
        the handler uses built-in default implementations:
        - DefaultProcessor: Attempts to parse responses as JSON, falls back to returning the string
        - DefaultValidator: Simply checks if the response is not None
        
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
                
                # Validate the processed response
                if not self._validate_response(processed_response):
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
        Process the raw response from the model by delegating to the processor.
        
        Args:
            response: Raw response string from the model
            
        Returns:
            T: Processed response (dictionary or string)
        """
        return self.processor.process(response)
    
    def _validate_response(self, processed_response: T) -> bool:
        """
        Validate the processed response by delegating to the validator.
        
        Args:
            processed_response: The processed response to validate
            
        Returns:
            bool: True if the response is valid, False otherwise
        """
        return self.validator.validate(processed_response)