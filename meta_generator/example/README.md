# Meta Generator Examples

This directory contains example files demonstrating how to use the Vocabulary Meta Generator.

## Files

- **example_input.json**: Sample input file containing basic vocabulary entries
- **example_output.json**: Sample output file showing the enriched vocabulary data
- **config.yaml**: Example configuration file for OpenAI models with default input/output paths
- **config_nebius.yaml**: Example configuration file for Nebius AI Studio (DeepSeek models) with default input/output paths

## How to Run the Example

1. Make sure you've set up the project according to the main README
2. Choose your AI provider and ensure your API key is configured:
   - **For OpenAI**: Set your `OPENAI_API_KEY` environment variable or add it to the config file
   - **For Nebius (DeepSeek)**: Set your `NEBIUS_API_KEY` environment variable or add it to the config file
3. Run the following command from the project root (from `example` directory):

### Using OpenAI Models

```bash
# Using the command line options with OpenAI config
python ../main.py --config "config.yaml"

# Using the short form options
python ../main.py -i "example_input.json" -o "example_output.json" --config "config.yaml"

# Or simply use the defaults from the example config.yaml (which already includes input/output paths)
python ../main.py --config "config.yaml"
```

### Using Nebius (DeepSeek) Models

```bash
# Using the command line options with Nebius config
python ../main.py --config "config_nebius.yaml"

# Using the short form options
python ../main.py -i "example_input.json" -o "example_output.json" --config "config_nebius.yaml"

# Or simply use the defaults from the example config_nebius.yaml
python ../main.py --config "config_nebius.yaml"
```

4. Compare your output with the provided `example_output.json` file to verify the generator is working correctly

## Expected Output Structure

Each input word entry will be enriched with:

- **definition**: Clear definition of the word
- **examples**: 3 example sentences showing proper usage
- **synonyms**: List of similar words
- **antonyms**: List of opposite words
- **etymology**: Origin of the word
- **collocations**: Common word combinations

## Troubleshooting

If you encounter issues:

1. Check that the appropriate API key is properly set:
   - For OpenAI: `OPENAI_API_KEY` environment variable
   - For Nebius: `NEBIUS_API_KEY` environment variable
2. Verify the input file has the correct format
3. Ensure you're running the command from the project root directory
4. Make sure you're using the correct configuration file for your chosen AI provider

For more detailed troubleshooting, refer to the main README.md file.