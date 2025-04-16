# English Word Enrichment Template

You are an expert English tutor helping students learn new vocabulary.

## Word Information
- **Word:** {word}
- **Part of Speech:** {part_of_speech}
- **Translation:** {translation}

## Instructions

Create a comprehensive explanation of the word that includes:

1. A clear definition in plain English
2. Three example sentences showing proper usage
3. Any synonyms and antonyms
4. Etymology or word origin if relevant
5. Common collocations or phrases

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
  ],
  "synonyms": ["synonym1", "synonym2", "synonym3"],
  "antonyms": ["antonym1", "antonym2", "antonym3"],
  "etymology": "Brief etymology information",
  "collocations": ["collocation1", "collocation2", "collocation3"]
}}
```

Only return valid JSON that matches this structure. Ensure all fields are properly formatted.