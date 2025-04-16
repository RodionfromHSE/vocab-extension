import os
import json
from typing import Any, Dict, List
import click

REQUIRED_KEYS = {"word", "context"}
DEFAULT_OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "data", "words_raw.json")
DEFAULT_OUTPUT_FILE = os.path.abspath(DEFAULT_OUTPUT_FILE)

def is_valid_json_content(data: Dict[str, Any]) -> bool:
    """Return True if JSON has exactly 'word' and 'context' keys."""
    return isinstance(data, dict) and set(data.keys()) == REQUIRED_KEYS

def read_json_file(file_path: str) -> Dict[str, Any]:
    """Read and return JSON content from a file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def combine_json_files(input_folder: str) -> List[Dict[str, Any]]:
    """Return a list of valid JSON objects from input_folder."""
    combined_data = []
    for filename in os.listdir(input_folder):
        if not filename.lower().endswith('.json'):
            continue  # Skip non-JSON files
        
        file_path = os.path.join(input_folder, filename)
        try:
            data = read_json_file(file_path)
        except json.JSONDecodeError:
            click.echo(f"Skipping file {filename}: invalid JSON format.")
            continue
        except Exception as e:
            click.echo(f"Error reading file {filename}: {e}")
            continue
        
        if is_valid_json_content(data):
            combined_data.append(data)
        else:
            click.echo(f"Skipping file {filename}: missing required keys.")
    
    return combined_data

@click.command()
@click.argument("input_folder", type=click.Path(exists=True, file_okay=False), default=os.environ.get("WORD_SAVER_SAVE_DIRECTORY"))
@click.argument("output_file", type=click.Path(writable=True, dir_okay=False), default=DEFAULT_OUTPUT_FILE)
def main(input_folder: str, output_file: str) -> None:
    """Combine valid JSON files from input_folder into output_file."""
    data = combine_json_files(input_folder)
    
    try:
        with open(output_file, 'w', encoding='utf-8') as out_f:
            json.dump(data, out_f, ensure_ascii=False, indent=4)
        click.echo(f"Successfully combined {len(data)} file(s) into '{output_file}'.")
    except Exception as e:
        click.echo(f"Failed to write to '{output_file}': {e}")

if __name__ == '__main__':
    main()
