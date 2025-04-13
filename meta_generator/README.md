# Text Generation Component

This component converts raw input (e.g., word entries with properties like word, part of speech, and translation) into enriched text (e.g., definitions, examples) by interfacing with OpenAI’s API. The output is a JSON-formatted result ready for downstream applications such as flashcard creation.

## Overview

- **Purpose:**  
  Generate enriched textual content from raw input using configurable prompts and robust error handling.
  
- **Key Features:**  
  - **Modular Design:** Decoupled layers including model API, prompt templating, response handling, post-processing, and validation.  
  - **Single Configuration:** A single `config.yaml` centralizes API settings, model parameters, and runtime behaviors.  
  - **External Prompt File:** Prompts are stored as Markdown in `prompt.md`, making prompt edits easy without touching code.
  - **Error Resilience:** Built-in retry logic, custom error handlers, and response validation ensure robustness against unstable APIs.

## Folder Structure

```
text-generation-component/
├── config.yaml                     # Component settings (API, model, handler parameters, prompt file path)
├── prompt.md                 # Markdown file containing the prompt template
├── main.py                         # Entry point script to run the generation workflow
├── README.md                       # This documentation file
├── requirements.txt                # Python dependency list
├── src/
│   ├── __init__.py
│   ├── model/                      # Contains the API model definitions
│   │   ├── __init__.py
│   │   ├── base_model.py           # Abstract base class defining text generation interface
│   │   └── openai_model.py         # OpenAI-specific implementation extending BaseModel
│   ├── prompter/                   # Handles prompt templating from the external Markdown file
│   │   ├── __init__.py
│   │   └── template_prompter.py    # Loads prompt.md, performs substitution (e.g., {word}, {part_of_speech})
│   ├── handler/                    # Manages API calls, retry logic, and error handling
│   │   ├── __init__.py
│   │   ├── base_handler.py         # Defines a generic handler interface for generation workflows
│   │   └── generation_handler.py   # Implements retry logic and orchestrates processing and validation
│   ├── processors/                 # Post-processes API responses (e.g., code block extraction)
│   │   ├── __init__.py
│   │   ├── base_processor.py       # Base class for response processing tasks
│   │   └── codeblock_extractor_processor.py  # Extracts valid JSON or cleaned text from code blocks
│   ├── validators/                # Validates processed responses
│   │   ├── __init__.py
│   │   ├── base_validator.py       # Base validator class interface
│   │   └── json_response_validator.py  # Confirms JSON validity and schema compliance
│   └── utils/                      # Utility functions used throughout the component
│       ├── __init__.py
│       └── smart_format.py         # Robust string substitution for prompt formatting
└── tests/                          # Unit and integration tests
    ├── __init__.py
    ├── test_base_model.py          # Tests for BaseModel and its implementations
    ├── test_template_prompter.py   # Validation for prompt templating and substitution
    ├── test_generation_handler.py  # Tests for retry logic and error scenarios in GenerationHandler
    └── test_processors_validators.py  # Tests for processor and validator functions
```

## Getting Started

1. **Clone the Repository & Install Dependencies**

   ```bash
   git clone <repository_url>
   cd text-generation-component
   pip install -r requirements.txt
   ```

2. **Configure the Component**

   - **`config.yaml`**  
     Define all necessary settings including API key, model parameters, retries, and the prompt file path.  
     Example snippet:
     ```yaml
     api:
       key: "your_openai_api_key"
       model: "gpt-3.5-turbo"
     prompt_path: "prompt.md"
     handler:
       retries: 3
       sleep_time: 3600
     ```
   
   - **`prompt.md`**  
     Edit your prompt template here. For example:
     ```markdown
     You are a wonderful English teacher who explains the meaning of the word to a student.
     
     **User:** {word} ({part_of_speech})
     
     **Model:**
     ```

3. **Run the Component**

   Use the entry point script:
   ```bash
   python main.py
   ```

## Developing and Extending

- **Model Module:**  
  Extend `BaseModel` in `src/model/base_model.py` to support additional APIs or custom parameters.  
  Modify or extend `openai_model.py` if you need to adjust OpenAI-specific behaviors.

- **Prompter:**  
  The `TemplatePrompter` in `src/prompter/template_prompter.py` handles external Markdown loading and substitutions. Customize it if additional formatting or variable processing is needed.

- **Handler and Processors:**  
  - Create new handlers by extending `BaseHandler` in `src/handler/base_handler.py`.  
  - Add custom processors by extending `BaseProcessor` in `src/processors/base_processor.py` and ensuring they integrate with `GenerationHandler`.

- **Validators:**  
  Extend `BaseValidator` in `src/validators/base_validator.py` to implement new validation rules for output formats.

- **Utilities:**  
  Leverage helper functions in `src/utils/` (such as `smart_format.py`) for common tasks during prompt substitution.

- **Testing:**  
  New changes should be covered by unit tests in the `tests/` directory.

## Summary

This text generation component provides a clear, modular architecture ideal for evolving requirements. Its separation into model, prompter, handler, processors, and validators, combined with a single configuration file and external Markdown prompt, ensures a maintainable, scalable design that mid-level developers can readily extend.

For further details or contributions, please refer to the inline documentation and test cases across the codebase.
