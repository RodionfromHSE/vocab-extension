"""
Module for managing storage of prompt data.

This module provides a StorageManager class which saves prompt data (a word and a context)
into JSON files in a designated directory. It alternates between saving to "1.json" and "2.json".
"""

import json
import os
from pathlib import Path
from typing import List

from app.config import SAVE_DIRECTORY

class StorageManager:
    """
    Manages saving of prompt data into JSON files.

    The manager alternates between two files ("1.json" and "2.json") to store data.
    """
    def __init__(self, save_directory: str = SAVE_DIRECTORY, indices: List[int] = None) -> None:
        """
        Initialize the storage manager.

        Args:
            save_directory (str): Directory where JSON files will be saved.
            indices (List[int], optional): List of file indices to alternate between.
                Defaults to [1, 2].
        """
        if indices is None:
            indices = [1, 2]
        self.save_directory: str = save_directory
        self.indices: List[int] = indices
        self.current_index: int = indices[0]
        # Ensure the save directory exists.
        Path(self.save_directory).mkdir(parents=True, exist_ok=True)

    def save(self, prompt_word: str, prompt_context: str) -> None:
        """
        Save the given prompt data into a JSON file.

        Args:
            prompt_word (str): The prompt word.
            prompt_context (str): The prompt context.
        """
        data = {
            "prompt_word": prompt_word,
            "prompt_context": prompt_context
        }
        file_path = os.path.join(self.save_directory, f"{self.current_index}.json")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        print(f"Data saved to {file_path}")
        self._toggle_index()

    def _toggle_index(self) -> None:
        """
        Toggle the current file index between the available indices.
        """
        self.current_index = (
            self.indices[1] if self.current_index == self.indices[0] else self.indices[0]
        )
