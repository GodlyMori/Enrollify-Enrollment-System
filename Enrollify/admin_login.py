from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QLineEdit, QSizePolicy
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap
import os


class AdminLoginScreen(QWidget):
    back_signal = pyqtSignal()
    login_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #E8F4F2;")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Back button
        back_widget = QWidget()
        back_widget.setFixedHeight(70)
        back_layout = QHBoxLayout(back_widget)
        back_layout.setContentsMargins(60, 20, 60, 20)

        back_btn = QPushButton("← Back to Home")
        back_btn.setFixedSize(140, 45)
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #4A9A87;
                border: none;
                font-size: 14px;
                font-weight: 500;
                text-align: left;
                padding: 10px;
            }
            QPushButton:hover { 
                color: #5DBAA3;
                background-color: rgba(93, 186, 163, 0.1);
                border-radius: 6px;
            }
        """)
        back_btn.clicked.connect(self.back_signal.emit)

        back_layout.addWidget(back_btn)
        back_layout.addStretch()

        layout.addWidget(back_widget)

        # Main content area - properly centered
        content_widget = QWidget()
        content_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        content_layout.addStretch()

        # Card container - horizontally centered
        card_container = QWidget()
        card_container_layout = QHBoxLayout(card_container)
        card_container_layout.setContentsMargins(0, 0, 0, 0)
        card_container_layout.setSpacing(0)

        card_container_layout.addStretch()

        card = QFrame()
        card.setFixedSize(550, 800)
        card.setStyleSheet("""
            QFrame { 
                background-color: white; 
                border-radius: 20px;
            }
        """)

        inner_layout = QVBoxLayout(card)
        inner_layout.setContentsMargins(50, 60, 50, 60)
        inner_layout.setSpacing(18)

        # Logo
        logo_container = QHBoxLayout()
        logo_label = QLabel()
        if os.path.exists('assets/enrollify_logo.png'):
            pixmap = QPixmap('assets/enrollify_logo.png')
            if not pixmap.isNull():
                scaled = pixmap.scaled(70, 70, Qt.AspectRatioMode.KeepAspectRatio,
                                      Qt.TransformationMode.SmoothTransformation)
                logo_label.setPixmap(scaled)
                logo_label.setFixedSize(scaled.size())
            else:
                self.create_fallback_logo(logo_label, 70)
        else:
            self.create_fallback_logo(logo_label, 70)

        logo_container.addStretch()
        logo_container.addWidget(logo_label)
        logo_container.addStretch()
        inner_layout.addLayout(logo_container)

        title = QLabel("Admin Login")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #060C0B; font-size: 28px; font-weight: 700; margin-top: 15px;")
        inner_layout.addWidget(title)

        subtitle = QLabel("System administration access")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #888; font-size: 14px; font-weight: 400; margin-bottom: 15px;")
        inner_layout.addWidget(subtitle)

        # Form fields with better spacing
        email_label = QLabel("Email Address")
        email_label.setStyleSheet("color: #060C0B; font-size: 13px; font-weight: 600; margin-top: 10px;")
        inner_layout.addWidget(email_label)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("admin@enrollify.edu")
        self.email_input.setMinimumHeight(50)
        self.email_input.setStyleSheet("""
            QLineEdit {
                background-color: #F8F9FA;
                border: 2px solid #E9ECEF;
                border-radius: 8px;
                padding-left: 15px;
                padding-right: 15px;
                font-size: 13px;
                color: #060C0B;
            }
            QLineEdit:focus {
                border: 2px solid #060C0B;
                background-color: white;
            }
            QLineEdit::placeholder {
                color: #AAA;
            }
        """)
        inner_layout.addWidget(self.email_input)

        password_label = QLabel("Password")
        password_label.setStyleSheet("color: #060C0B; font-size: 13px; font-weight: 600; margin-top: 15px;")
        inner_layout.addWidget(password_label)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(50)
        self.password_input.setStyleSheet("""
            QLineEdit {
                background-color: #F8F9FA;
                border: 2px solid #E9ECEF;
                border-radius: 8px;
                padding-left: 15px;
                padding-right: 15px;
                font-size: 13px;
                color: #060C0B;
            }
            QLineEdit:focus {
                border: 2px solid #060C0B;
                background-color: white;
            }
            QLineEdit::placeholder {
                color: #AAA;
            }
        """)
        inner_layout.addWidget(self.password_input)

        signin_btn = QPushButton("Sign In as Admin")
        signin_btn.setMinimumHeight(50)
        signin_btn.setStyleSheet("""
            QPushButton {
                background-color: #060C0B;
                color: white;
                border-radius: 8px;
                font-size: 15px;
                font-weight: 600;
                border: none;
                padding: 12px;
                margin-top: 20px;
            }
            QPushButton:hover { 
                background-color: #1a2320;
            }
            QPushButton:pressed {
                background-color: #000;
            }
        """)
        signin_btn.clicked.connect(self.login_signal.emit)
        inner_layout.addWidget(signin_btn)

        demo_label = QLabel("Administrative Access Only")
        demo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        demo_label.setWordWrap(True)
        demo_label.setStyleSheet("color: #AAA; font-size: 11px; margin-top: 15px;")
        inner_layout.addWidget(demo_label)

        inner_layout.addStretch()

        card_container_layout.addWidget(card)
        card_container_layout.addStretch()

        content_layout.addWidget(card_container)
        content_layout.addStretch()

        layout.addWidget(content_widget)

    def create_fallback_logo(self, label, size):
        label.setText("🛡")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(f"""
            QLabel {{ 
                background-color: #060C0B; 
                color: white; 
                border-radius: {size // 2}px; 
                font-size: {size // 2}px; 
                font-weight: bold; 
            }}
        """)
        label.setFixedSize(size, size)
