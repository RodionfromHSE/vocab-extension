#!/usr/bin/env python3
"""Entry point for the text generation component that processes vocabulary data."""
import os
import sys
import json
import logging
from typing import Dict, Any, List, Optional
import click
from tqdm import tqdm

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s\n%(message)s\nLocation: %(pathname)s:%(lineno)d\n\n------\n',
    handlers=[logging.StreamHandler(sys.stdout)]
)

# Import our components
from src.model.openai_model import OpenAIModel
from src.prompter.template_prompter import TemplatePrompter
from src.processors.codeblock_extractor_processor import CodeBlockExtractorProcessor
from src.validators.json_response_validator import JsonResponseValidator
from src.handler.generation_handler import GenerationHandler
from src.utils.config import read_config, config_to_dict


def create_components(config: Dict[str, Any]):
    """
    Create and initialize all components required for text generation.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        tuple: (model, prompter, processor, validator, handler)
    """
    try:
        # Create model
        model = OpenAIModel(config)
        
        # Create prompter
        prompter = TemplatePrompter(config)
        
        # Create processor
        processor = CodeBlockExtractorProcessor(config, extract_json=True)
        
        # Create validator
        validator = JsonResponseValidator(config)
        
        # Create handler
        handler = GenerationHandler(config, model, prompter, processor, validator)
        
        return model, prompter, processor, validator, handler
    
    except Exception as e:
        logging.error(f"Error creating components: {e}")
        sys.exit(1)


def process_input_file(handler: GenerationHandler, input_path: str, output_path: str):
    """
    Process a JSON input file containing vocabulary words with a progress bar.
    
    Args:
        handler: The GenerationHandler to use for processing
        input_path: Path to the input JSON file
        output_path: Path to save the output JSON file
    """
    try:
        # Load input data
        with open(input_path, 'r', encoding='utf-8') as file:
            input_data = json.load(file)
        
        # Process each word entry with a progress bar
        results = []
        for entry in tqdm(input_data, desc="Processing entries"):
            try:
                # Generate enriched content
                enriched = handler.handle(entry)
                results.append(enriched)
            except Exception as e:
                logging.error(f"Error processing entry {entry.get('word', 'Unknown')}: {e}")
                # Add the original entry with an error flag
                entry['error'] = str(e)
                results.append(entry)
        
        # Save results
        with open(output_path, 'w', encoding='utf-8') as file:
            json.dump(results, file, indent=2, ensure_ascii=False)
            
        logging.info(f"Processing complete. Results saved to {output_path}")
        
    except Exception as e:
        logging.error(f"Error processing input file: {e}")
        sys.exit(1)


def get_default_paths(config):
    """
    Get default input and output paths from config if available.
    
    Args:
        config: Configuration object
        
    Returns:
        tuple: (input_path, output_path)
    """
    input_path = config.get("input", None)
    output_path = config.get("output", None)
    return input_path, output_path


@click.command()
@click.option(
    "--config", 
    default="config.yaml", 
    help="Path to the configuration file"
)
@click.option(
    "--input", "-i",
    help="Path to input JSON file containing vocabulary entries"
)
@click.option(
    "--output", "-o",
    help="Path to output JSON file"
)
def main(config, input, output):
    """Main entry point for the text generation component."""
    # Load configuration
    config_data = read_config(config)
    
    # Get input and output paths - CLI args override config values
    default_input, default_output = get_default_paths(config_data)
    input_path = input or default_input
    
    # If no input is provided either through CLI or config, exit
    if not input_path:
        logging.error("No input file specified. Use --input/-i option or set 'input' in config.yaml")
        sys.exit(1)
    
    # Determine output path
    if output:
        output_path = output
    elif default_output:
        output_path = default_output
    else:
        output_path = input_path.replace(".json", "_enriched.json")
    
    # Create components
    _, _, _, _, handler = create_components(config_data)
    
    # Process input file
    process_input_file(handler, input_path, output_path)


if __name__ == "__main__":
    main()