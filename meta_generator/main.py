#!/usr/bin/env python3
"""Entry point for the text generation component that processes vocabulary data."""
import os
import sys
import json
import logging
from typing import Dict, Any, List
import yaml
import click
from tqdm import tqdm

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

# Import our components
from src.model.openai_model import OpenAIModel
from src.prompter.template_prompter import TemplatePrompter
from src.processors.codeblock_extractor_processor import CodeBlockExtractorProcessor
from src.validators.json_response_validator import JsonResponseValidator
from src.handler.generation_handler import GenerationHandler


def load_config(config_path: str = "config.yaml") -> Dict[str, Any]:
    """
    Load configuration from YAML file.
    
    Args:
        config_path: Path to the configuration file
        
    Returns:
        Dict[str, Any]: Configuration dictionary
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        return config
    except Exception as e:
        logging.error(f"Error loading configuration: {e}")
        sys.exit(1)


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


@click.command()
@click.option(
    "--config", 
    default="config.yaml", 
    help="Path to the configuration file"
)
@click.option(
    "--file", 
    required=True,
    help="Path to input JSON file containing vocabulary entries"
)
@click.option(
    "--output", 
    help="Path to output JSON file"
)
def main(config, file, output):
    """Main entry point for the text generation component."""
    # Load configuration
    config_data = load_config(config)
    
    # Create components
    _, _, _, _, handler = create_components(config_data)
    
    # Process input file
    output_path = output or file.replace(".json", "_enriched.json")
    process_input_file(handler, file, output_path)


if __name__ == "__main__":
    main()