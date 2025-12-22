from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QFrame, QTableWidget, QTableWidgetItem,
                             QHeaderView, QLineEdit, QComboBox, QSizePolicy)
from PyQt6.QtCore import (
    Qt, QTimer, QPropertyAnimation,
    QEasingCurve, pyqtSignal
)
from PyQt6.QtGui import QPainter, QColor, QPixmap
import os


class PieChartWidget(QWidget):
    def __init__(self, value1, value2, color1, color2, label1, label2):
        super().__init__()
        self.value1 = value1
        self.value2 = value2
        self.color1 = QColor(color1)
        self.color2 = QColor(color2)
        self.label1 = label1
        self.label2 = label2
        self._angle = 0
        self.setMinimumSize(300, 300)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def get_angle(self):
        return self._angle

    def set_angle(self, angle):
        self._angle = angle
        self.update()

    angle = property(get_angle, set_angle)

    def start_animation(self):
        self.animation = QPropertyAnimation(self, b"angle")
        self.animation.setDuration(1500)
        self.animation.setStartValue(0)
        self.animation.setEndValue(360)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        total = self.value1 + self.value2
        if total == 0:
            return

        width = self.width()
        height = self.height()
        margin = 30
        size = min(width, height) - (margin * 2)
        x = (width - size) // 2
        y = (height - size) // 2

        angle1 = int((self.value1 / total) * self._angle * 16)
        angle2 = int((self.value2 / total) * self._angle * 16)

        painter.setBrush(self.color1)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawPie(x, y, size, size, 90 * 16, -angle1)

        painter.setBrush(self.color2)
        painter.drawPie(x, y, size, size, (90 * 16) - angle1, -angle2)


class BarWidget(QWidget):
    def __init__(self, labels, values, color):
        super().__init__()
        self.labels = labels
        self.values = values
        self.color = QColor(color)
        self.setMinimumHeight(280)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def paintEvent(self, event):
        if not self.values:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        width = self.width()
        height = self.height() - 60
        bar_width = (width - 120) / len(self.values)
        max_value = max(self.values) if self.values else 1

        for i, (label, value) in enumerate(zip(self.labels, self.values)):
            x = 60 + i * bar_width + (bar_width - 70) / 2
            bar_height = (value / max_value) * height
            y = height - bar_height + 30

            painter.setBrush(self.color)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRect(int(x), int(y), 70, int(bar_height))

            painter.setPen(QColor("#666"))
            painter.drawText(int(x), height + 40, 70, 25, Qt.AlignmentFlag.AlignCenter, label)


class HeaderWidget(QWidget):
    logout_signal = pyqtSignal()

    def __init__(self, title="Enrollify", subtitle="Staff Portal - Student Management"):
        super().__init__()
        self.setFixedHeight(90)
        self.setAutoFillBackground(True)

        # Set white background using palette for better compatibility
        from PyQt6.QtGui import QPalette
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#FFFFFF"))
        self.setPalette(palette)

        self.setStyleSheet("""
            HeaderWidget {
                background-color: #FFFFFF;
                border: none;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(40, 0, 40, 0)

        # Logo and title
        logo_layout = QHBoxLayout()
        logo_layout.setSpacing(20)

        logo = QLabel()
        if os.path.exists('assets/enrollify_logo.png'):
            pixmap = QPixmap('assets/enrollify_logo.png')
            if not pixmap.isNull():
                # scale and set fixed size so the logo is not cut off
                scaled = pixmap.scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio,
                                      Qt.TransformationMode.SmoothTransformation)
                logo.setPixmap(scaled)
                logo.setFixedSize(scaled.size())
            else:
                self.create_fallback_logo(logo, 50)
        else:
            self.create_fallback_logo(logo, 50)

        logo_layout.addWidget(logo)

        title_container = QWidget()
        title_layout = QVBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(5)

        title_label = QLabel(title)
        title_label.setStyleSheet("color: #060C0B; font-size: 22px; font-weight: 600;")

        subtitle_label = QLabel(subtitle)
        subtitle_label.setStyleSheet("color: #666; font-size: 14px; font-weight: 500;")

        title_layout.addWidget(title_label)
        title_layout.addWidget(subtitle_label)

        logo_layout.addWidget(title_container)

        layout.addLayout(logo_layout)
        layout.addStretch()

        # Logout button
        logout_btn = QPushButton("⎋ Logout")
        logout_btn.setFixedSize(120, 45)
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #4A9A87;
                border: 2px solid #5DBAA3;
                border-radius: 10px;
                font-size: 15px;
                font-weight: 500;
                padding: 10px;
            }
            QPushButton:hover { 
                background-color: #E8F4F2;
                transform: scale(1.02);
            }
        """)
        logout_btn.clicked.connect(self.logout_signal.emit)
        layout.addWidget(logout_btn)

    def create_fallback_logo(self, label, size):
        label.setText("✓")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(f"""
            QLabel {{ 
                background-color: #5DBAA3; 
                color: #060C0B; 
                border-radius: {size // 2}px; 
                font-size: {size // 2}px; 
                font-weight: bold; 
            }}
        """)
        label.setFixedSize(size, size)


class NavTabsWidget(QWidget):
    show_overview_signal = pyqtSignal()
    show_enrollees_signal = pyqtSignal()
    show_reports_signal = pyqtSignal()

    def __init__(self, active="overview"):
        super().__init__()
        self.setFixedHeight(60)
        self.setStyleSheet("background-color: #F8F9FA;")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(40, 0, 40, 0)
        layout.setSpacing(0)

        # Create tab buttons
        self.overview_btn = self.create_tab_button("⊞ Overview", active == "overview")
        self.enrollees_btn = self.create_tab_button("👥 Enrollees", active == "enrollees")
        self.reports_btn = self.create_tab_button("📄 Reports", active == "reports")

        self.overview_btn.clicked.connect(self.show_overview_signal.emit)
        self.enrollees_btn.clicked.connect(self.show_enrollees_signal.emit)
        self.reports_btn.clicked.connect(self.show_reports_signal.emit)

        layout.addWidget(self.overview_btn)
        layout.addWidget(self.enrollees_btn)
        layout.addWidget(self.reports_btn)
        layout.addStretch()

    def create_tab_button(self, text, is_active):
        btn = QPushButton(text)
        if is_active:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: white;
                    color: #060C0B;
                    border: none;
                    font-size: 15px;
                    font-weight: 600;
                    padding: 0 25px;
                    height: 60px;
                }
                QPushButton:hover {
                    background-color: #F0F0F0;
                }
            """)
        else:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #666;
                    border: none;
                    font-size: 15px;
                    font-weight: 500;
                    padding: 0 25px;
                    height: 60px;
                }
                QPushButton:hover { 
                    background-color: #E8E8E8;
                    color: #060C0B;
                }
            """)
        return btn


class StatCard(QFrame):
    def __init__(self, title, value, subtitle, icon):
        super().__init__()
        self.setStyleSheet("""
            QFrame { 
                background-color: white; 
                border-radius: 15px; 
                border: 1px solid #E8E8E8;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.02);
            }
            QFrame:hover {
                border-color: #5DBAA3;
            }
        """)
        self.setFixedHeight(150)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(12)

        # Header
        header = QHBoxLayout()
        header.setContentsMargins(0, 0, 0, 0)

        title_label = QLabel(title)
        title_label.setStyleSheet("color: #060C0B; font-size: 16px; font-weight: 600;")

        icon_label = QLabel(icon)
        icon_label.setStyleSheet("color: #5DBAA3; font-size: 24px;")

        header.addWidget(title_label)
        header.addStretch()
        header.addWidget(icon_label)

        layout.addLayout(header)

        # Value
        value_label = QLabel(value)
        value_label.setStyleSheet("color: #060C0B; font-size: 42px; font-weight: 700; margin: 5px 0;")
        layout.addWidget(value_label)

        # Subtitle
        subtitle_label = QLabel(subtitle)
        subtitle_label.setStyleSheet("color: #999; font-size: 14px;")
        layout.addWidget(subtitle_label)

        layout.addStretch()