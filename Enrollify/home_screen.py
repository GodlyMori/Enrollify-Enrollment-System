from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QSizePolicy
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QPixmap, QFont, QColor, QPainter, QPen
from PyQt6.QtSvgWidgets import QSvgWidget
import os


class HomeScreen(QWidget):
    staff_login_signal = pyqtSignal()
    admin_login_signal = pyqtSignal()
    enroll_now_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QWidget {
                background-color: #E8F5F3;
            }
        """)
        self.setup_ui()

    def load_icon(self, icon_name, size=24, fallback_text=""):
        """
        Load an icon from assets/icons folder with fallback to emoji

        Args:
            icon_name: Name of the icon file (e.g., 'admin.png', 'enroll.svg')
            size: Size of the icon in pixels
            fallback_text: Emoji or text to show if icon not found

        Returns:
            QLabel with the icon or fallback text
        """
        icon_label = QLabel()
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Try different file extensions
        icon_extensions = ['.png', '.svg', '.jpg', '.jpeg']
        icon_path = None

        for ext in icon_extensions:
            path = f'assets/icons/{icon_name}{ext}'
            if os.path.exists(path):
                icon_path = path
                break

        if icon_path:
            if icon_path.endswith('.svg'):
                # For SVG files, use QSvgWidget approach
                svg_widget = QSvgWidget(icon_path)
                svg_widget.setFixedSize(size, size)
                # Create a layout to embed the SVG widget - centered
                container = QWidget()
                container.setStyleSheet("background-color: transparent;")
                container.setFixedHeight(size)
                layout = QHBoxLayout(container)
                layout.setContentsMargins(0, 0, 0, 0)
                layout.addStretch()
                layout.addWidget(svg_widget)
                layout.addStretch()
                return container
            else:
                # For raster images (PNG, JPG)
                pixmap = QPixmap(icon_path)
                if not pixmap.isNull():
                    scaled_pixmap = pixmap.scaled(
                        size, size,
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation
                    )
                    icon_label.setPixmap(scaled_pixmap)
                    icon_label.setFixedHeight(size)
                    icon_label.setStyleSheet("background-color: transparent;")
                    return icon_label

        # Fallback to emoji/text
        icon_label.setText(fallback_text)
        icon_label.setFixedHeight(size)
        icon_label.setStyleSheet(f"font-size: {size}px; background-color: transparent;")
        return icon_label

    def setup_ui(self):
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Top bar with Admin button
        top_widget = QWidget()
        top_widget.setFixedHeight(100)
        top_widget.setStyleSheet("background-color: #E8F5F3;")
        top_layout = QHBoxLayout(top_widget)
        top_layout.setContentsMargins(60, 30, 60, 30)
        top_layout.addStretch()

        # Admin button in top right
        admin_btn = QPushButton()
        admin_btn.setFixedSize(120, 45)
        admin_btn.setStyleSheet("""
            QPushButton {
                background-color: #1A3F3A;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 600;
                padding: 8px 16px;
            }
            QPushButton:hover { 
                background-color: #234940;
            }
        """)
        admin_btn.clicked.connect(self.admin_login_signal.emit)

        # Admin button layout with icon
        admin_btn_layout = QHBoxLayout(admin_btn)
        admin_btn_layout.setContentsMargins(8, 0, 8, 0)
        admin_btn_layout.setSpacing(6)
        admin_btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        admin_icon = self.load_icon('admin', size=18, fallback_text="🛡")
        admin_icon.setStyleSheet("color: white; background-color: transparent;")
        admin_btn_layout.addWidget(admin_icon, alignment=Qt.AlignmentFlag.AlignCenter)

        admin_text = QLabel("Admin")
        admin_text.setStyleSheet("color: white; font-size: 14px; font-weight: 600; background-color: transparent;")
        admin_btn_layout.addWidget(admin_text, alignment=Qt.AlignmentFlag.AlignCenter)

        top_layout.addWidget(admin_btn)

        main_layout.addWidget(top_widget)

        # Main content area - centered card
        content_container = QWidget()
        content_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        content_container.setStyleSheet("background-color: #E8F5F3;")
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        content_layout.addStretch()

        # Center the card horizontally
        card_wrapper = QHBoxLayout()
        card_wrapper.addStretch()

        # Main card container
        card = QFrame()
        card.setFixedSize(450, 600)
        card.setStyleSheet("""
            QFrame { 
                background-color: white; 
                border-radius: 16px;
            }
        """)
        # Add shadow effect
        from PyQt6.QtWidgets import QGraphicsDropShadowEffect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setXOffset(0)
        shadow.setYOffset(10)
        shadow.setColor(QColor(0, 0, 0, 30))
        card.setGraphicsEffect(shadow)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(50, 50, 50, 50)
        card_layout.setSpacing(20)

        # Logo at top
        logo_label = QLabel()
        if os.path.exists('assets/enrollify_logo.png'):
            pixmap = QPixmap('assets/enrollify_logo.png')
            if not pixmap.isNull():
                scaled = pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio,
                                       Qt.TransformationMode.SmoothTransformation)
                logo_label.setPixmap(scaled)
                logo_label.setFixedSize(scaled.size())
            else:
                logo_label.setFixedSize(80, 80)
                self.create_checkmark_logo(logo_label)
        else:
            logo_label.setFixedSize(80, 80)
            self.create_checkmark_logo(logo_label)

        logo_container = QHBoxLayout()
        logo_container.addStretch()
        logo_container.addWidget(logo_label)
        logo_container.addStretch()
        card_layout.addLayout(logo_container)

        card_layout.addSpacing(10)

        # Brand name - Enrollify
        brand_name = QLabel("Enrollify")
        brand_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        brand_name.setStyleSheet("""
            QLabel {
                color: #234940; 
                font-size: 42px; 
                font-weight: 700;
                letter-spacing: -0.5px;
            }
        """)
        card_layout.addWidget(brand_name)

        # Tagline
        tagline = QLabel("Your Gateway to Senior High Success")
        tagline.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tagline.setStyleSheet("""
            QLabel {
                color: #4A9A87; 
                font-size: 15px; 
                font-weight: 500;
            }
        """)
        card_layout.addWidget(tagline)

        card_layout.addSpacing(25)

        # Enroll Now button (teal/green filled)
        enroll_btn = QPushButton()
        enroll_btn.setFixedHeight(110)
        enroll_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        enroll_btn.setStyleSheet("""
            QPushButton {
                background-color: #2D9B84;
                border-radius: 12px;
                border: none;
                padding: 0px;
            }
            QPushButton:hover { 
                background-color: #35B499;
            }
        """)
        enroll_btn.clicked.connect(self.enroll_now_signal.emit)

        enroll_layout = QVBoxLayout(enroll_btn)
        enroll_layout.setContentsMargins(10, 10, 10, 10)
        enroll_layout.setSpacing(5)

        # Icon for enroll button - load from assets
        enroll_icon = self.load_icon('enroll', size=28, fallback_text="⊕")
        enroll_icon.setStyleSheet("color: white; background-color: transparent;")
        enroll_layout.addWidget(enroll_icon, alignment=Qt.AlignmentFlag.AlignCenter)

        enroll_title = QLabel("Enroll Now")
        enroll_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        enroll_title.setStyleSheet("color: white; font-size: 18px; font-weight: 700; background-color: transparent;")
        enroll_layout.addWidget(enroll_title)

        enroll_subtitle = QLabel("Start your enrollment application")
        enroll_subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        enroll_subtitle.setStyleSheet("color: white; font-size: 12px; font-weight: 500; background-color: transparent;")
        enroll_layout.addWidget(enroll_subtitle)

        card_layout.addWidget(enroll_btn)

        card_layout.addSpacing(15)

        # OR separator
        or_container = QWidget()
        or_layout = QHBoxLayout(or_container)
        or_layout.setContentsMargins(0, 5, 0, 5)
        or_layout.setSpacing(15)

        or_line_left = QFrame()
        or_line_left.setFrameShape(QFrame.Shape.HLine)
        or_line_left.setStyleSheet("background-color: #D5D5D5;")
        or_line_left.setFixedHeight(1)

        or_label = QLabel("OR")
        or_label.setStyleSheet("color: #999999; font-size: 13px; font-weight: 600;")

        or_line_right = QFrame()
        or_line_right.setFrameShape(QFrame.Shape.HLine)
        or_line_right.setStyleSheet("background-color: #D5D5D5;")
        or_line_right.setFixedHeight(1)

        or_layout.addWidget(or_line_left, 1)
        or_layout.addWidget(or_label)
        or_layout.addWidget(or_line_right, 1)

        card_layout.addWidget(or_container)

        card_layout.addSpacing(15)

        # Staff Portal button (outlined)
        staff_btn = QPushButton()
        staff_btn.setFixedHeight(110)
        staff_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        staff_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: 2px solid #2D9B84;
                border-radius: 12px;
                padding: 0px;
            }
            QPushButton:hover { 
                background-color: #F0FAF8;
            }
        """)
        staff_btn.clicked.connect(self.staff_login_signal.emit)

        staff_layout = QVBoxLayout(staff_btn)
        staff_layout.setContentsMargins(10, 10, 10, 10)
        staff_layout.setSpacing(5)

        # Icon for staff button - load from assets
        staff_icon = self.load_icon('staff', size=28, fallback_text="👥")
        staff_icon.setStyleSheet("color: #2D9B84; background-color: transparent;")
        staff_layout.addWidget(staff_icon, alignment=Qt.AlignmentFlag.AlignCenter)

        staff_title = QLabel("Staff Portal")
        staff_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        staff_title.setStyleSheet("color: #2D9B84; font-size: 18px; font-weight: 700; background-color: transparent;")
        staff_layout.addWidget(staff_title)

        staff_subtitle = QLabel("Login to manage enrollments")
        staff_subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        staff_subtitle.setStyleSheet(
            "color: #2D9B84; font-size: 12px; font-weight: 500; background-color: transparent;")
        staff_layout.addWidget(staff_subtitle)

        card_layout.addWidget(staff_btn)

        card_wrapper.addWidget(card)
        card_wrapper.addStretch()

        content_layout.addLayout(card_wrapper)
        content_layout.addStretch()

        main_layout.addWidget(content_container)

    def create_checkmark_logo(self, label):
        """Fallback: draw a checkmark logo when image is unavailable"""
        label.setText("")
        label.setStyleSheet("background-color: transparent;")

        # Store pixmap as instance variable to prevent garbage collection
        self.logo_pixmap = QPixmap(80, 80)
        self.logo_pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(self.logo_pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw circle background
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#2D9B84"))
        painter.drawEllipse(5, 5, 70, 70)

        # Draw checkmark
        pen = QPen(QColor("#234940"))
        pen.setWidth(8)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)

        from PyQt6.QtGui import QPainterPath
        path = QPainterPath()
        path.moveTo(25, 40)
        path.lineTo(35, 50)
        path.lineTo(55, 25)

        painter.drawPath(path)
        painter.end()

        label.setPixmap(self.logo_pixmap)