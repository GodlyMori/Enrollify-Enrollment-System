from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt

class SubmitButton(QPushButton):
    def __init__(self, text="Submit"):
        super().__init__(text)
        self.setMinimumHeight(52)
        self.setMinimumWidth(200)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                background-color: #2D9B84;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 15px;
                font-weight: 700;
                padding: 12px 30px;
                letter-spacing: 0.5px;
            }
            QPushButton:hover {
                background-color: #35B499;
            }
            QPushButton:pressed {
                background-color: #1F7A66;
            }
        """)
