"""
Module for global hotkey listening.

Uses pynput to listen for a global hotkey and triggers a signal through a helper QObject.

Note: pynput's macOS backend (darwin.py) is patched in .venv to handle
kCGEventTapDisabledByTimeout — without it the hotkey silently dies after ~30 min.
"""

import threading
from pynput import keyboard
from PyQt5.QtCore import QObject, pyqtSignal
from .config import HOTKEY


class HotkeyEmitter(QObject):
    hotkey_signal = pyqtSignal()

hotkey_emitter = HotkeyEmitter()


class HotkeyListener(threading.Thread):
    """Global hotkey listener using pynput. Emits hotkey_signal via HotkeyEmitter."""
    def __init__(self) -> None:
        super().__init__()
        self.daemon = True

    def run(self) -> None:
        try:
            with keyboard.GlobalHotKeys({HOTKEY: self.on_hotkey}) as listener:
                print(f"Listening for hotkey: {HOTKEY}")
                listener.join()
        except Exception as e:
            print(f"HotkeyListener error: {e}")

    def on_hotkey(self) -> None:
        print("Hotkey pressed, emitting signal...")
        hotkey_emitter.hotkey_signal.emit()
        print("Signal emitted.")
