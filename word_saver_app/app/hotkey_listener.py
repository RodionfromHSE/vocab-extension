"""
Module for global hotkey listening.

This module defines a HotkeyListener that uses pynput to listen for a global hotkey
(Cmd+Shift+V) and triggers a signal through a helper QObject.
"""

import threading
from pynput import keyboard
from PyQt5.QtCore import QObject, pyqtSignal
from .config import HOTKEY

class HotkeyEmitter(QObject):
    hotkey_signal = pyqtSignal()

# Created in main thread
hotkey_emitter = HotkeyEmitter()

class HotkeyListener(threading.Thread):
    """
    Global hotkey listener using pynput.
    Emits hotkey_signal via HotkeyEmitter when triggered.
    """
    def __init__(self) -> None:
        super().__init__()
        self.daemon = True

    def run(self) -> None:
        with keyboard.GlobalHotKeys({HOTKEY: self.on_hotkey}) as listener:
            print(f"Listening for hotkey: {HOTKEY}")
            listener.join()

    def on_hotkey(self) -> None:
        print("Hotkey pressed, emitting signal...")
        hotkey_emitter.hotkey_signal.emit()
        print("Signal emitted.")