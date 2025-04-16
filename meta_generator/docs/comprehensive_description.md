# Vocabulary Meta Generator  
*A Comprehensive Developer Guide*

The Vocabulary Meta Generator is a flexible tool designed to generate custom meta information for vocabulary entries (or any other data). Unlike a fixed output format limited to definitions, examples, or synonyms, the tool allows users to tailor the output according to their prompt templates and configuration. This means you can generate any meta details you need by simply modifying the prompt and settings.

---

## Table of Contents

1. [Project Purpose & Overview](#project-purpose--overview)
2. [Project Structure](#project-structure)
3. [Core Modules & Their Responsibilities](#core-modules--their-responsibilities)
   - [Handler](#handler)
   - [Model](#model)
   - [Processors](#processors)
   - [Prompter](#prompter)
   - [Validators](#validators)
   - [Utilities](#utilities)
4. [Configuration Details](#configuration-details)
5. [Usage Examples](#usage-examples)
6. [Important Notes & Extension Points](#important-notes--extension-points)

---

## Project Purpose & Overview

The primary aim of the Vocabulary Meta Generator is to generate meta information for vocabulary (or other types of) entries in a customizable way. Rather than being limited to a pre-defined structure such as definitions, examples, synonyms, antonyms, etymology, and collocations, the output is determined by your prompt template.  
This means you can freely define what meta information you require:  
- Custom explanations  
- Context-specific examples  
- Any additional details in a structured JSON format

The built-in prompt (in `prompt.md`) currently generates a specific type of meta information, but you can change it to suit your needs. This flexibility is at the core of the project.

---

## Project Structure

Below is an overview of the entire project structure. This makes it easy to navigate and understand where to find various components of the tool:

```
.github/
  └─ copilot-instructions.md         # Developer instructions for integrating with Copilot
example/
  ├─ config.yaml                      # Example configuration file
  ├─ prompt.md                        # Example prompt template for meta generation
  └─ README.md                        # Readme for examples usage
src/
  ├─ handler/                         # Orchestrates the generation process
  │   ├─ __init__.py                  
  │   ├─ base_handler.py               # Abstract workflow definition
  │   └─ generation_handler.py         # Implements the meta generation workflow including retries
  ├─ model/                           # Contains text generation models
  │   ├─ __init__.py
  │   ├─ base_model.py                 # Defines a common interface for models
  │   └─ openai_model.py               # OpenAI API implementation (extendable by adding your own models)
  ├─ processors/                      # Handles processing of model responses
  │   ├─ __init__.py
  │   ├─ base_processor.py             # Abstract processor interface
  │   ├─ codeblock_extractor_processor.py  # Extracts content from markdown code blocks (e.g., ```json blocks)
  │   └─ default_processor.py          # Tries to parse the response as JSON directly
  ├─ prompter/                        # Loads and formats prompt templates
  │   ├─ __init__.py
  │   └─ template_prompter.py          # Reads the prompt file and substitutes input variables
  ├─ utils/                           # Utility functions
  │   ├─ __init__.py
  │   ├─ config.py                     # Reads and resolves YAML configuration files
  │   └─ smart_format.py               # Handles strict string formatting and variable extraction
  └─ validators/                      # Ensures the generated output meets expected criteria
      ├─ __init__.py
      ├─ base_validator.py             # Abstract validator interface
      ├─ default_validator.py          # Basic existence check for output
      └─ json_response_validator.py    # Validates and optionally enforces JSON schema (extendable)
tests/
  ├─ model/
  │   ├─ __init__.py
  │   ├─ test_base_model.py           # Tests for base model functionality
  │   └─ test_openai_model.py         # Tests for OpenAI model integration
  ├─ utils/
  │   ├─ test_config.py               # Tests configuration utilities
  │   └─ test_smart_format.py         # Tests for the smart string formatting functions
  ├─ other test files                 # Tests for handler, processors, validators, and the prompter
  └─ __init__.py
config.yaml                           # Main configuration file for the generator
main.py                               # Main entry point to run the meta generation process
prompt.md                             # Default prompt template defining meta information output format
README.md                             # High-level overview and instructions for using the project
```

---

## Core Modules & Their Responsibilities

### Handler

- **Files:** `base_handler.py`, `generation_handler.py`  
- **Responsibilities:**  
  - **Workflow Orchestration:**  
    - Formats the prompt using the prompter.
    - Sends the prompt to the text generation model.
    - Processes the response through a processor.
    - Validates the resulting meta information.
  - **Error and Retry Logic:**  
    - Automatically retries failed generation attempts (default is 3 attempts) with a delay between tries.
    - Logs errors and warnings for diagnostics.

### Model

- **Files:** `base_model.py`, `openai_model.py`  
- **Responsibilities:**  
  - **Base Interface:**  
    - The abstract `BaseModel` class defines the interface for any text generation model.
  - **OpenAI Integration:**  
    - `OpenAIModel` implements the interface using the OpenAI API.
    - Constructs the request payload, handles authentication (via config or environment variable), and extracts the generated text.
- **Extensibility Note:**  
  - You can easily add your own models by extending `BaseModel` and implementing the required methods.

### Processors

- **Files:** `base_processor.py`, `codeblock_extractor_processor.py`, `default_processor.py`  
- **Responsibilities:**  
  - **Response Processing:**  
    - `BaseProcessor` defines the general interface.
    - `CodeBlockExtractorProcessor` searches for markdown code blocks (like ```json) in the response and extracts their content. This is especially useful when responses include extra explanatory text outside the desired JSON.
    - `DefaultProcessor` attempts to parse the entire response as JSON directly.
- **Extensibility Note:**  
  - New processors can be added by extending `BaseProcessor` to handle different response formats or processing logic.

### Prompter

- **Files:** `template_prompter.py`  
- **Responsibilities:**  
  - **Template Loading & Variable Substitution:**  
    - Reads a prompt template from a file (default: `prompt.md`).
    - Extracts required variables and substitutes them with user input.
    - Provides warnings if extra variables are provided.
  - **Dynamic Reload Capability:**  
    - Supports reloading the template in case it is updated externally.

### Validators

- **Files:** `base_validator.py`, `default_validator.py`, `json_response_validator.py`  
- **Responsibilities:**  
  - **Output Verification:**  
    - `BaseValidator` defines the required interface.
    - `DefaultValidator` checks for existence of output.
    - `JsonResponseValidator` confirms the output is valid JSON and, if needed, validates it against a JSON schema.
- **Extensibility Note:**  
  - You may extend validators by inheriting from `BaseValidator` to implement more complex validation schemes.

### Utilities

- **Files:** `config.py`, `smart_format.py`  
- **Responsibilities:**  
  - **Configuration Handling:**  
    - Loads and resolves configuration settings from a YAML file using OmegaConf.
  - **Smart String Formatting:**  
    - Performs strict variable substitutions in templates.
    - Extracts variable names and warns if unused variables are provided.

---

## Configuration Details

The primary configuration is done through the `config.yaml` file. Key parameters include:

- **api:**  
  - **type:**  
    - Specifies the API provider (e.g., `"openai"`).  
  - **key:**  
    - The authentication key; if not provided, the environment variable `OPENAI_API_KEY` is used.
  - **model:**  
    - Specifies the AI model to use (e.g., `"gpt-3.5-turbo"`).  
  - **params:**  
    - **temperature:** Determines randomness (e.g., `0.7` for balanced output).
    - **max_tokens:** Controls the maximum length of the output (set to `1000` for detailed responses).
    - **timeout:** (if applicable) Limits the API call duration.
- **prompt_path:**  
  - Path to the prompt template file (default is `prompt.md`), which defines how the meta information should be structured.
- **input & output:**  
  - **input:**  
    - The default path to the JSON input file containing the initial entries.
  - **output:**  
    - The default path where the enriched meta information will be saved.
  
These configuration values can be tailored to fit your environment and the specific meta details you wish to generate.

---

## Usage Examples

To run the meta generation process, simply execute the entry point. The configuration file handles default input and output paths.

- **Run with Default Settings:**
  ```bash
  python main.py
  ```

- **Override Input/Output Files (via command-line arguments):**
  ```bash
  python main.py --input "data/words_raw.json" --output "data/words_enriched.json"
  ```
  
The application will read each entry from the input file, generate the meta information using the custom prompt, and then write the enriched records to the output file while displaying a progress bar.

---

## Important Notes & Extension Points

- **Custom Meta Generation:**  
  The output is fully customizable. Modify the `prompt.md` template to define exactly what meta information is generated. This enables users to design output that best fits their use case.

- **Extending Core Components:**  
  - **Models:**  
    - You can add your own models by extending `BaseModel`. This makes it possible to integrate with other APIs or local models.
  - **Processors:**  
    - New processing methods can be implemented by creating subclasses of `BaseProcessor` for different output formats.
  - **Validators:**  
    - For more robust output checks, extend `BaseValidator` to add custom validation logic.
  
- **Error Handling & Logging:**  
  Robust retry mechanisms ensure that network or API hiccups are retried with a delay. Detailed logs are available to aid in troubleshooting.

- **Project Flexibility:**  
  With a modular design, each component of the system can be independently modified, extended, or replaced without affecting the overall workflow.
