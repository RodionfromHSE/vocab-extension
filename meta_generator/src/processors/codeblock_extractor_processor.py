import json
import re
from typing import Dict, Any, Union, Optional

from src.processors.base_processor import BaseProcessor


class CodeBlockExtractorProcessor(BaseProcessor[Union[Dict[str, Any], str]]):
    """
    Processor for extracting code blocks from text responses.
    
    This processor identifies and extracts content from code blocks 
    in model responses, typically to parse JSON content from markdown-formatted
    responses that include ```json blocks.
    """
    
    def __init__(self, config: Dict[str, Any], extract_json: bool = True):
        """
        Initialize the code block extractor processor.
        
        Args:
            config: Dictionary containing configuration parameters
            extract_json: If True, attempts to parse extracted content as JSON
        """
        super().__init__(config)
        self.extract_json = extract_json
        
    def process(self, response: str) -> Union[Dict[str, Any], str]:
        """
        Extract content from code blocks in the response.
        
        Args:
            response: Raw response string from the model,
                     potentially containing code blocks
            
        Returns:
            Union[Dict[str, Any], str]: JSON object if extraction and parsing succeeds,
                                       otherwise the extracted string
            
        Raises:
            ValueError: If no code blocks are found and extraction is strict
        """
        if not response:
            return {}
            
        # Extract content from code blocks
        extracted_content = self._extract_from_codeblocks(response)
        
        if not extracted_content:
            # If no code blocks found, use the entire response
            extracted_content = response
        
        if self.extract_json:
            try:
                # Attempt to parse as JSON
                return json.loads(extracted_content)
            except json.JSONDecodeError:
                # If JSON parsing fails, return the extracted content as-is
                return extracted_content
        else:
            return extracted_content
            
    def _extract_from_codeblocks(self, text: str) -> str:
        """
        Extract content from code blocks in text.
        
        Args:
            text: Text potentially containing code blocks
            
        Returns:
            str: Content of the first code block, or empty string if none found
        """
        # Match both ```json and ``` code blocks
        # The pattern looks for:
        # 1. Three backticks, optionally followed by "json" (case insensitive)
        # 2. Capture everything until the closing three backticks
        json_pattern = r'```(?:json)?\s*\n([\s\S]*?)\n\s*```'
        matches = re.findall(json_pattern, text, re.IGNORECASE)
        
        if matches:
            # Return the content of the first code block
            return matches[0].strip()
        else:
            # If specific JSON pattern not found, try generic code block
            generic_pattern = r'```([\s\S]*?)```'
            matches = re.findall(generic_pattern, text)
            if matches:
                return matches[0].strip()
                
        return ""