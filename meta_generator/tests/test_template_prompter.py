import unittest
from unittest.mock import patch, mock_open
import os
from typing import Dict, Any

from src.prompter.template_prompter import TemplatePrompter
from src.utils.smart_format import extract_variables


class TestTemplatePrompter(unittest.TestCase):
    """Test cases for the TemplatePrompter class"""
    
    def setUp(self):
        self.config = {"prompt_path": "prompt.md"}
        self.test_template = """# English Word Enrichment Template
        
You are an expert English tutor helping students learn new vocabulary.

## Word Information
- **Word:** {word}
- **Part of Speech:** {part_of_speech}
- **Translation:** {translation}

## Instructions
Create a comprehensive explanation of the word."""
    
    @patch("builtins.open", new_callable=mock_open)
    @patch("os.path.exists")
    def test_template_loading(self, mock_exists, mock_file):
        """Test that template is loaded correctly from file"""
        # Setup mocks
        mock_exists.return_value = True
        mock_file.return_value.read.return_value = self.test_template
        
        # Create prompter
        prompter = TemplatePrompter(self.config)
        
        # Verify template was loaded
        self.assertEqual(prompter.template, self.test_template)
        mock_file.assert_called_once_with("prompt.md", "r", encoding="utf-8")
    
    @patch("builtins.open", new_callable=mock_open)
    @patch("os.path.exists")
    def test_format_prompt(self, mock_exists, mock_file):
        """Test that variables are correctly substituted in the template"""
        # Setup mocks
        mock_exists.return_value = True
        mock_file.return_value.read.return_value = self.test_template
        
        # Create prompter
        prompter = TemplatePrompter(self.config)
        
        # Test formatting with variables
        variables = {
            "word": "example",
            "part_of_speech": "noun",
            "translation": "an instance"
        }
        
        formatted = prompter.format_prompt(variables)
        
        # Check that variables were substituted
        self.assertIn("Word:** example", formatted)
        self.assertIn("Part of Speech:** noun", formatted)
        self.assertIn("Translation:** an instance", formatted)
    
    @patch("builtins.open", new_callable=mock_open)
    @patch("os.path.exists")
    def test_missing_variables(self, mock_exists, mock_file):
        """Test handling of missing variables in template"""
        # Setup mocks
        mock_exists.return_value = True
        mock_file.return_value.read.return_value = self.test_template
        
        # Create prompter
        prompter = TemplatePrompter(self.config)
        
        # Test formatting with missing variables
        variables = {
            "word": "example",
            # Missing part_of_speech and translation
        }
        
        formatted = prompter.format_prompt(variables)
        
        # Check that present variables were substituted
        self.assertIn("Word:** example", formatted)
        
        # Check that missing variables are kept as placeholders
        self.assertIn("Part of Speech:** {part_of_speech}", formatted)
        self.assertIn("Translation:** {translation}", formatted)
    
    @patch("builtins.open", new_callable=mock_open)
    @patch("os.path.exists")
    def test_get_required_variables(self, mock_exists, mock_file):
        """Test extracting required variables from template"""
        # Setup mocks
        mock_exists.return_value = True
        mock_file.return_value.read.return_value = self.test_template
        
        # Create prompter
        prompter = TemplatePrompter(self.config)
        
        # Get required variables
        variables = prompter.get_required_variables()
        
        # Check that all variables were extracted
        self.assertIn("word", variables)
        self.assertIn("part_of_speech", variables)
        self.assertIn("translation", variables)
        self.assertEqual(len(variables), 3)
    
    @patch("os.path.exists")
    def test_file_not_found(self, mock_exists):
        """Test error handling when template file is not found"""
        mock_exists.return_value = False
        
        # Check that appropriate error is raised
        with self.assertRaises(FileNotFoundError):
            prompter = TemplatePrompter(self.config)
    
    @patch("builtins.open", new_callable=mock_open)
    @patch("os.path.exists")
    def test_reload_template(self, mock_exists, mock_file):
        """Test reloading template from file"""
        # Setup initial template
        mock_exists.return_value = True
        mock_file.return_value.read.return_value = self.test_template
        
        # Create prompter
        prompter = TemplatePrompter(self.config)
        
        # Change mock to return new template
        new_template = "New template with {word}"
        mock_file.return_value.read.return_value = new_template
        
        # Reload template
        prompter.reload_template()
        
        # Check that template was updated
        self.assertEqual(prompter.template, new_template)


if __name__ == "__main__":
    unittest.main()