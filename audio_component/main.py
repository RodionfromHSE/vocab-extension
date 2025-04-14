"""
Main orchestration script for the Audio Companion Component.

This script loads the configuration, processes the input JSON file,
generates audio files for each sentence, and updates the JSON with
the paths to the generated files.
"""
import os
import sys
import argparse
from typing import Dict, List, Any
import omegaconf
from audio_generator import generate_audio
import io_utils

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Audio Companion Component')
    parser.add_argument('input_file', help='Path to the input JSON file')
    parser.add_argument('--output-file', help='Path to the output JSON file (default: [input_file]_with_audio.json)')
    parser.add_argument('--config', default='config.yaml', help='Path to the configuration file (default: config.yml)')
    
    return parser.parse_args()

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
    for idx, item in enumerate(data):
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
            
            print(f"Processed item {idx + 1}/{len(data)}: '{sentence[:30]}...' if len(sentence) > 30 else sentence")
        
        except Exception as e:
            print(f"Error processing item {idx}: {str(e)}", file=sys.stderr)
            # Continue processing other items
    
    return data

def main():
    # Parse command line arguments
    args = parse_arguments()
    
    try:
        # Load configuration
        config = load_config(args.config)
        
        # Read input JSON
        data = io_utils.read_input_json(args.input_file)
        
        # Create the target directory
        target_dir = io_utils.create_target_directory(
            config.save_directory, 
            config.media_subdirectory
        )
        
        # Determine the output file path
        output_file = args.output_file
        if not output_file:
            base, ext = os.path.splitext(args.input_file)
            output_file = f"{base}_with_audio{ext}"
        
        # Process the data
        updated_data = process_data(data, target_dir, config.language)
        
        # Write the updated data to the output file
        io_utils.write_output_json(updated_data, output_file)
        
        print(f"Processing complete. Output written to {output_file}")
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()