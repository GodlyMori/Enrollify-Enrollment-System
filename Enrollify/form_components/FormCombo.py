from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox
from PyQt6.QtCore import pyqtSignal

class FormCombo(QWidget):
    # Emit signal when selection changes
    value_changed = pyqtSignal(str)

    def __init__(self, label_text, items):
        super().__init__()
        self.setup_ui(label_text, items)

    def setup_ui(self, label_text, items):
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

        self.combo = QComboBox()
        self.combo.addItems(items)
        self.combo.setMinimumHeight(52)
        self.combo.setStyleSheet("""
            QComboBox {
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
            QComboBox:focus {
                border-bottom: 2px solid #2D9B84;
                background-color: #FAFBFC;
            }
            QComboBox::drop-down {
                border: none;
                width: 24px;
            }
            QComboBox::down-arrow {
                image: none;
                width: 0px;
            }
        """)

        # Connect signal
        self.combo.currentTextChanged.connect(self.value_changed.emit)

        layout.addWidget(self.label)
        layout.addWidget(self.combo)

    def value(self):
        return self.combo.currentText()

    def setValue(self, text):
        index = self.combo.findText(text)
        if index >= 0:
            self.combo.setCurrentIndex(index)

    def clear(self):
        self.combo.setCurrentIndex(0)

    # NEW: Dynamically update options
    def set_options(self, items):
        """Replace current items with new list"""
        current = self.value()
        self.combo.clear()
        self.combo.addItems(items)
        # Try to restore previous selection if still valid
        if current in items:
            self.setValue(current)