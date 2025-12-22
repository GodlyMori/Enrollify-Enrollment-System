from PyQt6.QtWidgets import QLabel

class SectionHeader(QLabel):
    def __init__(self, text):
        super().__init__(text)
        self.setStyleSheet("""
            QLabel {
                color: #1F2937;
                font-size: 17px;
                font-weight: 700;
                padding-top: 20px;
                padding-bottom: 10px;
                letter-spacing: 0.5px;
            }
        """)
