"""
Entry point for the mini application.
Updated to handle proper signal connection in main thread, continue running 
even after the dialog is closed, and gracefully exit on termination or suspension signals.
"""

import sys
import signal
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer

from app.gui import PromptDialog
from app.hotkey_listener import HotkeyListener, hotkey_emitter
from app.storage import StorageManager
from app.config import ALLOWED_APPLICATIONS
from app.utils.application_monitor import ApplicationMonitor

should_exit = False


def show_prompt_dialog(storage_manager: StorageManager) -> None:
    print("Showing prompt dialog...")
    
    dialog = PromptDialog()
    dialog.data_entered.connect(storage_manager.save)
    
    dialog.show()
    dialog.force_focus()
    dialog.exec_()

def handle_signal(signum, frame) -> None:
    """Sets a flag to quit via the Qt event loop (avoids C++ blocking)."""
    global should_exit
    print(f"Received signal {signum}. Flagging application for shutdown...")
    should_exit = True

def check_for_exit() -> None:
    if should_exit:
        print("Exiting application due to received signal.")
        QApplication.instance().quit()


def main() -> None:
    app = QApplication(sys.argv)
    storage_manager = StorageManager()
    
    app.setQuitOnLastWindowClosed(False)
    
    signal.signal(signal.SIGTSTP, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)
    
    exit_timer = QTimer()
    exit_timer.timeout.connect(check_for_exit)
    exit_timer.start(100)
    
    app_monitor = ApplicationMonitor()
    def show_dialog_callback() -> None:
        print("Hotkey pressed, checking allowed applications...")
        if ApplicationMonitor.is_allowed_application(ALLOWED_APPLICATIONS):
            print("Allowed application detected, showing dialog.")
            show_prompt_dialog(storage_manager)
    hotkey_emitter.hotkey_signal.connect(show_dialog_callback)
    
    hotkey_listener = HotkeyListener()
    hotkey_listener.start()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
