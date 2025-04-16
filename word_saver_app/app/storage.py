"""
Module for managing storage of prompt data.

This module provides a StorageManager class which saves prompt data (a word and a context)
into JSON files in a designated directory. The manager uses a counter attribute to keep
track of how many words have been saved. For example, if the counter is 5, the prompt is saved 
to "5.json" and the counter is then incremented.
"""

import json
import os
from pathlib import Path

from app.config import SAVE_DIRECTORY

class StorageManager:
    """
    Manages saving of prompt data into JSON files with an incremental counter.
    """
    def __init__(self, save_directory: str = str(SAVE_DIRECTORY)) -> None:
        """
        Initialize the storage manager and the counter.

        Args:
            save_directory (str): Directory where JSON files will be saved.
        """
        self.save_directory: str = save_directory
        # Ensure the save directory exists.
        Path(self.save_directory).mkdir(parents=True, exist_ok=True)
        # Initialize the counter using a special method.
        self.counter: int = self._initialize_counter()
        print(f"StorageManager initialized with counter starting at {self.counter}")

    def _initialize_counter(self) -> int:
        """
        Initialize the counter based on existing JSON files in the storage directory.

        The method searches for files matching the pattern "<number>.json" and, if found,
        sets the counter to one plus the highest number. Otherwise, it starts at 1.

        Returns:
            int: The next available counter value.
        """
        def json_to_number(filename: str) -> int:
            """
            Convert a filename to an integer if it ends with '.json'.
            """
            if filename.endswith('.json'):
                name_without_ext = filename[:-5]
                if name_without_ext.isdigit():
                    return int(name_without_ext)
            return 0
        
        return max(
            (json_to_number(f) for f in os.listdir(self.save_directory)),
            default=0
        ) + 1

    def save(self, prompt_word: str, prompt_context: str) -> None:
        """
        Save the given prompt data into a JSON file named with the current counter value.

        For example, if the counter is 5, the file "5.json" is created (or overwritten)
        and then the counter increases by 1.

        Args:
            prompt_word (str): The prompt word.
            prompt_context (str): The prompt context.
        """
        data = {
            "word": prompt_word,
            "context": prompt_context
        }
        # Construct the file path using the current counter value.
        filename = f"{self.counter}.json"
        file_path = os.path.join(self.save_directory, filename)
        # Save the data as a JSON file.
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        print(f"Data saved to {file_path}")
        # Increment the counter after saving.
        self.counter += 1
