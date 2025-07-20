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
- **Multiple AI Providers**: Support for both OpenAI and Nebius AI Studio (DeepSeek models)
- **Batch Processing**: Process entire word lists in JSON format
- **Flexible Configuration**: Easy to configure with API settings and prompt adjustments
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

### API Setup

This tool supports two AI providers:

#### OpenAI API Setup

You need an OpenAI API key to use OpenAI models. You can provide it in one of two ways:

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

#### Nebius AI Studio Setup (DeepSeek Models)

You need a Nebius AI Studio API key to use DeepSeek models. You can provide it in one of two ways:

1. **Environment Variable (Recommended)**:
   ```bash
   # On macOS/Linux
   export NEBIUS_API_KEY="your-nebius-api-key-here"
   
   # On Windows (PowerShell)
   $env:NEBIUS_API_KEY="your-nebius-api-key-here"
   ```

2. **Configuration File**:
   Edit `config.yaml` and add your API key:
   ```yaml
   api:
     type: "nebius"
     key: "your-nebius-api-key-here"
     model: "deepseek-ai/DeepSeek-V3-0324"
     base_url: "https://api.studio.nebius.ai/v1"  # Optional, this is the default
     params:
       temperature: 0.7
       max_tokens: 1000
       timeout: 30
   ```

### Detailed Configuration Reference

The `config.yaml` file includes essential API settings, the prompt path, and default input/output paths. This provides both flexibility and convenience.

**OpenAI Configuration Example:**
```yaml
api:
  type: "openai"           # The API provider to use
  model: "gpt-3.5-turbo"   # The specific model to use for generation
  params:                  # Model-specific parameters
    temperature: 0.7       # Controls randomness (0.0 = deterministic, 1.0 = creative)
    max_tokens: 1000       # Maximum length of the generated response
prompt_path: "prompt.md"   # Path to the prompt template file
input: "data/words.json"   # Default input file path (optional)
output: "data/words_enriched.json" # Default output file path (optional)
```

**Nebius Configuration Example:**
```yaml
api:
  type: "nebius"                              # The API provider to use
  model: "deepseek-ai/DeepSeek-V3-0324"      # The specific DeepSeek model to use
  base_url: "https://api.studio.nebius.ai/v1" # Nebius API endpoint (optional)
  params:                                     # Model-specific parameters
    temperature: 0.7                          # Controls randomness
    max_tokens: 1000                          # Maximum length of the generated response
    timeout: 30                               # Request timeout in seconds
prompt_path: "prompt.md"   # Path to the prompt template file
input: "data/words.json"   # Default input file path (optional)
output: "data/words_enriched.json" # Default output file path (optional)
```

#### API Configuration Fields:

| Field | Description | Default | Notes |
|-------|-------------|---------|-------|
| `api.type` | The API provider to use | `"openai"` | Supported: `"openai"`, `"nebius"` |
| `api.key` | Your API key | None | Can be provided via environment variable instead |
| `api.model` | The model to use | `"gpt-3.5-turbo"` | OpenAI: `"gpt-3.5-turbo"`, `"gpt-4"`, etc.<br>Nebius: `"deepseek-ai/DeepSeek-V3-0324"` |
| `api.base_url` | API endpoint URL | Auto-detected | Nebius: `"https://api.studio.nebius.ai/v1"`<br>OpenAI: Uses default OpenAI endpoint |
| `api.params.temperature` | Controls output randomness | `0.7` | Range: 0.0-1.0 (lower is more deterministic) |
| `api.params.max_tokens` | Maximum response length | `1000` | Increase for more complex/lengthy responses |
| `api.params.timeout` | Request timeout in seconds | `30` | Nebius-specific, controls API call timeout |
| `prompt_path` | Path to prompt template | `"prompt.md"` | Can be absolute or relative path |
| `input` | Default input file path | `"data/words.json"` | Can be overridden with --input/-i option |
| `output` | Default output file path | `"data/words_enriched.json"` | Can be overridden with --output/-o option |

### Global Configuration Constants

Instead of using the configuration file for every setting, we've moved certain operational parameters into code-level constants.

#### Handler Constants (in `generation_handler.py`):

```python
# Default handler settings for retry behavior
DEFAULT_RETRIES = 3        # Number of retry attempts for API calls
DEFAULT_SLEEP_TIME = 2     # Delay between retries in seconds
```

These constants control the retry behavior when API calls fail. The generator will:
- Make up to `DEFAULT_RETRIES` attempts to get a valid response
- Wait `DEFAULT_SLEEP_TIME` seconds between each attempt
- Log detailed information about each failure
- Raise the final error if all attempts fail

#### Validator Constants (in `json_response_validator.py`):

```python
# Default validator settings for JSON schema validation
DEFAULT_REQUIRE_SCHEMA = False     # Whether a schema is required for validation
DEFAULT_SCHEMA_PATH = ""           # Default path to JSON schema file
```

These constants control JSON validation behavior:
- `DEFAULT_REQUIRE_SCHEMA`: When `True`, responses must match a provided schema
- `DEFAULT_SCHEMA_PATH`: Path to a JSON schema file for validation

#### When to Modify Constants vs. Config File

- **Modify config.yaml when**:
  - Changing API credentials
  - Adjusting model parameters
  - Using different prompt templates
  - Changing default input/output paths

- **Modify code constants when**:
  - Changing system behavior (like retry logic)
  - Implementing different validation requirements
  - Extending the tool with new capabilities

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
# Using the command line options
python main.py --input "data/words_raw.json" --output "data/words_enriched.json"

# Using the short form options
python main.py -i "data/words_raw.json" -o "data/words_enriched.json"

# Using default paths from config.yaml
python main.py

# Process all entries in the file
python main.py --input "data/words_raw.json" --all
# or with short form
python main.py -i "data/words_raw.json" -all
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

### Command-Line Options

The entry script uses Click for command-line interface management:

| Option | Short | Description | Required | Default |
|--------|-------|-------------|----------|---------|
| `--config` | | Path to configuration file | No | `"config.yaml"` |
| `--input` | `-i` | Path to input JSON file | No* | Value from config.yaml |
| `--output` | `-o` | Path for output JSON file | No | Value from config or input filename with `_enriched` suffix |
| `--all` | `-all` | Process all entries in the input file | No | `False` |

*Either `--input`/`-i` or the `input` field in the config file must be provided.

## Troubleshooting

### Common Issues

1. **Incomplete JSON Responses**: If the model returns incomplete JSON:
   - Increase the `max_tokens` parameter in the configuration
   - Simplify the requested output structure in the prompt template
   - For Nebius models, also try increasing the `timeout` parameter

2. **Prompt Template Issues**: Ensure curly braces are properly escaped in JSON examples within the prompt template

3. **API Authentication Issues**:
   - **OpenAI**: Ensure your `OPENAI_API_KEY` environment variable is set or provided in config
   - **Nebius**: Ensure your `NEBIUS_API_KEY` environment variable is set or provided in config
   - Check that your API keys have the necessary permissions and credits

4. **API Rate Limiting**: When processing large datasets, you may need to modify the retry settings in the `src/handler/generation_handler.py` file by adjusting the `DEFAULT_RETRIES` and `DEFAULT_SLEEP_TIME` constants:
   ```python
   # For aggressive retry behavior with longer wait times
   DEFAULT_RETRIES = 5      # Increase number of attempts
   DEFAULT_SLEEP_TIME = 10  # Longer wait between retries (in seconds)
   ```

5. **Model-Specific Considerations**:
   - **DeepSeek models** (via Nebius) may have different response patterns compared to OpenAI models
   - If switching between providers, test your prompt template to ensure consistent output quality
   - Nebius models may require adjusting the `timeout` parameter for complex requests

6. **JSON Validation Issues**: If you need stricter JSON validation:
   - Create a JSON schema file
   - Modify the `DEFAULT_REQUIRE_SCHEMA` and `DEFAULT_SCHEMA_PATH` constants in `json_response_validator.py`

## Extending the Tool

The modular architecture makes the tool easy to extend:

1. **Add New Models**: Implement a new model in `src/model/` by extending `BaseModel` (see `openai_model.py` and `nebius_model.py` as examples)
2. **Custom Processors**: Create additional processors in `src/processors/` by extending `BaseProcessor`
3. **Different Validators**: Add new validators in `src/validators/` by extending `BaseValidator`

### Available Models

The tool currently includes two AI provider implementations:

- **OpenAI Model** (`openai_model.py`): Supports GPT models including GPT-3.5-turbo, GPT-4, etc.
- **Nebius Model** (`nebius_model.py`): Supports DeepSeek models via Nebius AI Studio's OpenAI-compatible API

Both models implement the same `BaseModel` interface, making it easy to switch between providers or add new ones.

## Example Usage

Check out the `example/` directory for sample input files and expected output files. Each example comes with a README explaining how to use it.