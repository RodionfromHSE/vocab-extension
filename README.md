# Vocabulary Extension

A comprehensive toolkit for capturing, enriching, and learning new vocabulary words.

## Table of Contents

- [Vocabulary Extension](#vocabulary-extension)
- [Overview](#overview)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
- [Architecture](#architecture)
- [Usage](#usage)
  - [Running the Complete Pipeline](#running-the-complete-pipeline)
  - [Pipeline Options](#pipeline-options)
- [Components Configuration](#components-configuration)
  - [Word Saver App](#word-saver-app)
  - [Meta Generator](#meta-generator)
  - [Audio Component](#audio-component)
  - [Flashcard Converter](#flashcard-converter)
  - [Dataset Converter](#dataset-converter)
- [Pipeline Configuration](#pipeline-configuration)
- [Customization](#customization)
  - [Input Data Format](#input-data-format)
  - [Customizing the AI Prompt](#customizing-the-ai-prompt)
  - [Flashcard Templates](#flashcard-templates)
  - [Text-to-Speech Language](#text-to-speech-language)
- [Troubleshooting](#troubleshooting)
  - [Word Saver App](#word-saver-app-1)
  - [Meta Generator](#meta-generator-1)
  - [Audio Component](#audio-component-1)
  - [Flashcard Converter](#flashcard-converter-1)
- [Component Documentation](#component-documentation)
- [TODO](#todo)


## Overview

Vocabulary Extension is a modular application designed to help you learn new words more effectively. It provides a complete workflow from capturing vocabulary items to creating rich, multimedia flashcards for spaced repetition learning.

The project consists of several interconnected components that can be used together as a pipeline or independently:

- **Word Saver App**: A background application that captures words via a global hotkey
- **Meta Generator**: Enriches basic word entries with detailed metadata using AI (OpenAI API)
- **Audio Component**: Generates audio files for vocabulary words using text-to-speech
- **Flashcard Converter**: Transforms enriched vocabulary data into Anki flashcards
- **Dataset Converter**: Utility for merging and validating JSON files

## Getting Started

### Prerequisites

- Python 3.10+ (recommended)
- Poetry for dependency management
- OpenAI API key (for meta generation)
- Anki desktop application with AnkiConnect add-on (for flashcard creation)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd vocab_extension
   ```

2. Install dependencies:
   ```bash
   poetry install
   eval $(poetry env activate)
   ```

### Environment Variables

Set the following environment variables:

```bash
# Required for main pipeline
export VOCAB_EXTENSION_DATA_FOLDER="~/Documents/vocab_extension_data"
export OPENAI_API_KEY="your-openai-api-key"

# Required for Word Saver App
export WORD_SAVER_SAVE_DIRECTORY="~/Documents/word_saver"
```

## Architecture

Vocabulary Extension follows a modular architecture where each component handles a specific part of the vocabulary learning workflow:

1. **Word Collection**: The Word Saver App is a background application that listens for a global hotkey (<cmd>+<shift>+p by default) while browsing in Yandex Browser. When activated, it opens a dialog to save the word and its context.

2. **Data Aggregation**: The Dataset Converter merges individual JSON files created by the Word Saver App into a single dataset, validating that each contains the required fields.

3. **Enrichment**: The Meta Generator uses the OpenAI API to transform basic word entries into comprehensive vocabulary resources with definitions, examples, synonyms, etc.

4. **Audio Creation**: The Audio Component converts text to speech using Google TTS, generating MP3 files for pronunciation practice and embedding in flashcards.

5. **Flashcard Generation**: The Flashcard Converter creates Anki flashcards using customizable templates, automatically uploading them to your Anki collection.

## Usage

### Running the Complete Pipeline

The simplest way to use Vocabulary Extension is with the integrated pipeline:

```bash
python run_pipeline.py
```

This will:
1. Convert your saved word data into a single dataset (Dataset Converter component)
2. Enrich the words with comprehensive metadata using AI (Meta Generator component)
3. Generate audio files for each word (Audio Component)
4. Create and upload flashcards to Anki (Flashcard Converter component)

### Pipeline Options

You can run selective parts of the pipeline using command-line flags:

```bash
# Skip specific steps
python run_pipeline.py --skip-dataset
python run_pipeline.py --skip-meta
python run_pipeline.py --skip-audio
python run_pipeline.py --skip-flashcard

# Use a custom configuration file
python run_pipeline.py --config custom_pipeline_config.yaml
```

## Components Configuration

### Word Saver App

The Word Saver App runs in the background, listening for a global hotkey to capture vocabulary items. It can be compiled into a standalone application using py2app for macOS.

**Configuration**: Edit `word_saver_app/app/config.py`

```python
# Applications where the hotkey will work
ALLOWED_APPLICATIONS = ["yandex", "yandex browser", "yandexbrowser"]

# The hotkey combination to trigger the popup
HOTKEY = "<cmd>+<shift>+p"  # Global hotkey string format

# Directory where the word data is saved
SAVE_DIRECTORY = get_save_directory()  # Uses WORD_SAVER_SAVE_DIRECTORY env var or defaults to ~/Documents/word_saver
```

**Running the App**:
```bash
# Run as a script
cd word_saver_app
python main.py

# Build as a standalone app for macOS
cd word_saver_app
python setup.py py2app
```

### Meta Generator

The Meta Generator enriches basic vocabulary words with detailed information.

**Configuration**: Edit `meta_generator/config.yaml`

```yaml
api:
  type: "openai"           # API provider (currently only OpenAI)
  key: "your-api-key"      # Can use OPENAI_API_KEY env var instead
  model: "gpt-3.5-turbo"   # Model to use for generation
  params:
    temperature: 0.7       # Controls randomness (0.0-1.0)
    max_tokens: 1000       # Maximum response length

prompt_path: "prompt.md"   # Path to prompt template
input: "data/words.json"   # Default input file path
output: "data/words_enriched.json" # Default output path
```

**Prompt Template**: The `prompt.md` file defines the structure of the AI-generated metadata. Single curly braces are used for variables to be replaced from input data, while double curly braces are used to escape curly braces in JSON templates.

**Running Independently**:
```bash
cd meta_generator
python main.py --input "data/words_raw.json" --output "data/words_enriched.json"

# Process all entries
python main.py --input "data/words_raw.json" --all
```

### Audio Component

The Audio Component generates MP3 files for vocabulary words.

**Configuration**: Edit `audio_component/config.yaml`

```yaml
language: en  # Language code for text-to-speech (e.g., en, fr, es, de)
save_directory: ~/Library/Application Support/Anki2/User 1/collection.media  # Where audio files will be stored
media_subdirectory: vocab_extension  # Subfolder for organizing generated files
```

**Running Independently**:
```bash
cd audio_component
python main.py input.json --output-file output.json --config config.yaml
```

### Flashcard Converter

The Flashcard Converter transforms enriched data into Anki flashcards.

**Configuration**: Edit `flashcard_converter/config.yaml`

```yaml
input_file: "data/meta.json"  # Path to the enriched vocabulary data
deck_name: "Vocabulary Extension"  # Name of the Anki deck to create/populate
flashcard_template:  # Defines the structure of the flashcards
  - front: "{word} - {example}"  # Content for the front of the card
    back: "{definition} [sound:{audio_relative_path}]"  # Content for the back of the card
```

**Running Independently**:
```bash
cd flashcard_converter
python main.py
```

**Anki Integration**: Ensure Anki is running with the AnkiConnect add-on installed (code: 2055492159)

### Dataset Converter

The Dataset Converter merges individual JSON files from the Word Saver App.

**Running Independently**:
```bash
python other/dataset_convertor.py input_folder output_file.json
```

## Pipeline Configuration

The main pipeline is configured via `pipeline_config.yaml`:

```yaml
pipeline_name: "en_custom"  # Name of the pipeline configuration
data_folder: ${oc.env:VOCAB_EXTENSION_DATA_FOLDER}/${pipeline_name}  # Where data will be stored

root: "/path/to/vocab_extension"  # Root directory of the project

dataset_converter:
  input_dir: "${oc.env:WORD_SAVER_SAVE_DIRECTORY}"  # Directory with raw word JSON files
  output_file: "${data_folder}/words_raw.json"  # Path for the merged dataset

meta_generator:
  config_file: "${root}/meta_generator/config.yaml"  # Meta generator configuration
  input_file: ${dataset_converter.output_file}  # Takes output from dataset converter
  output_file: "${data_folder}/words_enriched.json"  # Path for enriched data

audio_generator:
  config_file: "${root}/audio_component/config.yaml"  # Audio generator configuration
  input_file: ${meta_generator.output_file}  # Takes output from meta generator
  output_file: "${data_folder}/words_enriched_with_audio.json"  # Path for data with audio paths

flashcard_converter:
  config_file: "${root}/flashcard_converter/config.yaml"  # Flashcard converter configuration
  input_file: ${audio_generator.output_file}  # Takes output from audio generator
```

## Customization

### Input Data Format

For the dataset converter, each JSON file should contain:
```json
{
  "word": "example",
  "context": "This is an example sentence."
}
```

These are the required fields for the pipeline to work correctly.

### Customizing the AI Prompt

To change the metadata structure, edit `meta_generator/prompt.md`. The prompt template uses a special syntax:

- Use single curly braces for variables to be replaced from input data (e.g., `{word}`)
- Use double curly braces for escaping curly braces in JSON examples within the prompt (e.g., `{{` and `}}`)

For example:
```
Format your response as valid JSON:

```json
{{
  "word": "{word}",
  "definition": "A clear definition here"
}}
```
```

### Flashcard Templates

Modify the `flashcard_template` in `flashcard_converter/config.yaml` to customize your flashcards:
```yaml
flashcard_template:
  - front: "{word}"  # Shows just the word on the front
    back: "{definition}\n\n{example}\n\n[sound:{audio_relative_path}]"  # Definition, example, and audio on back
  - front: "{example} (with blank)"  # Shows example with word blanked out
    back: "The word is: {word}\n{definition}"  # Reveals word and definition
```

This example creates two types of cards for each vocabulary item. You can reference any field from your enriched JSON data.

### Text-to-Speech Language

Change the `language` parameter in `audio_component/config.yaml` to generate speech in different languages:
```yaml
language: fr  # French
```

Supported language codes include: en, fr, es, de, it, ja, ko, etc.

## Troubleshooting

### Word Saver App
- If the hotkey doesn't work, check `ALLOWED_APPLICATIONS` in the config
- Make sure the save directory exists
- Run the tests to diagnose issues: `cd word_saver_app && pytest tests/`
- If using the compiled application and experiencing issues, try running as a script for more verbose output

### Meta Generator
- For incomplete responses, increase `max_tokens` in the configuration
- API errors may indicate rate limiting - adjust retry settings in `src/handler/generation_handler.py`

### Audio Component
- Ensure you have internet connectivity for Google TTS
- Verify the save directory exists and is writable

### Flashcard Converter
- Ensure Anki is running with the AnkiConnect add-on installed
- Check that your template only references fields that exist in your data

## Component Documentation

For detailed information about each component, please refer to their individual README files:

- Audio Component: [audio_component/README.md](audio_component/README.md)
- Flashcard Converter: [flashcard_converter/README.md](flashcard_converter/README.md)
- Meta Generator: [meta_generator/README.md](meta_generator/README.md)
- Word Saver App: [word_saver_app/README.md](word_saver_app/README.md)

## TODO

* Move the components into separate folder
* Add info on integration test into README.md
* Replace poetry with just requirements.txt in component folders (to avoid poetry messing up with the environment)
* Add a demo video