# Meta Generator Examples

This directory contains example files demonstrating how to use the Vocabulary Meta Generator.

## Files

- **example_input.json**: Sample input file containing basic vocabulary entries
- **example_output.json**: Sample output file showing the enriched vocabulary data
- **config.yaml**: Example configuration file with default input/output paths

## How to Run the Example

1. Make sure you've set up the project according to the main README
2. Ensure your OpenAI API key is configured (either in the config file or as an environment variable)
3. Run the following command from the project root:

```bash
# Using the command line options
python main.py --input "example/example_input.json" --output "example/your_output.json" --config "example/config.yaml"

# Using the short form options
python main.py -i "example/example_input.json" -o "example/your_output.json" --config "example/config.yaml"

# Or simply use the defaults from the example config.yaml (which already includes input/output paths)
python main.py --config "example/config.yaml"
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

1. Check the API key is properly set
2. Verify the input file has the correct format
3. Ensure you're running the command from the project root directory

For more detailed troubleshooting, refer to the main README.md file.