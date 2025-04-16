"""
Vocabulary Extension Pipeline

This module implements a multi-stage pipeline for processing vocabulary data:
1. Dataset conversion - Merges individual JSON files into a single dataset
2. Meta generation - Enriches words with definitions and examples
3. Audio generation - Creates audio files for words and examples
4. Flashcard conversion - Generates Anki flashcards from the enriched data

Each stage can be run independently or as part of the complete pipeline,
with options to skip individual stages as needed.
"""
import os
import sys
import subprocess
import functools
import logging
from pathlib import Path
from typing import Dict, Any, Callable, TypeVar, Optional, List, Union
import click
from dotenv import load_dotenv

from boilerplate_tools import load_config



# Type variable for the decorator
load_dotenv()
T = TypeVar('T')
PYTHON_EXECUTABLE = sys.executable

def change_directory(directory: str) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Decorator that changes the working directory before executing a function and
    restores the original directory afterward.
    
    Args:
        directory: The directory to change to before executing the function
        
    Returns:
        A decorator function that handles directory changes
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            # assert dir exists
            if not os.path.exists(directory):
                raise FileNotFoundError(f"Directory does not exist: {directory}")
            
            original_dir = os.getcwd()
            try:
                os.chdir(directory)
                return func(*args, **kwargs)
            finally:
                os.chdir(original_dir)
        return wrapper
    return decorator

DEBUG = True
def run_subprocess(
    command: List[str], 
    description: str,
    check: bool = True
) -> subprocess.CompletedProcess:
    """
    Run a subprocess with proper logging and error handling.
    
    Args:
        command: Command to execute as a list of strings
        description: Description of what the subprocess is doing (for logging)
        check: Whether to raise an exception if the subprocess returns non-zero exit code
    
    Returns:
        The completed process information
    
    Raises:
        subprocess.CalledProcessError: If the subprocess returns a non-zero exit code and check is True
    """
    print(f"Running {description}")
    try:
        result = subprocess.run(
            command, 
            check=check, 
            capture_output=True, 
            text=True
        )
        print(f"Successfully completed: {description}")
        if DEBUG:
            print(f"Command: {' '.join(command)}")
            print(f"Output:\n{result.stdout}")
            print(f"stderr (logs):\n{result.stderr}")
        return result
    except subprocess.CalledProcessError as e:
        print(f"ERROR in {description}:")
        print(f"Exit code: {e.returncode}")
        print(f"Standard output: {e.stdout}")
        print(f"Standard error: {e.stderr}")
        raise

def get_shortened_path(path: str) -> str:
    """
    Get shortened version of a path containing only the base directory and filename/dirname.
    
    Args:
        path: Full path to file or directory
        
    Returns:
        Shortened path string
    """
    dirname = os.path.dirname(path)
    basename = os.path.basename(path)
    if basename == '':  # If path ends with separator
        basename = os.path.basename(dirname)
        dirname = os.path.dirname(dirname)
    return os.path.join(os.path.basename(dirname), basename)

def run_dataset_converter(config: Dict[str, Any]) -> str:
    """
    Run the dataset converter component to merge individual JSON files.
    
    Args:
        config: Configuration dictionary with dataset converter settings
        
    Returns:
        Path to the output file
    """
    input_dir = config['dataset_converter']['input_dir']
    output_file = config['dataset_converter']['output_file']
    
    # Ensure output directory exists
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    
    run_subprocess(
        [PYTHON_EXECUTABLE, "other/dataset_convertor.py", input_dir, output_file],
        f"dataset converter: {get_shortened_path(input_dir)} -> {get_shortened_path(output_file)}"
    )
    return output_file

@change_directory("meta_generator")
def run_meta_generator(config: Dict[str, Any]) -> str:
    """
    Run the meta generator component to enrich words with definitions and examples.
    
    Args:
        config: Configuration dictionary with meta generator settings
        
    Returns:
        Path to the output file
    """
    meta_config = config['meta_generator']['config_file']
    input_file = config['meta_generator']['input_file']
    output_file = config['meta_generator']['output_file']
    
    # Ensure output directory exists
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    
    run_subprocess(
        [PYTHON_EXECUTABLE, "main.py", 
         "--input", input_file, 
         "--output", output_file, 
         "--config", meta_config],
        f"meta generator: {get_shortened_path(input_file)} -> {get_shortened_path(output_file)}"
    )
    return output_file

@change_directory("audio_component")
def run_audio_generator(config: Dict[str, Any]) -> str:
    """
    Run the audio component to generate audio files for each word and example.
    
    Args:
        config: Configuration dictionary with audio generator settings
        
    Returns:
        Path to the output file
    """
    audio_config = config['audio_generator']['config_file']
    input_file = config['audio_generator']['input_file']
    output_file = config['audio_generator']['output_file']
    
    run_subprocess(
        [PYTHON_EXECUTABLE, "main.py", 
         input_file, 
         "--output-file", output_file, 
         "--config", audio_config],
        f"audio generator: {get_shortened_path(input_file)} -> {get_shortened_path(output_file)}"
    )
    return output_file

@change_directory("flashcard_converter")
def run_flashcard_converter(config: Dict[str, Any]) -> None:
    """
    Run the flashcard converter to create Anki cards from the enriched data.
    
    Args:
        config: Configuration dictionary with flashcard converter settings
    """
    flashcard_config = config['flashcard_converter']['config_file']
    input_file = config['flashcard_converter']['input_file']
    
    run_subprocess(
        [PYTHON_EXECUTABLE, "main.py", 
         "-i", input_file, 
         "--config", flashcard_config],
        f"flashcard converter with {get_shortened_path(input_file)}"
    )

def run_or_skip(
    action: Callable[[Dict[str, Any]], Optional[str]], 
    is_skip: bool, 
    skip_message: str, 
    config: Dict[str, Any]
) -> Optional[str]:
    """
    Run an action if not skipped, otherwise print a skip message.
    
    Args:
        action: Function to run if not skipped
        is_skip: Flag indicating whether to skip the action
        skip_message: Message to print if action is skipped
        config: Configuration dictionary to pass to the action
        
    Returns:
        Result of the action function if not skipped, None otherwise
    """
    if not is_skip:
        return action(config)
    else:
        print(skip_message)
        return None

@click.command()
@click.option("--config", default="pipeline_config.yaml", help="Pipeline configuration file")
@click.option("--skip-dataset", is_flag=True, help="Skip dataset conversion step")
@click.option("--skip-meta", is_flag=True, help="Skip meta generation step")
@click.option("--skip-audio", is_flag=True, help="Skip audio generation step")
@click.option("--skip-flashcard", is_flag=True, help="Skip flashcard creation step")
def main(
    config: str, 
    skip_dataset: bool, 
    skip_meta: bool, 
    skip_audio: bool, 
    skip_flashcard: bool
) -> None:
    """
    Run the complete vocabulary extension pipeline from raw data to Anki flashcards.
    
    Args:
        config: Path to the pipeline configuration file
        skip_dataset: Flag to skip dataset conversion step
        skip_meta: Flag to skip meta generation step
        skip_audio: Flag to skip audio generation step
        skip_flashcard: Flag to skip flashcard creation step
    """
    config_data = load_config(config)
    
    run_or_skip(run_dataset_converter, skip_dataset, "Skipping dataset conversion", config_data)
    run_or_skip(run_meta_generator, skip_meta, "Skipping meta generation", config_data)
    run_or_skip(run_audio_generator, skip_audio, "Skipping audio generation", config_data)
    run_or_skip(run_flashcard_converter, skip_flashcard, "Skipping flashcard creation", config_data)
    
    print("Pipeline completed successfully!")

if __name__ == "__main__":
    main()