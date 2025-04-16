"""
I/O utilities for the Audio Companion Component.

This module provides functions for reading input JSON, validating content,
creating target directories, and writing output JSON with media file paths.
"""
import json
import os
from typing import Dict, List, Any
# import TEXT_KEY from main.py
from main import TEXT_KEY

def _validate_json_data(data: Any) -> None:
    """Validate that JSON data contains a list of objects with sentence fields."""
    if not isinstance(data, list):
        raise ValueError("Input JSON must contain a list of objects")
        
    for idx, item in enumerate(data):
        if not isinstance(item, dict):
            raise ValueError(f"Item at index {idx} is not an object")
        if TEXT_KEY not in item:
            raise ValueError(f"Object at index {idx} is missing the '{TEXT_KEY}' field")

def read_input_json(file_path: str) -> List[Dict[str, Any]]:
    """
    Read input JSON file and validate that each object has a "sentence" field.
    
    Args:
        file_path: Path to the input JSON file.
        
    Returns:
        List of dictionaries from the JSON file.
        
    Raises:
        FileNotFoundError: If the input file doesn't exist.
        ValueError: If any object in the JSON doesn't have a "sentence" field.
        json.JSONDecodeError: If the file contains invalid JSON.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        _validate_json_data(data)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"Input file not found: {file_path}")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Invalid JSON in input file: {str(e)}", e.doc, e.pos)

def create_target_directory(save_directory: str, media_subdirectory: str) -> str:
    """
    Create and return the target directory path.
    
    Args:
        save_directory: The base directory where media files will be stored.
        media_subdirectory: The subfolder within the save_directory.
        
    Returns:
        The absolute path to the target directory.
    """
    # Expand user home directory if present
    save_dir = os.path.expanduser(save_directory)
    
    # Combine save_directory and media_subdirectory
    target_dir = os.path.join(save_dir, media_subdirectory)
    
    # Create the directory if it doesn't exist
    os.makedirs(target_dir, exist_ok=True)
    
    return target_dir

def save_audio_file(target_dir: str, file_name: str, audio_data: bytes) -> Dict[str, str]:
    """
    Save audio data to a file and return the absolute and relative paths.
    
    Args:
        target_dir: The target directory where the file will be saved.
        file_name: The name of the file (without extension).
        audio_data: The binary audio data to be saved.
        
    Returns:
        Dictionary containing the absolute and relative paths to the saved file.
    """
    # Ensure the filename has the .mp3 extension
    if not file_name.endswith('.mp3'):
        file_name += '.mp3'
    
    # Create paths
    abs_path = os.path.join(target_dir, file_name)
    rel_path = os.path.join(os.path.basename(target_dir), file_name)
    
    # Save the audio data to the file
    with open(abs_path, 'wb') as f:
        f.write(audio_data)
    
    return {
        'audio_absolute_path': abs_path,
        'audio_relative_path': rel_path
    }
    
def write_output_json(data: List[Dict[str, Any]], output_file_path: str) -> None:
    """
    Write the updated data to an output JSON file.
    
    Args:
        data: The list of objects to be written to the output file.
        output_file_path: The path where the output file will be saved.
    """
    # Create the output directory if it doesn't exist
    output_dir = os.path.dirname(output_file_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    # Write the data to the output file
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)