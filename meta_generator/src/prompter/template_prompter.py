from typing import Dict, Any, Optional, List
import os
import logging
from src.utils.smart_format import smart_format, extract_variables


class TemplatePrompter:
    """
    Template prompter for loading and formatting prompt templates.
    
    This class handles loading prompt templates from external Markdown files
    and substituting variables within the template.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the template prompter with configuration.
        
        Args:
            config: Dictionary containing configuration parameters,
                   including the path to the prompt template file
        """
        self.config = config
        self.template = None
        self.template_path = config.get("prompt_path", "prompt.md")
        self.load_template()
        
    def load_template(self) -> None:
        """
        Load the prompt template from the specified file path.
        
        Raises:
            FileNotFoundError: If the template file cannot be found
            IOError: If there's an error reading the template file
        """
        try:
            if not os.path.exists(self.template_path):
                raise FileNotFoundError(f"Template file not found: {self.template_path}")
                
            with open(self.template_path, 'r', encoding='utf-8') as file:
                self.template = file.read()
                
            if not self.template:
                logging.warning(f"Template file is empty: {self.template_path}")
                
        except Exception as e:
            logging.error(f"Error loading template from {self.template_path}: {e}")
            raise
            
    def get_required_variables(self) -> List[str]:
        """
        Get the list of variable names required by the template.
        
        Returns:
            List[str]: List of variable names found in the template
        """
        if not self.template:
            return []
            
        return extract_variables(self.template)
        
    def format_prompt(self, variables: Dict[str, Any]) -> str:
        """
        Format the prompt template by substituting the provided variables.
        
        Args:
            variables: Dictionary of variables to substitute in the template
            
        Returns:
            str: The formatted prompt string
            
        Raises:
            ValueError: If the template has not been loaded
        """
        if not self.template:
            raise ValueError("No template loaded. Call load_template() first.")
            
        return smart_format(self.template, variables)
        
    def reload_template(self) -> None:
        """
        Reload the template from the file.
        
        This is useful when the template file has been modified externally.
        """
        self.load_template()