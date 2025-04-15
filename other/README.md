# Dataset Convertor

This tool processes and combines multiple JSON files into a single structured output, filtering out invalid or incomplete entries. It's especially useful for preparing datasets containing word-context pairs.

---

## 📁 Overview

This folder contains:

- **`dataset_convertor.py`**  
  A CLI utility that merges and validates JSON files located in a directory.

---

## ✅ JSON File Requirements

Each input JSON file must:

- Have exactly two keys: `"word"` and `"context"`
- Be a valid JSON object

Example of a valid JSON file:

```json
{
    "word": "serenity",
    "context": "She found serenity in the quiet garden."
}
```

---

## 🚀 Usage

You can run the script via command line using [Click](https://click.palletsprojects.com/):

```bash
python dataset_convertor.py [INPUT_FOLDER] [OUTPUT_FILE]
```

### Arguments:

- `INPUT_FOLDER`: Path to the folder containing `.json` files  
- `OUTPUT_FILE`: Path to save the combined result (default: `./data/words_raw.json`)

> If not provided, the script reads from the `WORD_SAVER_SAVE_DIRECTORY` environment variable for input, and saves to the default output file.

---

## ⚙️ Features

- ✅ Skips non-JSON files
- ✅ Skips files with missing or invalid keys
- ✅ Outputs a nicely formatted `.json` file
- ✅ Provides CLI feedback

---

## 📦 Output

A single JSON array containing all valid entries:

```json
[
    {
        "word": "serenity",
        "context": "She found serenity in the quiet garden."
    },
    {
        "word": "resilience",
        "context": "Resilience is built through facing difficulties."
    }
]
```

---

## 🛠 Development

Install dependencies (Click is the only external one):

```bash
pip install click
```

---

## 📂 Folder Structure

```
other/
├── dataset_convertor.py
└── README.md
```

