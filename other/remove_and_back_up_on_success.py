"""
This script removes old (back up) content and then moves the current word saver directory content to a backup directory.
Call only when you're sure you want to remove the old content.
"""
import os
import logging

BACKUP_DIR_NAME = "old"
WORD_SAVER_DIR = os.environ["WORD_SAVER_SAVE_DIRECTORY"]

def remove_and_back_up() -> None:
    """
    Remove the old content and back up the current word saver directory content.
    Note: In case WORD_SAVER_DIR is empty, the script will not perform any action.
    """
    # If WORD_SAVER_DIR is empty, do nothing
    word_saver_files = os.listdir(WORD_SAVER_DIR)
    word_saver_files = [f for f in word_saver_files if f.endswith(".json")]
    if not word_saver_files:
        logging.warning("No files to back up. Exiting.")
        return
    
    # Clean up old backup directory
    BACKUP_DIR = os.path.join(WORD_SAVER_DIR, BACKUP_DIR_NAME)
    if os.path.exists(BACKUP_DIR) and os.path.isdir(BACKUP_DIR):
        for file in os.listdir(BACKUP_DIR):
            file_path = os.path.join(BACKUP_DIR, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
                logging.info(f"Removed {file_path}")
    
    # Move files to backup directory
    os.makedirs(BACKUP_DIR, exist_ok=True)
    for file in word_saver_files:
        src = os.path.join(WORD_SAVER_DIR, file)
        dst = os.path.join(BACKUP_DIR, file)
        os.rename(src, dst)
        logging.info(f"Moved {file} to {BACKUP_DIR_NAME}/{file}")

def main() -> None:
    """
    Main function to execute the script.
    """
    logging.basicConfig(level=logging.INFO)
    remove_and_back_up()
    logging.info("Backup completed successfully.")

if __name__ == "__main__":
    main()
    