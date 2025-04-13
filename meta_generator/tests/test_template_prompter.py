"""Tests for the TemplatePrompter component that handles loading and formatting prompt templates."""
import os
from typing import Dict, Any

import pytest
from unittest.mock import patch, mock_open

from src.prompter.template_prompter import TemplatePrompter
from src.utils.smart_format import extract_variables


@pytest.fixture
def test_config():
    """Config fixture for TemplatePrompter tests"""
    return {"prompt_path": "prompt.md"}


@pytest.fixture
def test_template():
    """Sample prompt template for testing"""
    return """# English Word Enrichment Template
        
You are an expert English tutor helping students learn new vocabulary.

## Word Information
- **Word:** {word}
- **Part of Speech:** {part_of_speech}
- **Translation:** {translation}

## Instructions
Create a comprehensive explanation of the word."""


@patch("builtins.open", new_callable=mock_open)
@patch("os.path.exists")
def test_template_loading(mock_exists, mock_file, test_config, test_template):
    """Test that template is loaded correctly from file"""
    # Setup mocks
    mock_exists.return_value = True
    mock_file.return_value.read.return_value = test_template
    
    # Create prompter
    prompter = TemplatePrompter(test_config)
    
    # Verify template was loaded
    assert prompter.template == test_template
    mock_file.assert_called_once_with("prompt.md", "r", encoding="utf-8")


@patch("builtins.open", new_callable=mock_open)
@patch("os.path.exists")
def test_format_prompt(mock_exists, mock_file, test_config, test_template):
    """Test that variables are correctly substituted in the template"""
    # Setup mocks
    mock_exists.return_value = True
    mock_file.return_value.read.return_value = test_template
    
    # Create prompter
    prompter = TemplatePrompter(test_config)
    
    # Test formatting with variables
    variables = {
        "word": "example",
        "part_of_speech": "noun",
        "translation": "an instance"
    }
    
    formatted = prompter.format_prompt(variables)
    
    # Check that variables were substituted
    assert "Word:** example" in formatted
    assert "Part of Speech:** noun" in formatted
    assert "Translation:** an instance" in formatted


@patch("builtins.open", new_callable=mock_open)
@patch("os.path.exists")
def test_missing_variables(mock_exists, mock_file, test_config, test_template):
    """Test handling of missing variables in template"""
    # Setup mocks
    mock_exists.return_value = True
    mock_file.return_value.read.return_value = test_template
    
    # Create prompter
    prompter = TemplatePrompter(test_config)
    
    # Test formatting with missing variables
    variables = {
        "word": "example",
        # Missing part_of_speech and translation
    }
    
    formatted = prompter.format_prompt(variables)
    
    # Check that present variables were substituted
    assert "Word:** example" in formatted
    
    # Check that missing variables are kept as placeholders
    assert "Part of Speech:** {part_of_speech}" in formatted
    assert "Translation:** {translation}" in formatted


@patch("builtins.open", new_callable=mock_open)
@patch("os.path.exists")
def test_get_required_variables(mock_exists, mock_file, test_config, test_template):
    """Test extracting required variables from template"""
    # Setup mocks
    mock_exists.return_value = True
    mock_file.return_value.read.return_value = test_template
    
    # Create prompter
    prompter = TemplatePrompter(test_config)
    
    # Get required variables
    variables = prompter.get_required_variables()
    
    # Check that all variables were extracted
    assert "word" in variables
    assert "part_of_speech" in variables
    assert "translation" in variables
    assert len(variables) == 3


@patch("os.path.exists")
def test_file_not_found(mock_exists, test_config):
    """Test error handling when template file is not found"""
    mock_exists.return_value = False
    
    # Check that appropriate error is raised
    with pytest.raises(FileNotFoundError):
        prompter = TemplatePrompter(test_config)


@patch("builtins.open", new_callable=mock_open)
@patch("os.path.exists")
def test_reload_template(mock_exists, mock_file, test_config, test_template):
    """Test reloading template from file"""
    # Setup initial template
    mock_exists.return_value = True
    mock_file.return_value.read.return_value = test_template
    
    # Create prompter
    prompter = TemplatePrompter(test_config)
    
    # Change mock to return new template
    new_template = "New template with {word}"
    mock_file.return_value.read.return_value = new_template
    
    # Reload template
    prompter.reload_template()
    
    # Check that template was updated
    assert prompter.template == new_template