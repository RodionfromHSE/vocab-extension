"""
Configuration module for the mini application.
"""

import os
from pathlib import Path

# Directory where JSON files will be saved.
SAVE_DIRECTORY: Path = Path(__file__).resolve().parent.parent / "saved_data"

if not os.path.exists(SAVE_DIRECTORY):
    print(f"Creating directory: {SAVE_DIRECTORY}")
    os.makedirs(SAVE_DIRECTORY)

HOTKEY = "<cmd>+<shift>+v"  # Global hotkey for triggering the prompt dialog
