"""
Entry point for the mini application.
Updated to handle proper signal connection in main thread.
"""

import sys
from PyQt5.QtWidgets import QApplication
from app.gui import PromptDialog
from app.hotkey_listener import HotkeyListener, hotkey_emitter
from app.storage import StorageManager

def show_prompt_dialog() -> None:
    global storage_manager
    print("Showing prompt dialog...")
    dialog = PromptDialog()
    dialog.data_entered.connect(storage_manager.save)
    dialog.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    storage_manager = StorageManager()

    # Set up hotkey listener and signal connection
    hotkey_emitter.hotkey_signal.connect(show_prompt_dialog)
    hotkey_listener = HotkeyListener()
    hotkey_listener.start()

    sys.exit(app.exec_())
