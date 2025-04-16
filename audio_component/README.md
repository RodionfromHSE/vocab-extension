# Audio Companion Component

A standalone Python component that processes JSON files containing sentences, generates corresponding audio files using Google Text-to-Speech (gTTS), and updates the JSON with paths to the generated files.

## Features

- Convert sentences from JSON objects to MP3 audio files using Google Text-to-Speech (gTTS)
- Customizable configuration via YAML file (language, save directory, media subdirectory)
- Automatically creates necessary directories
- Updates JSON objects with both absolute and relative paths to generated audio files
- Handles errors gracefully
- Designed for integration with Anki media directories

## Setup and Installation

### Prerequisites

- Python 3.10+
- Poetry (dependency management)

### Installation

1. Clone the repository and navigate to the project directory:

```bash
git clone <repository-url>
cd audio-component
```

2. Install dependencies using Poetry:

```bash
poetry install
```

3. Activate the virtual environment:

```bash
poetry shell
```

## Configuration

The component uses a `config.yml` file to store settings. Example configuration:

```yaml
language: en
save_directory: ~/Library/Application Support/Anki2/User 1/collection.media
media_subdirectory: decca1
```

### Configuration Parameters

- `language`: The language code for text-to-speech (e.g., "en", "fr", "es")
- `save_directory`: The base directory where audio files will be stored (defaults to Anki Media Directory)
- `media_subdirectory`: A subfolder within the save directory for organizing generated files

## Usage

### Basic Usage

```bash
python main.py input.json
```

The component will:
1. Read the input JSON file
2. Generate an MP3 file for each sentence
3. Save the audio files to the specified directory
4. Update each JSON object with the paths to the corresponding audio file
5. Write the updated JSON to an output file (by default: `input_with_audio.json`)

### Command Line Options

```
usage: main.py [-h] [--output-file OUTPUT_FILE] [--config CONFIG] input_file

Audio Companion Component

positional arguments:
  input_file            Path to the input JSON file

optional arguments:
  -h, --help            Show this help message and exit
  --output-file OUTPUT_FILE
                        Path to the output JSON file (default: [input_file]_with_audio.json)
  --config CONFIG       Path to the configuration file (default: config.yml)
```

### Input JSON Format

The input JSON should be an array of objects, each containing at least a "sentence" field:

```json
[
  {
    "sentence": "Hello, how are you?",
    "other_field": "other_value"
  },
  {
    "sentence": "This is another sentence."
  }
]
```

### Output JSON Format

The output JSON will include the original data plus two additional fields for each object:

```json
[
  {
    "sentence": "Hello, how are you?",
    "other_field": "other_value",
    "audio_absolute_path": "/absolute/path/to/decca1/audio_0.mp3",
    "audio_relative_path": "decca1/audio_0.mp3"
  },
  {
    "sentence": "This is another sentence.",
    "audio_absolute_path": "/absolute/path/to/decca1/audio_1.mp3",
    "audio_relative_path": "decca1/audio_1.mp3"
  }
]
```

## Development

### Testing

Run the test suite with pytest:

```bash
pytest
```

### Adding Dependencies

To add a new dependency:

```bash
poetry add package-name
```

For development dependencies:

```bash
poetry add --dev package-name
```