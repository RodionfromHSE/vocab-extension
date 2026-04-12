#!/usr/bin/env python3
"""
CSV to JSON converter with context field.
Converts a CSV file with vocabulary data into JSON format with 'word' and 'context' fields.
"""

import csv
import json
import argparse
import sys
from pathlib import Path


def build_context(row, headers):
    """
    Build context string from CSV row data, excluding the 'word' field and empty values.
    
    Args:
        row (dict): CSV row data
        headers (list): List of CSV headers
    
    Returns:
        str: Formatted context string
    """
    context_parts = []
    
    for header in headers:
        if header == 'word':
            continue
        
        value = row.get(header, '').strip()
        if value:  # Only include non-empty values
            context_parts.append(f"{header}: {value}")
    
    return ", ".join(context_parts)


def csv_to_json_with_context(input_csv_path, output_json_path=None):
    """
    Convert CSV file to JSON with word and context fields.
    
    Args:
        input_csv_path (str): Path to input CSV file
        output_json_path (str, optional): Path to output JSON file. 
                                        If None, will use input filename with .json extension
    
    Returns:
        list: List of dictionaries with 'word' and 'context' fields
    """
    input_path = Path(input_csv_path)
    
    if not input_path.exists():
        raise FileNotFoundError(f"Input CSV file not found: {input_csv_path}")
    
    # Set default output path if not provided
    if output_json_path is None:
        output_json_path = input_path.with_suffix('.json')
    
    result = []
    
    try:
        with open(input_path, 'r', encoding='utf-8') as csvfile:
            # Detect delimiter
            sample = csvfile.read(1024)
            csvfile.seek(0)
            sniffer = csv.Sniffer()
            delimiter = sniffer.sniff(sample).delimiter
            
            reader = csv.DictReader(csvfile, delimiter=delimiter)
            headers = reader.fieldnames
            
            if not headers or 'word' not in headers:
                raise ValueError("CSV must have a 'word' column")
            
            for row in reader:
                word = row.get('word', '').strip()
                if not word:  # Skip rows with empty word field
                    continue
                
                context = build_context(row, headers)
                
                result.append({
                    "word": word,
                    "context": context
                })
        
        # Write JSON output
        with open(output_json_path, 'w', encoding='utf-8') as jsonfile:
            json.dump(result, jsonfile, indent=2, ensure_ascii=False)
        
        print(f"Successfully converted {len(result)} entries from {input_csv_path} to {output_json_path}")
        return result
        
    except Exception as e:
        print(f"Error processing file: {e}", file=sys.stderr)
        raise


def main():
    """Main function to handle command line arguments."""
    parser = argparse.ArgumentParser(
        description="Convert CSV file to JSON with word and context fields"
    )
    parser.add_argument(
        "input_csv", 
        help="Path to input CSV file"
    )
    parser.add_argument(
        "-o", "--output", 
        help="Path to output JSON file (optional, defaults to input filename with .json extension)"
    )
    
    args = parser.parse_args()
    
    try:
        csv_to_json_with_context(args.input_csv, args.output)
    except Exception as e:
        print(f"Conversion failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
