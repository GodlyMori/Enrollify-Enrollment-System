from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit
from PyQt6.QtCore import Qt

class FormInput(QWidget):
    def __init__(self, label_text, placeholder=""):
        super().__init__()
        self.setup_ui(label_text, placeholder)

    def setup_ui(self, label_text, placeholder):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        self.label = QLabel(label_text)
        self.label.setStyleSheet("""
            color: #374151;
            font-size: 14px;
            font-weight: 600;
            letter-spacing: 0.3px;
        """)

        self.input = QLineEdit()
        self.input.setPlaceholderText(placeholder)
        self.input.setMinimumHeight(52)
        self.input.setStyleSheet("""
            QLineEdit {
                background-color: #FFFFFF;
                border: none;
                border-bottom: 2px solid #E5E7EB;
                border-radius: 0px;
                padding: 12px 0px;
                padding-left: 4px;
                padding-right: 4px;
                font-size: 14px;
                color: #1F2937;
            }
            QLineEdit:focus {
                border-bottom: 2px solid #2D9B84;
                background-color: #FAFBFC;
            }
            QLineEdit::placeholder {
                color: #D1D5DB;
            }
        """)

        layout.addWidget(self.label)
        layout.addWidget(self.input)

    def value(self):
        return self.input.text()

    def setValue(self, text):
        self.input.setText(text)

    def clear(self):
        self.input.clear()
