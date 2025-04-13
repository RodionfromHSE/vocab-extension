"""Tests for the smart_format utilities that handle template variable substitution."""
import re
import pytest
import warnings

from src.utils.smart_format import (
    smart_format, 
    format_with_fallbacks, 
    extract_variables
)


class TestSmartFormat:
    """Test cases for the smart_format function."""
    
    def test_successful_formatting(self):
        """Test standard successful variable substitution."""
        template = "Hello, {name}! You are {age} years old."
        variables = {"name": "Alice", "age": 30}
        
        result = smart_format(template, variables)
        
        assert result == "Hello, Alice! You are 30 years old."
    
    def test_missing_variable(self):
        """Test that KeyError is raised when a variable is missing."""
        template = "Hello, {name}! You are {age} years old."
        variables = {"name": "Alice"}  # Missing 'age'
        
        with pytest.raises(KeyError) as excinfo:
            smart_format(template, variables)
        
        assert "Missing required template variable: 'age'" in str(excinfo.value)
    
    def test_unused_variable_warning(self):
        """Test that a warning is issued for unused variables."""
        template = "Hello, {name}!"
        variables = {"name": "Alice", "age": 30}  # 'age' is unused
        
        with pytest.warns(UserWarning) as record:
            result = smart_format(template, variables)
        
        assert result == "Hello, Alice!"
        assert len(record) == 1
        assert "Unused variables provided" in str(record[0].message)
        assert "age" in str(record[0].message)
    
    def test_empty_template(self):
        """Test handling of an empty template."""
        template = ""
        variables = {"name": "Alice"}
        
        result = smart_format(template, variables)
        
        assert result == ""
        
    def test_template_without_variables(self):
        """Test a template with no variables."""
        template = "Hello, world!"
        variables = {"name": "Alice"}
        
        with pytest.warns(UserWarning) as record:
            result = smart_format(template, variables)
        
        assert result == "Hello, world!"
        assert len(record) == 1
        assert "Unused variables provided" in str(record[0].message)


class TestFormatWithFallbacks:
    """Test cases for the format_with_fallbacks function."""
    
    def test_successful_formatting_with_variables(self):
        """Test formatting with all variables provided in primary dict."""
        template = "Hello, {name}! You are {age} years old."
        variables = {"name": "Alice", "age": 30}
        fallbacks = {"name": "Unknown", "age": 0, "country": "Unknown"}
        
        result = format_with_fallbacks(template, variables, fallbacks)
        
        assert result == "Hello, Alice! You are 30 years old."
    
    def test_successful_formatting_with_fallbacks(self):
        """Test formatting with some variables from fallbacks."""
        template = "Hello, {name}! You are {age} years old."
        variables = {"name": "Alice"}  # Missing 'age'
        fallbacks = {"age": 30}
        
        result = format_with_fallbacks(template, variables, fallbacks)
        
        assert result == "Hello, Alice! You are 30 years old."
    
    def test_variables_override_fallbacks(self):
        """Test that primary variables take precedence over fallbacks."""
        template = "Hello, {name}!"
        variables = {"name": "Alice"}
        fallbacks = {"name": "Bob"}
        
        result = format_with_fallbacks(template, variables, fallbacks)
        
        assert result == "Hello, Alice!"
    
    def test_missing_variable_in_both(self):
        """Test that KeyError is raised when a variable is missing from both dicts."""
        template = "Hello, {name}! You are {age} years old."
        variables = {"name": "Alice"}
        fallbacks = {"country": "USA"}  # Doesn't have 'age' either
        
        with pytest.raises(KeyError) as excinfo:
            format_with_fallbacks(template, variables, fallbacks)
        
        assert "Missing required template variable: 'age'" in str(excinfo.value)
    
    def test_none_fallbacks_defaults_to_empty_dict(self):
        """Test that None fallbacks defaults to empty dict."""
        template = "Hello, {name}!"
        variables = {"name": "Alice"}
        
        result = format_with_fallbacks(template, variables)
        
        assert result == "Hello, Alice!"


class TestExtractVariables:
    """Test cases for the extract_variables function."""
    
    def test_extract_single_variable(self):
        """Test extracting a single variable from a template."""
        template = "Hello, {name}!"
        
        variables = extract_variables(template)
        
        assert variables == ["name"]
    
    def test_extract_multiple_variables(self):
        """Test extracting multiple variables from a template."""
        template = "Hello, {name}! You are {age} years old from {country}."
        
        variables = extract_variables(template)
        
        assert set(variables) == {"name", "age", "country"}
        assert len(variables) == 3
    
    def test_extract_duplicate_variables(self):
        """Test extracting duplicate variables from a template."""
        template = "Hello, {name}! Your name is {name}."
        
        variables = extract_variables(template)
        
        assert variables == ["name", "name"]
        assert len(variables) == 2
    
    def test_extract_from_empty_template(self):
        """Test extracting variables from an empty template."""
        template = ""
        
        variables = extract_variables(template)
        
        assert variables == []
    
    def test_extract_with_no_variables(self):
        """Test extracting from a template with no variables."""
        template = "Hello, world!"
        
        variables = extract_variables(template)
        
        assert variables == []
    
    def test_extract_with_nested_braces(self):
        """Test extracting variables with complex nested braces."""
        template = "Value: {dict[key]} and {list[0]}"
        
        variables = extract_variables(template)
        
        assert set(variables) == {"dict[key]", "list[0]"}
        assert len(variables) == 2