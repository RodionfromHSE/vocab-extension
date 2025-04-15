#!/usr/bin/env python3
"""
Flashcard Converter: Converts JSON meta information into Anki flashcards.

This script loads a configuration file specifying an input JSON file and 
flashcard templates, then processes the data to create Anki flashcards.
"""

import json
import logging
import sys
from pathlib import Path
from typing import Dict, List, Any
import click
from omegaconf import DictConfig
from tqdm import tqdm

from ankiapi import AnkiApi
from boilerplate_tools import smart_format, load_config, read_json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(name)s - %(levelname)s - %(message)s\nLocation: %(pathname)s:%(lineno)d",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("flashcard_converter")


def setup_config(config_path: str = "config.yaml") -> DictConfig:
    """
    Load and validate the configuration file.
    
    Args:
        config_path: Path to the configuration YAML file

    Returns:
        Loaded configuration as DictConfig
    """
    try:
        config = load_config(config_path)
        
        # Validate required fields
        required_fields = ["input_file", "deck_name", "flashcard_template"]
        for field in required_fields:
            if field not in config:
                raise ValueError(f"Missing required field '{field}' in config file")
        
        # Validate flashcard template format
        for template in config.flashcard_template:
            if "front" not in template or "back" not in template:
                raise ValueError("Each flashcard template must contain 'front' and 'back' keys")
        
        return config
    
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")
        raise

def create_flashcards(meta_data: List[Dict[str, Any]], 
                     templates: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Create flashcards from meta data using the provided templates.
    
    Args:
        meta_data: List of meta information records
        templates: List of flashcard templates with 'front' and 'back' keys

    Returns:
        List of flashcards with 'front' and 'back' content
    """
    flashcards = []
    
    for record in meta_data:
        for template in templates:
            try:
                front = smart_format(template["front"], record)
                back = smart_format(template["back"], record)
                
                flashcards.append({
                    "front": front,
                    "back": back
                })
            except KeyError as e:
                logger.error(f"Missing key in record: {e}. Skipping this flashcard.")
                raise
            except Exception as e:
                logger.warning(f"Error processing record: {e}. Skipping this flashcard.")
    
    return flashcards


def add_to_anki(flashcards: List[Dict[str, str]], deck_name: str) -> None:
    """
    Add the generated flashcards to an Anki deck.
    
    Args:
        flashcards: List of flashcards with 'front' and 'back' content
        deck_name: Name of the Anki deck to create/populate
    """
    try:
        anki = AnkiApi()
        
        anki.check_server()
        anki.create_deck(deck_name)  # create if not exists
        logger.info(f"Created/accessed deck: {deck_name}")
        
        # Add flashcards to deck
        cards_added = 0
        for card in tqdm(flashcards):
            try:
                anki.add_flashcard(
                    deck_name=deck_name,
                    front=card["front"],
                    back=card["back"]
                )
                cards_added += 1
            except Exception as e:
                logger.warning(f"Failed to add flashcard: {e}")
        
        logger.info(f"Added {cards_added} cards to deck '{deck_name}'")
    
    except Exception as e:
        logger.error(f"Error interacting with Anki: {e}")
        raise


@click.command()
@click.option('--input-file', '-i', type=click.Path(exists=True), help='Path to the input JSON file')
@click.option('--config', '-c', type=click.Path(exists=True), default="config.yaml", help='Path to the configuration file')
def main(input_file, config) -> None:
    """
    Convert JSON meta data to Anki flashcards.
    
    If input-file is provided, it will override the value in the config file.
    """
    try:
        # Load configuration
        config_obj = setup_config(config)
        
        # Override input file from command line if provided
        if input_file:
            logger.info(f"Using input file from command line: {input_file}")
            input_path = Path(input_file).expanduser().resolve()
        else:
            logger.info(f"Using input file from config: {config_obj.input_file}")
            input_path = Path(config_obj.input_file).expanduser().resolve()
        
        logger.info(f"Loaded configuration. Input file: {input_path}, Deck: {config_obj.deck_name}")
        
        # Load meta data
        meta_data = read_json(str(input_path))
        logger.info(f"Loaded {len(meta_data)} records from {input_path}")
        
        # Create flashcards
        flashcards = create_flashcards(meta_data, config_obj.flashcard_template)
        logger.info(f"Created {len(flashcards)} flashcards")
        
        # Add to Anki
        add_to_anki(flashcards, config_obj.deck_name)
        
        logger.info("Conversion completed successfully")
    
    except Exception as e:
        logger.error(f"Conversion failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()