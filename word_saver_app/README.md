# Mini Application - Prompt Collector

A lightweight utility that captures text prompts via global hotkey, specifically designed to work with Yandex Browser.

## Overview

This application lets you quickly save text prompts with context information by using a global hotkey. When activated, a dialog appears that automatically pre-fills with your clipboard content, making it easy to capture and store information while browsing.

## Features

- Global hotkey triggering (`Cmd+Shift+P` by default)
- Application-specific activation (works only in Yandex Browser (adjustable, see configuration))
- Automatic clipboard content retrieval
- Incremental JSON storage system
- Cross-platform support (macOS, Windows, Linux)

## Codebase Structure

```
app/
  utils/
    application_monitor.py  # Detects active applications
  config.py                 # Configuration settings
  gui.py                    # PyQt dialog interface
  hotkey_listener.py        # Global hotkey detection
  storage.py                # JSON data storage manager
tests/
  test_application_monitor.py
main.py                     # Entry point
setup.py                    # Packaging configuration
```

## Key Components

- **ApplicationMonitor**: Detects the current active application and checks if it's allowed
- **PromptDialog**: Shows input fields for prompt word and context
- **HotkeyListener**: Listens for global hotkey in a separate thread
- **StorageManager**: Saves prompts to JSON files with incremental numbering

## Configuration

Edit `app/config.py` to change:
- `ALLOWED_APPLICATIONS`: List of applications where the hotkey works
- `HOTKEY`: The global hotkey combination
- `SAVE_DIRECTORY`: Where prompt data is saved (use `WORD_SAVER_SAVE_DIRECTORY` environment variable; by default, `~/Documents/word_saver`)
- `DEBUG`: Set to `True` for debugging information

## How to Run

```bash
python main.py
```

For macOS application packaging:
```bash
python setup.py py2app
```

You can find the packaged application in the `dist` directory after running the above command. \
For debugging and more details see [py2app tutorial](https://py2app.readthedocs.io/en/latest/tutorial.html). \
After creating the application, you can safely move it to your Applications folder or any other location.

**Important Note**: After you ensured that your application works correctly, you can mess up with Mac OS permissions. Try to change the application's name (see pyproject.toml) **after** you moved the ready application to the Applications folder.

## Development Notes

- The application uses PyQt5 for the UI components
- Global hotkeys are managed via pynput
- The app continues running in the background until explicitly terminated
- Data is saved to numbered JSON files (1.json, 2.json, etc.)