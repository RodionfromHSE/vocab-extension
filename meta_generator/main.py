#!/usr/bin/env python3
import os
import sys
import json
import logging
import argparse
from typing import Dict, Any, List
import yaml

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
    Process a JSON input file containing vocabulary words.
    
    Args:
        handler: The GenerationHandler to use for processing
        input_path: Path to the input JSON file
        output_path: Path to save the output JSON file
    """
    try:
        # Load input data
        with open(input_path, 'r', encoding='utf-8') as file:
            input_data = json.load(file)
        
        # Process each word entry
        results = []
        for i, entry in enumerate(input_data):
            try:
                logging.info(f"Processing entry {i+1}/{len(input_data)}: {entry.get('word', 'Unknown')}")
                # Generate enriched content
                enriched = handler.handle(entry)
                results.append(enriched)
            except Exception as e:
                logging.error(f"Error processing entry {i+1}: {e}")
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


def process_single_word(handler: GenerationHandler, word: str, part_of_speech: str, translation: str):
    """
    Process a single word from command line arguments.
    
    Args:
        handler: The GenerationHandler to use for processing
        word: The word to process
        part_of_speech: The part of speech for the word
        translation: The translation of the word
    """
    try:
        # Create input data
        input_data = {
            "word": word,
            "part_of_speech": part_of_speech,
            "translation": translation
        }
        
        # Generate enriched content
        logging.info(f"Processing: {word} ({part_of_speech})")
        enriched = handler.handle(input_data)
        
        # Print the result
        print(json.dumps(enriched, indent=2, ensure_ascii=False))
        
    except Exception as e:
        logging.error(f"Error processing word: {e}")
        sys.exit(1)


def main():
    """Main entry point for the text generation component."""
    parser = argparse.ArgumentParser(
        description="Generate enriched text content from vocabulary input."
    )
    
    # Command-line arguments
    parser.add_argument(
        "--config", 
        type=str, 
        default="config.yaml", 
        help="Path to the configuration file"
    )
    
    # Input mode group
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "--file", 
        type=str, 
        help="Path to input JSON file containing vocabulary entries"
    )
    input_group.add_argument(
        "--word", 
        type=str, 
        help="Single word to process"
    )
    
    # Additional word info parameters
    parser.add_argument(
        "--pos", 
        type=str, 
        default="noun", 
        help="Part of speech (when using --word)"
    )
    parser.add_argument(
        "--translation", 
        type=str, 
        default="", 
        help="Translation (when using --word)"
    )
    
    # Output file parameter
    parser.add_argument(
        "--output", 
        type=str, 
        help="Path to output JSON file (when using --file)"
    )
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Create components
    _, _, _, _, handler = create_components(config)
    
    # Process input
    if args.file:
        # Process file mode
        output_path = args.output or args.file.replace(".json", "_enriched.json")
        process_input_file(handler, args.file, output_path)
    else:
        # Process single word mode
        process_single_word(handler, args.word, args.pos, args.translation)


if __name__ == "__main__":
    main()