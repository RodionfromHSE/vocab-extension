"""Archive submitted word-saver JSON files after a successful pipeline run."""

from __future__ import annotations

import argparse
import os
import logging
from pathlib import Path

BACKUP_DIR_NAME = "old"


def remove_and_back_up(word_saver_dir: str | os.PathLike[str] | None = None) -> int:
    """
    Move direct JSON inputs to ``<word_saver_dir>/old``.

    Returns the number of files moved. Existing files in ``old`` are removed
    before the new batch is moved, preserving the original backup semantics.
    """
    configured_dir = word_saver_dir or os.environ.get("WORD_SAVER_SAVE_DIRECTORY")
    if not configured_dir:
        raise ValueError("Word-saver directory is not configured")
    source_dir = Path(configured_dir).expanduser()
    if not source_dir.is_dir():
        raise FileNotFoundError(f"Word-saver directory does not exist: {source_dir}")

    word_saver_files = sorted(
        path for path in source_dir.iterdir() if path.is_file() and path.suffix.lower() == ".json"
    )
    if not word_saver_files:
        logging.warning("No files to back up. Exiting.")
        return 0

    # Clean up old backup directory
    backup_dir = source_dir / BACKUP_DIR_NAME
    if backup_dir.exists() and backup_dir.is_dir():
        for file_path in backup_dir.iterdir():
            if file_path.is_file():
                file_path.unlink()
                logging.info("Removed %s", file_path)
    
    # Move files to backup directory
    backup_dir.mkdir(exist_ok=True)
    for source_file in word_saver_files:
        destination = backup_dir / source_file.name
        source_file.rename(destination)
        logging.info("Moved %s to %s/%s", source_file.name, BACKUP_DIR_NAME, source_file.name)
    return len(word_saver_files)

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("word_saver_dir", nargs="?", help="Directory containing submitted word JSON files")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    moved = remove_and_back_up(args.word_saver_dir)
    logging.info("Backup completed successfully: moved %d file(s).", moved)

if __name__ == "__main__":
    main()
