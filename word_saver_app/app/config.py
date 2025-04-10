"""
Configuration module for the mini application.
"""

import os
from pathlib import Path

# Directory where JSON files will be saved.
SAVE_DIRECTORY: Path = Path(__file__).resolve().parent.parent / "saved_data"
ALLOWED_APPLICATIONS: list[str] = [
    "yandex",
    "yandex browser",
    "yandexbrowser",
]
HOTKEY = "<cmd>+<shift>+v"  # Global hotkey for triggering the prompt dialog
