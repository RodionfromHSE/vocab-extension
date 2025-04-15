"""
Main orchestration script for the Audio Companion Component.

This script loads the configuration, processes the input JSON file,
generates audio files for each sentence, and updates the JSON with
the paths to the generated files.
"""
import os
import sys
from typing import Dict, List, Any, Optional
import click
import omegaconf
from tqdm import tqdm
from src.audio_generator import generate_audio
import src.io_utils as io_utils

TEXT_KEY = "word"  # Key for the text to be converted to audio

def load_config(config_path: str) -> omegaconf.DictConfig:
    """
    Load configuration from the specified YAML file.
    
    Args:
        config_path: Path to the configuration file.
        
    Returns:
        The loaded configuration.
        
    Raises:
        FileNotFoundError: If the configuration file doesn't exist.
        omegaconf.errors.OmegaConfError: If there's an error loading the configuration.
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    try:
        return omegaconf.OmegaConf.load(config_path)
    except Exception as e:
        raise omegaconf.errors.OmegaConfError(f"Error loading configuration: {str(e)}") from e

def process_item(item: Dict[str, Any], idx: int, target_dir: str, language: str) -> Dict[str, Any]:
    """Process a single item by generating audio and updating the item."""
    sentence = item[TEXT_KEY]
    file_name = f"audio_{idx}.mp3"
    
    try:
        # Generate audio for the sentence
        audio_data = generate_audio(sentence, language=language)
        
        # Save the audio file and get the paths
        paths = io_utils.save_audio_file(target_dir, file_name, audio_data)
        
        # Update the item with the paths
        item.update(paths)
    except Exception as e:
        # Log error to stderr but continue processing other items
        print(f"Error processing item {idx}: {str(e)}", file=sys.stderr)
    
    return item

def process_data(data: List[Dict[str, Any]], target_dir: str, language: str) -> List[Dict[str, Any]]:
    """
    Process the data by generating audio files for each sentence and updating with file paths.
    
    Args:
        data: The list of objects to process.
        target_dir: The target directory where audio files will be saved.
        language: The language to use for text-to-speech conversion.
        
    Returns:
        The updated list of objects.
    """
    # Use tqdm to create a progress bar and process each item
    start_idx = len(os.listdir(target_dir)) if os.path.exists(target_dir) else 0
    tqdm.write(f"Starting from index: {start_idx}")
    tqdm.write(f"Target directory: {target_dir}")
    tqdm.write(f"Language: {language}")
    for idx, item in enumerate(tqdm(data, desc="Processing items", unit="item"), start=start_idx):
        process_item(item, idx, target_dir, language)
    
    return data

def determine_input_file(cli_input: Optional[str], config: omegaconf.DictConfig) -> str:
    """Determine which input file to use based on CLI args and config."""
    if cli_input:
        return cli_input
        
    if hasattr(config, 'input_file') and config.input_file:
        return config.input_file
        
    raise click.UsageError("Input file must be provided either as an argument or in the config file")

def determine_output_file(cli_output: Optional[str], config: omegaconf.DictConfig, input_file: str) -> str:
    """Determine which output file to use based on CLI args, config, or derive from input file."""
    if cli_output:
        return cli_output
        
    if hasattr(config, 'output_file') and config.output_file:
        return config.output_file
        
    # Derive default output file from input file
    base, ext = os.path.splitext(input_file)
    return f"{base}_with_audio{ext}"

@click.command()
@click.argument('input_file', type=click.Path(exists=True), required=False)
@click.option('--output-file', '-o', type=click.Path(), help='Path to the output JSON file')
@click.option('--config', '-c', type=click.Path(exists=True), default='config.yaml', 
              help='Path to the configuration file (default: config.yaml)')
def main(input_file: Optional[str], output_file: Optional[str], config: str):
    """
    Audio Companion Component: Processes JSON files and generates speech media files.
    
    INPUT_FILE: Path to the input JSON file (optional if specified in config)
    """
    try:
        # Load configuration
        cfg = load_config(config)
        
        # Determine input and output files
        input_path = determine_input_file(input_file, cfg)
        output_path = determine_output_file(output_file, cfg, input_path)
        
        # Read input JSON
        data = io_utils.read_input_json(input_path)
        
        # Create the target directory
        target_dir = io_utils.create_target_directory(
            cfg.save_directory, 
            cfg.media_subdirectory
        )
        
        # Process the data
        updated_data = process_data(data, target_dir, cfg.language)
        
        # Write the updated data to the output file
        io_utils.write_output_json(updated_data, output_path)
        
        click.echo(f"Processing complete. Output written to {output_path}")
        
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)

if __name__ == "__main__":
    main()