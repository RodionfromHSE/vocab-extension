import os
import sys
from pathlib import Path

root_directory = Path(__file__).resolve().parent

PROMPT_PATH = root_directory / "prompt.md"
DISCUSSED_TOPICS_PATH = root_directory / "discussed_topics.md"
INTERESTING_TOPICS_PATH = root_directory / "interesting_topics.md"

def create_prompt() -> str:
    """
    Create a prompt for the AI model.
    """
    return PROMPT_PATH.read_text().format(
        discussed_topics=DISCUSSED_TOPICS_PATH.read_text(),
        interesting_topics=INTERESTING_TOPICS_PATH.read_text()
    )

def main():
    """Create a prompt and print it."""
    prompt = create_prompt()
    print(prompt)

if __name__ == "__main__":
    main()