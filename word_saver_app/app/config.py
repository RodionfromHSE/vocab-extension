"""
Configuration module for the mini application.
"""

import os
from pathlib import Path

DEBUG_MODE = False # Set to True for debugging
ALLOWED_APPLICATIONS: list[str] = [
    "yandex",
    "yandex browser",
    "yandexbrowser",
]
HOTKEY = "<cmd>+<shift>+p"  # Global hotkey for triggering the prompt dialog


def get_save_directory() -> Path:
    """
    Get the save directory for the application.
    """
    USER_HOME = Path.home()
    DEFAULT_SAVE_DIRECTORY = USER_HOME / "Documents" / "word_saver"
    SAVE_DIRECTORY: Path = Path(os.environ.get("WORD_SAVER_SAVE_DIRECTORY", str(DEFAULT_SAVE_DIRECTORY))) if not DEBUG_MODE else Path(__file__).parent.parent / "test_data"
    SAVE_DIRECTORY.mkdir(parents=True, exist_ok=True)  # Ensure the save directory exists
    return SAVE_DIRECTORY
SAVE_DIRECTORY = get_save_directory()  # Directory where JSON files will be saved