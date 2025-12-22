from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QTabBar
)
from PyQt6.QtCore import Qt


class DashboardBase(QMainWindow):
    def __init__(self, title, subtitle):
        super().__init__()
        self.setWindowTitle(title)
        self.resize(1200, 800)
        self._build_base(title, subtitle)

    # ---------- BASE LAYOUT ----------
    def _build_base(self, title, subtitle):
        root = QWidget()
        root.setStyleSheet("background-color:#F9FAFB;")

        self.main_layout = QVBoxLayout(root)
        self.main_layout.setContentsMargins(32, 32, 32, 32)
        self.main_layout.setSpacing(28)

        self.main_layout.addWidget(self.header(title, subtitle))
        self.main_layout.addWidget(self.tabs())
        self.content_container = QWidget()
        self.content_layout = QVBoxLayout(self.content_container)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(28)

        self.main_layout.addWidget(self.content_container)
        self.setCentralWidget(root)

    # ---------- HEADER ----------
    def header(self, title, subtitle):
        bar = QWidget()
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(0, 0, 0, 0)

        left = QVBoxLayout()
        app = QLabel(title)
        app.setStyleSheet("font-size:22px;font-weight:700;color:#060C0B;")
        sub = QLabel(subtitle)
        sub.setStyleSheet("font-size:13px;color:#6B7280;")

        left.addWidget(app)
        left.addWidget(sub)

        logout = QPushButton("Logout")
        logout.setFixedHeight(36)
        logout.setStyleSheet("""
            QPushButton {
                padding: 0 18px;
                border-radius: 18px;
                border: 1px solid #10B981;
                color:#065F46;
                font-weight:600;
                background:white;
            }
            QPushButton:hover { background:#ECFDF5; }
        """)

        layout.addLayout(left)
        layout.addStretch()
        layout.addWidget(logout)

        return bar

    # ---------- TABS ----------
    def tabs(self):
        tabs = QTabBar()
        tabs.setDrawBase(False)
        tabs.setStyleSheet("""
            QTabBar::tab {
                padding: 10px 20px;
                color:#6B7280;
                font-weight:600;
            }
            QTabBar::tab:selected {
                color:#047857;
                border-bottom: 3px solid #10B981;
            }
        """)
        return tabs

    # ---------- CARD ----------
    def card(self):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background:white;
                border-radius:18px;
                border:1px solid #E5E7EB;
            }
        """)
        return card
