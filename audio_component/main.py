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
from src import io_utils

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
        config = omegaconf.OmegaConf.load(config_path)
        return config
    except Exception as e:
        raise omegaconf.errors.OmegaConfError(f"Error loading configuration: {str(e)}") from e

def process_data(data: List[Dict[str, Any]], target_dir: str, language: str) -> List[Dict[str, Any]]:
    """
    Process the data by generating audio files for each sentence and updating the data with file paths.
    
    Args:
        data: The list of objects to process.
        target_dir: The target directory where audio files will be saved.
        language: The language to use for text-to-speech conversion.
        
    Returns:
        The updated list of objects.
    """
    # Use tqdm to create a progress bar
    for idx, item in enumerate(tqdm(data, desc="Processing items", unit="item")):
        sentence = item["sentence"]
        
        # Generate a unique filename based on the index
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
    
    return data

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
        
        # Determine input file with priority: CLI argument > config file
        if input_file is None:
            if hasattr(cfg, 'input_file') and cfg.input_file:
                input_file = cfg.input_file
            else:
                raise click.UsageError("Input file must be provided either as an argument or in the config file")
        
        # Read input JSON
        data = io_utils.read_input_json(input_file)
        
        # Create the target directory
        target_dir = io_utils.create_target_directory(
            cfg.save_directory, 
            cfg.media_subdirectory
        )
        
        # Determine the output file path with priority: CLI option > config file > derived from input
        if output_file is None:
            if hasattr(cfg, 'output_file') and cfg.output_file:
                output_file = cfg.output_file
            else:
                # Derive default output file from input file
                base, ext = os.path.splitext(input_file)
                output_file = f"{base}_with_audio{ext}"
        
        # Process the data
        updated_data = process_data(data, target_dir, cfg.language)
        
        # Write the updated data to the output file
        io_utils.write_output_json(updated_data, output_file)
        
        click.echo(f"Processing complete. Output written to {output_file}")
        
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)

if __name__ == "__main__":
    main()