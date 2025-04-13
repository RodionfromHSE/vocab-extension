# Vocabulary Meta Generator

## Overview

The Vocabulary Meta Generator enriches vocabulary words with comprehensive information using AI. It transforms basic word entries into structured data containing definitions, examples, synonyms, antonyms, and more.

## How It Works

**Input (JSON file):**
```json
[
  {
    "word": "example",
    "part_of_speech": "noun",
    "translation": "an instance that illustrates something"
  }
]
```

**Output (Enriched JSON):**
```json
{
  "word": "example",
  "part_of_speech": "noun",
  "definition": "A representation or instance of something that serves to illustrate a concept or principle.",
  "examples": [
    "This painting is an example of cubist art.",
    "The teacher provided an example to help students understand the concept.",
    "His behavior is a perfect example of good sportsmanship."
  ],
  "synonyms": ["instance", "sample", "illustration", "case", "demonstration"],
  "antonyms": ["exception", "anomaly", "deviation"],
  "etymology": "From Latin 'exemplum', meaning 'sample' or 'pattern'.",
  "collocations": ["clear example", "perfect example", "set an example", "follow the example of", "give an example"]
}
```

## Features

- **Powerful Enrichment**: Transform simple word entries into comprehensive vocabulary resources
- **Batch Processing**: Process entire word lists in JSON format
- **Flexible Configuration**: Easy to configure with API settings, prompt adjustments, and processing parameters
- **Modular Architecture**: Well-structured codebase that's easy to extend and modify
- **Error Handling**: Robust retry mechanisms and error handling for reliable processing
- **Structured Output**: Returns clean JSON data ready for use in applications

## Installation

### Prerequisites

- Python 3.8 or higher
- Poetry (recommended)

### Setup with Poetry

```bash
# Clone the repository
git clone <repository-url>
cd vocab_extension/meta_generator

# Install dependencies with Poetry
poetry install

# Activate the virtual environment
poetry shell
```

## Configuration

### OpenAI API Setup

You need an OpenAI API key to use this tool. You can provide it in one of two ways:

1. **Environment Variable (Recommended)**:
   ```bash
   # On macOS/Linux
   export OPENAI_API_KEY="your-api-key-here"
   
   # On Windows (PowerShell)
   $env:OPENAI_API_KEY="your-api-key-here"
   ```

2. **Configuration File**:
   Edit `config.yaml` and add your API key:
   ```yaml
   api:
     type: "openai"
     key: "your-api-key-here"
     model: "gpt-3.5-turbo"
     params:
       temperature: 0.7
       max_tokens: 1000
   ```

### General Configuration

The `config.yaml` file controls model parameters, API settings, and processing options:

```yaml
api:
  type: "openai"
  model: "gpt-3.5-turbo"  # Change to a different model if needed
  params:
    temperature: 0.7
    max_tokens: 1000  # Increase if responses are incomplete
prompt_path: "prompt.md"
handler:
  retries: 3
  sleep_time: 2
```

### Customizing the Prompt Template

The `prompt.md` file defines how the model generates word information. You can modify this file to change the output structure or the type of information requested.

Important considerations:
- Make sure to escape curly braces `{` and `}` when writing JSON templates in the prompt
- Use double curly braces for template parts that should appear in the final prompt (e.g., `{{word}}`)
- Use single curly braces for variables to be replaced from input data (e.g., `{word}`)

Example section from `prompt.md`:
```
Format your response as a valid JSON object with the following structure:

```json
{{
  "word": "{{word}}",
  "part_of_speech": "{{part_of_speech}}",
  "definition": "Clear definition here",
  "examples": [
    "First example sentence",
    "Second example sentence",
    "Third example sentence"
  ]
}}
```
```

## Usage

### Process a JSON File of Words

```bash
python main.py --file "data/words_raw.json" --output "data/words_enriched.json"
```

The input JSON file should have this structure:
```json
[
  {
    "word": "example",
    "part_of_speech": "noun",
    "translation": "an instance that illustrates something"
  },
  {
    "word": "sample",
    "part_of_speech": "noun",
    "translation": "a small part of something"
  }
]
```

## Troubleshooting

### Common Issues

1. **Incomplete JSON Responses**: If the model returns incomplete JSON:
   - Increase the `max_tokens` parameter in the configuration
   - Simplify the requested output structure in the prompt template

2. **Prompt Template Issues**: Ensure curly braces are properly escaped in JSON examples within the prompt template

3. **API Rate Limiting**: When processing large datasets, adjust the retry settings in the configuration:
   ```yaml
   handler:
     retries: 5
     sleep_time: 10
   ```

## Extending the Tool

The modular architecture makes the tool easy to extend:

1. **Add New Models**: Implement a new model in `src/model/` by extending `BaseModel`
2. **Custom Processors**: Create additional processors in `src/processors/` by extending `BaseProcessor`
3. **Different Validators**: Add new validators in `src/validators/` by extending `BaseValidator`