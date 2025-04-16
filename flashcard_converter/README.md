# Flashcard Converter

A simple tool to convert a JSON file with meta information into Anki flashcards using a configuration file.

## Overview

This tool allows you to:
- Define flashcard templates in a YAML configuration file
- Process JSON data to generate flashcards based on these templates
- Automatically add the flashcards to an Anki deck

## Prerequisites

- Python 3.10+
- Anki desktop application
- AnkiConnect add-on installed in Anki

## Installation


1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Make sure the AnkiConnect add-on is installed in Anki:
   - Open Anki
   - Go to Tools > Add-ons > Get Add-ons
   - Enter code: 2055492159
   - Restart Anki

## Configuration

Edit the `config.yaml` file to set:
- `input_file`: Path to your JSON data file
- `deck_name`: Name of the Anki deck to create/populate
- `flashcard_template`: Define how your flashcards should be formatted

Example configuration:
```yaml
input_file: "data/meta.json"
deck_name: "My Vocabulary Deck"
flashcard_template:
  - front: "{word} - {example}"
    back: "{definition} [sound:{audio}]"
```

## Input Data Format

The input JSON file should contain an array of objects with the fields you want to use in your flashcards:

```json
[
  {
    "word": "ephemeral",
    "definition": "Lasting for a very short time.",
    "example": "The ephemeral nature of fashion trends.",
    "audio": "ephemeral.mp3"
  },
  ...
]
```

*Note:* The keys in the JSON objects should match the placeholders used in your YAML configuration. \
Though, you're not obligated to use the keys as above (they are for demonstration purposes).

## Usage

1. Make sure Anki is running with the AnkiConnect add-on
2. Run the converter:
   ```
   python main.py
   ```

## Templating

The converter uses the `smart_format` function to replace placeholders in templates with values from your data:

- Use `{field_name}` syntax to reference fields from your JSON data
- For media files (like audio), use the Anki syntax: `[sound:{audio}]`

## Troubleshooting

- **"Cannot connect to Anki"**: Make sure Anki is running and the AnkiConnect add-on is installed
- **"Missing key in record"**: Check that your template only references fields that exist in your JSON data
- **"Invalid JSON format"**: Verify your input JSON file is properly formatted

## License

[MIT License](LICENSE)