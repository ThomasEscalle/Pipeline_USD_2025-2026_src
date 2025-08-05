from qtpy.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QHBoxLayout, QPushButton

import logging
import sys

class EmittingStream:
    def __init__(self, text_edit):
        self.text_edit = text_edit

    def write(self, text):
        if text.strip():  # Avoid printing empty lines
            text = text.replace('\n', '')  # Remove newlines for cleaner output
            self.text_edit.append(text)

    def flush(self):
        pass  # Needed for compatibility with sys.stdout

class ConsoleDialog(QDialog):
    def __init__(self, parent=None):
        super(ConsoleDialog, self).__init__(parent)

        self.setWindowTitle("Console")
        self.resize(600, 400)

        

        # Create a horizontal layout for the top bar (for the clear button)
        topBarLayout = QHBoxLayout()
        topBarLayout.addStretch()
        self.clearButton = QPushButton("Clear logs")
        self.clearButton.clicked.connect(self.clearLogs)
        topBarLayout.addWidget(self.clearButton)

        # Create a QTextEdit widget for the console
        self.console = QTextEdit(self)
        self.console.setReadOnly(True)

        # Redirect stdout and stderr to the QTextEdit
        sys.stdout = EmittingStream(self.console)
        sys.stderr = EmittingStream(self.console)
        


        # Set up the main layout
        layout = QVBoxLayout()
        layout.addLayout(topBarLayout)
        layout.addWidget(self.console)
        self.setLayout(layout)

    def clearLogs(self):
        self.console.clear()

    def print(self, message):
        """Append a message to the console."""
        self.console.append(message)

    def log(self, message):
        """Append a message to the console with a timestamp."""
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.console.append(f"[{timestamp}] {message}")