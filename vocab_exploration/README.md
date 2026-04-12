# Vocabulary Exploration - Complete Workflow to Anki Deck

This directory contains a complete workflow for converting vocabulary words from CSV format to a fully-featured Anki deck with metadata, audio, and flashcards.

## Overview

The workflow transforms vocabulary data through several stages:
1. **CSV Input** → **JSON Format** (compatible with metagenerator)
2. **JSON** → **Enriched JSON** (with definitions, translations, examples)
3. **Enriched JSON** → **JSON with Audio** (with generated speech files)
4. **JSON with Audio** → **Anki Deck** (with flashcards and templates)

## Files in this Directory

- `new_words_sample.csv` - Original vocabulary data with fields: word, guideword, level, pos, topic
- `new_words_sample.json` - Converted JSON format for metagenerator
- `new_words_sample_enriched.json` - Enriched with definitions, translations, examples
- `new_words_sample_with_audio.json` - Final JSON with audio file paths
- `prompt.md` - Custom prompt template for vocabulary metadata generation
- `config.yaml` - Metagenerator configuration
- `audio_config.yaml` - Audio component configuration
- `flashcard_config.yaml` - Flashcard converter configuration

## Step-by-Step Workflow

### Prerequisites

1. **Virtual Environment**: Ensure you have activated the virtual environment in the root folder:
   ```bash
   cd /path/to/vocab_extension
   source venv/bin/activate
   ```

2. **Anki Setup**: Make sure Anki is running with AnkiConnect addon installed

3. **Dependencies**: All components should have their dependencies installed via poetry

### Step 1: Convert CSV to JSON

If you have a CSV file with vocabulary words, convert it to JSON format:

```python
# Create a script similar to the deleted convert_csv_to_json.py
import csv
import json

def convert_csv_to_json(csv_path, json_path):
    words = []
    with open(csv_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            context_parts = []
            if row["guideword"]:
                context_parts.append(f"guideword: {row['guideword']}")
            context_parts.append(f"level: {row['level']}")
            context_parts.append(f"pos: {row['pos']}")
            if row["topic"]:
                context_parts.append(f"topic: {row['topic']}")
            
            context = ", ".join(context_parts)
            
            word_entry = {
                "word": row["word"],
                "context": context
            }
            words.append(word_entry)
    
    with open(json_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(words, jsonfile, indent=2, ensure_ascii=False)

# Usage
convert_csv_to_json("your_words.csv", "your_words.json")
```

### Step 2: Generate Metadata

Generate enriched metadata using the metagenerator:

```bash
cd /path/to/vocab_extension
source venv/bin/activate
cd meta_generator
python main.py --config ../vocab_exploration/config.yaml --input ../vocab_exploration/your_words.json --output ../vocab_exploration/your_words_enriched.json
```

**Configuration**: The `config.yaml` uses:
- Custom prompt template that handles CEFR levels, parts of speech, topics, and guidewords
- Nebius API for text generation
- Context-aware definitions and examples

### Step 3: Generate Audio

Generate audio files for the vocabulary words:

```bash
cd /path/to/vocab_extension/audio_component
poetry run python main.py --config ../vocab_exploration/audio_config.yaml
```

**Configuration**: The `audio_config.yaml`:
- Uses Google Text-to-Speech (gTTS)
- Saves audio files to Anki's media directory
- Creates both absolute and relative path references

### Step 4: Create Anki Deck

Convert the enriched data with audio to an Anki deck:

```bash
cd /path/to/vocab_extension
source venv/bin/activate
cd flashcard_converter
python main.py --config ../vocab_exploration/flashcard_config.yaml
```

**Configuration**: The `flashcard_config.yaml` creates:
- Deck name: "English General"
- Two flashcard templates:
  1. **Russian → English**: Shows Russian word/example, reveals English with audio
  2. **English → Russian**: Shows English word/example, reveals Russian with audio

## Flashcard Templates

### Template 1: Russian to English
- **Front**: Russian word, Russian example, English definition
- **Back**: English word, English example, audio pronunciation

### Template 2: English to Russian  
- **Front**: English word, English example
- **Back**: Russian word, Russian example, audio pronunciation

## Customization

### Modifying the Prompt
Edit `prompt.md` to change how definitions and examples are generated. The prompt considers:
- CEFR level (A1-C2) for appropriate complexity
- Part of speech for accurate definitions
- Topic context for relevant examples
- Guidewords for context-specific meanings

### Changing Audio Settings
Edit `audio_config.yaml` to modify:
- Language (`en` for English)
- Audio file location
- Media subdirectory name

### Customizing Flashcards
Edit `flashcard_config.yaml` to:
- Change deck name
- Modify template layouts
- Add or remove flashcard types
- Adjust field mappings

## Output

The final result is an Anki deck named "English General" containing:
- ✅ **Rich metadata**: Definitions, examples, translations
- ✅ **Audio pronunciation**: Generated TTS for each word
- ✅ **Multiple templates**: Both directions (EN→RU, RU→EN)
- ✅ **Context-aware content**: Considers CEFR level, topic, part of speech
- ✅ **Professional formatting**: Clean, consistent flashcard layout

## Troubleshooting

1. **Import errors**: Ensure virtual environment is activated and dependencies installed
2. **File not found**: Check file paths in configuration files are relative to the component directory
3. **AnkiConnect errors**: Ensure Anki is running with AnkiConnect addon
4. **Audio generation fails**: Check internet connection for gTTS API calls
5. **Missing __init__.py**: Some components may need `__init__.py` files in their src directories

## Example Data Flow

```
new_words_sample.csv (4 words)
    ↓ (convert_csv_to_json)
new_words_sample.json (word + context)
    ↓ (metagenerator)  
new_words_sample_enriched.json (+ definitions, translations, examples)
    ↓ (audio_component)
new_words_sample_with_audio.json (+ audio file paths)
    ↓ (flashcard_converter)
"English General" Anki Deck (8 flashcards: 4 words × 2 templates)
```

This workflow can be scaled to process larger vocabulary datasets by simply providing different input files to each step.
