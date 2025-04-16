"""
Entry point for the mini application.
Updated to handle proper signal connection in main thread, continue running 
even after the dialog is closed, and gracefully exit on termination or suspension signals.
"""

import sys
import signal
from functools import partial
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer

from app.gui import PromptDialog
from app.hotkey_listener import HotkeyListener, hotkey_emitter
from app.storage import StorageManager
from app.config import ALLOWED_APPLICATIONS
from app.utils.application_monitor import ApplicationMonitor

# Global flag for termination
should_exit = False


def show_prompt_dialog(storage_manager: StorageManager) -> None:
    print("Showing prompt dialog...")
    
    dialog = PromptDialog()
    dialog.data_entered.connect(storage_manager.save)
    
    # Ensure dialog is on top and focused
    dialog.show()
    dialog.force_focus()
    dialog.exec_()

def handle_signal(signum, frame) -> None:
    """
    Handle termination and suspension signals.
    
    Instead of immediately calling app.quit() (which might get delayed due 
    to the C++ event loop blocking the Python interpreter), we set a global flag.
    """
    global should_exit
    print(f"Received signal {signum}. Flagging application for shutdown...")
    should_exit = True

def check_for_exit() -> None:
    """
    Periodically check if the termination/suspension signal has been received.
    If so, gracefully quit the application.
    """
    if should_exit:
        print("Exiting application due to received signal.")
        QApplication.instance().quit()


def main() -> None:
    """
    Main function to initialize the application, set up the hotkey listener,
    and configure signal handling.
    """
    app = QApplication(sys.argv)
    storage_manager = StorageManager()
    
    # Prevent the application from quitting if all windows (dialogs) are closed.
    app.setQuitOnLastWindowClosed(False)
    
    # Exit gracefully in case of suspension
    signal.signal(signal.SIGTSTP, handle_signal)
    
    # Set up a QTimer to periodically check for a termination signal.
    exit_timer = QTimer()
    exit_timer.timeout.connect(check_for_exit)
    exit_timer.start(100)  # check every 100 ms
    
    # Set up hotkey listener and connect the signal to show prompt dialog using partial.
    app_monitor = ApplicationMonitor()
    def show_dialog_callback() -> None:
        if ApplicationMonitor.is_allowed_application(ALLOWED_APPLICATIONS):
            show_prompt_dialog(storage_manager)
    hotkey_emitter.hotkey_signal.connect(show_dialog_callback)
    
    # Start the hotkey listener in a separate thread.
    hotkey_listener = HotkeyListener()
    hotkey_listener.start()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
