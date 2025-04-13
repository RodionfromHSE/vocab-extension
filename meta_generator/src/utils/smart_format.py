from typing import Dict, Any, Optional
import string
import re


def smart_format(template: str, variables: Dict[str, Any]) -> str:
    """
    A robust string substitution utility that safely handles variable substitutions.
    
    This function performs substitution of variables in a template string,
    gracefully handling missing variables and providing fallbacks.
    
    Args:
        template: The template string with placeholders like {variable}
        variables: Dictionary of variables to substitute into the template
        
    Returns:
        str: The formatted string with variables substituted
        
    Examples:
        >>> smart_format("Hello, {name}!", {"name": "World"})
        'Hello, World!'
        >>> smart_format("Hello, {name}!", {})
        'Hello, {name}!'
    """
    # Create a custom formatter that handles missing keys
    class SafeFormatter(string.Formatter):
        def get_value(self, key, args, kwargs):
            # Return the key name if the key is not found
            if isinstance(key, str):
                return kwargs.get(key, "{" + key + "}")
            else:
                return super().get_value(key, args, kwargs)
    
    formatter = SafeFormatter()
    return formatter.format(template, **variables)


def format_with_fallbacks(template: str, variables: Dict[str, Any], 
                         fallbacks: Dict[str, Any] = None) -> str:
    """
    Format a string with variables, using fallbacks for missing values.
    
    Args:
        template: The template string with placeholders
        variables: Primary dictionary of variables to substitute
        fallbacks: Fallback dictionary to use when variables are missing
        
    Returns:
        str: The formatted string with variables substituted
    """
    if fallbacks is None:
        fallbacks = {}
    
    # Combine variables and fallbacks with variables taking precedence
    combined = {**fallbacks, **variables}
    
    return smart_format(template, combined)


def extract_variables(template: str) -> list:
    """
    Extract variable names from a template string.
    
    Args:
        template: The template string with placeholders like {variable}
        
    Returns:
        list: List of variable names found in the template
    """
    # Find all patterns like {variable_name}
    pattern = r'\{([^{}]+)\}'
    variables = re.findall(pattern, template)
    
    return variables