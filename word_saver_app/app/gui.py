"""
Module for the PyQt GUI.

This module defines a PromptDialog which shows two input fields (for prompt word and context)
and a submit button. When the user submits, the dialog emits the entered data.
"""
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QLabel, QPushButton, QApplication
from PyQt5.QtCore import pyqtSignal, Qt, QTimer
from PyQt5.QtGui import QClipboard  # Added for clipboard access


class PromptDialog(QDialog):
    """
    Dialog window for entering prompt data.

    Emits:
        data_entered (str, str): Emitted when the user finishes inputting data.
    """
    data_entered = pyqtSignal(str, str)

    def __init__(self, parent=None) -> None:
        """
        Initialize the prompt dialog.
        """
        super().__init__(parent)
        self.setup_ui()
        
        # Set window flags to ensure the dialog appears on top
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        
        # Get clipboard content and insert it into both fields
        self.insert_clipboard_content()
        
    def setup_ui(self) -> None:
        """
        Set up the user interface components.
        """
        layout = QVBoxLayout()

        self.label_word = QLabel("Prompt Word:")
        layout.addWidget(self.label_word)

        self.line_edit_word = QLineEdit()
        layout.addWidget(self.line_edit_word)

        self.label_context = QLabel("Prompt Context:")
        layout.addWidget(self.label_context)

        self.line_edit_context = QLineEdit()
        layout.addWidget(self.line_edit_context)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_data)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)
    
    def insert_clipboard_content(self) -> None:
        """
        Get text from clipboard and insert it into both input fields.
        """
        clipboard = QApplication.clipboard()
        clipboard_text = clipboard.text()
        
        if clipboard_text:
            self.line_edit_word.setText(clipboard_text)
            self.line_edit_context.setText(clipboard_text)
            
            # Select all text in the word field for easy editing
            self.line_edit_word.selectAll()
        
    def submit_data(self) -> None:
        """
        Emit the entered data and close the dialog.
        """
        prompt_word = self.line_edit_word.text().strip()
        prompt_context = self.line_edit_context.text().strip()
        self.data_entered.emit(prompt_word, prompt_context)
        self.accept()