"""
Entry point for the mini application.
Updated to handle proper signal connection in main thread and to continue running 
even after the dialog is closed.
"""

import sys
from PyQt5.QtWidgets import QApplication
from functools import partial

from app.gui import PromptDialog
from app.hotkey_listener import HotkeyListener, hotkey_emitter
from app.storage import StorageManager



def show_prompt_dialog(storage_manager: StorageManager) -> None:
    print("Showing prompt dialog...")
    dialog = PromptDialog()
    # Connect the signal from the dialog to the save method.
    dialog.data_entered.connect(storage_manager.save)
    dialog.exec_()

def main() -> None:
    """
    Main function to initialize the application and set up the hotkey listener.
    """
    app = QApplication(sys.argv)
    storage_manager = StorageManager()
    
    # Prevent the application from quitting if all windows (dialogs) are closed.
    app.setQuitOnLastWindowClosed(False)
    
    # Set up hotkey listener and signal connection. The listener will continue 
    # to run in the background and trigger 'show_prompt_dialog' every time the hotkey is pressed.
    hotkey_emitter.hotkey_signal.connect(partial(show_prompt_dialog, storage_manager))
    # Start the hotkey listener in a separate thread.
    hotkey_listener = HotkeyListener()
    hotkey_listener.start()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
