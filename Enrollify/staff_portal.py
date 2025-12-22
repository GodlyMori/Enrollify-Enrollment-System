# staff_portal.py - FIXED VERSION
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame,
    QScrollArea, QGridLayout, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox, QSizePolicy, QComboBox, QLineEdit
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap
from database_manager_mysql import get_database
import os


class StaffPortalScreen(QWidget):
    logout_signal = pyqtSignal()

    def set_current_user(self, user):
        """Set the currently logged-in staff user"""
        self.current_user = user
        print(f"✅ Staff Portal: User set to {user.get('full_name')} (ID: {user.get('id')})")

    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #F8F9FA;")
        self.db = get_database()
        self.current_tab = "analytics"
        self.current_user = None
        self.setup_ui()

    def load_icon(self, icon_name):
        """Load an icon from assets/icons/"""
        path = f"assets/icons/{icon_name}"
        if os.path.exists(path):
            pixmap = QPixmap(path).scaled(
                20, 20, Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            label = QLabel()
            label.setPixmap(pixmap)
            return label
        else:
            # Fallback to text icon if image not found
            fallback_label = QLabel(icon_name)
            fallback_label.setStyleSheet("font-size: 20px; color: #9CA3AF;")
            return fallback_label

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header
        header = self.create_header()
        main_layout.addWidget(header)

        # Navigation Tabs
        nav_tabs = self.create_nav_tabs()
        main_layout.addWidget(nav_tabs)

        # Scroll Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #F8F9FA;
            }
            QScrollBar:vertical {
                border: none;
                background: #F0F0F0;
                width: 10px;
                margin: 0px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #C0C0C0;
                border-radius: 5px;
                min-height: 20px;
            }
        """)

        # Content Container - FIXED SPACING
        self.content_container = QWidget()
        self.content_container.setStyleSheet("background-color: #F8F9FA;")
        self.content_layout = QVBoxLayout(self.content_container)
        self.content_layout.setContentsMargins(80, 60, 80, 100)  # Match admin screen
        self.content_layout.setSpacing(40)  # Match admin screen

        # Load initial content
        self.show_analytics_content()

        scroll.setWidget(self.content_container)
        main_layout.addWidget(scroll)

    def create_header(self):
        header = QFrame()
        header.setStyleSheet("QFrame { background-color: white; border: none; }")
        header.setFixedHeight(100)

        layout = QHBoxLayout(header)
        layout.setContentsMargins(40, 20, 40, 20)

        # Logo
        logo = QLabel()
        if os.path.exists('assets/enrollify_logo.png'):
            pixmap = QPixmap('assets/enrollify_logo.png').scaled(
                60, 60, Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            logo.setPixmap(pixmap)
        else:
            logo.setText("📚")
            logo.setStyleSheet("font-size: 32px; color: #060C0B;")

        # Title
        text_layout = QVBoxLayout()
        text_layout.setSpacing(4)
        title = QLabel("Enrollify")
        title.setStyleSheet("""
            font-size: 26px;
            font-weight: 700;
            color: #060C0B;
        """)
        subtitle = QLabel("Staff Portal - Enrollment Management")
        subtitle.setStyleSheet("""
            font-size: 16px;
            color: #666;
            font-weight: 500;
        """)
        text_layout.addWidget(title)
        text_layout.addWidget(subtitle)

        layout.addWidget(logo)
        layout.addLayout(text_layout)
        layout.addStretch()

        # Logout Button
        logout_btn = QPushButton("⎋ Logout")
        logout_btn.setFixedHeight(45)
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #2D9B84;
                border: 2px solid #2D9B84;
                border-radius: 10px;
                font-size: 15px;
                font-weight: 600;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #E8F4F2;
            }
        """)
        logout_btn.clicked.connect(self.logout_signal.emit)
        layout.addWidget(logout_btn)

        return header

    def create_tab_button(self, text, is_active, icon_path=None):
        btn = QPushButton()
        btn.setFixedHeight(65)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setMinimumWidth(120)
        # btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        # Create layout for icon + text
        layout = QHBoxLayout(btn)
        layout.setContentsMargins(12, 0, 12, 0)
        layout.setSpacing(8)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add icon if provided
        if icon_path and os.path.exists(icon_path):
            icon_label = QLabel()
            pixmap = QPixmap(icon_path).scaled(
                20, 20,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            icon_label.setPixmap(pixmap)
            layout.addWidget(icon_label)
        # Optional: fallback to emoji if you want (not required)
        # elif "Analytics" in text:
        #     layout.addWidget(QLabel("📊"))
        # elif "Enrollees" in text:
        #     layout.addWidget(QLabel("👥"))
        # elif "Reports" in text:
        #     layout.addWidget(QLabel("📈"))

        # Add text
        text_label = QLabel(text)
        layout.addWidget(text_label)

        # Apply styles
        if is_active:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #060C0B;
                    border: none;
                    border-bottom: 3px solid #2D9B84;
                    font-size: 16px;
                    font-weight: 600;
                    padding: 0 12px;
                }
            """)
        else:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                    color: #666;
                    font-size: 15px;
                    font-weight: 500;
                    padding: 0 12px;
                }
                QPushButton:hover {
                    background-color: #F9FAFB;
                    color: #060C0B;
                }
            """)

        return btn

    def create_nav_tabs(self):
        nav = QFrame()
        nav.setStyleSheet("QFrame { background-color: white; border: none; border-bottom: 1px solid #E5E7EB; }")
        nav.setFixedHeight(65)
        layout = QHBoxLayout(nav)
        layout.setContentsMargins(40, 0, 40, 0)
        layout.setSpacing(20)

        # Updated calls with icon paths
        self.analytics_btn = self.create_tab_button("Analytics", True, "assets/icons/analytics.png")
        self.enrollees_btn = self.create_tab_button("Enrollees", False, "assets/icons/enrollees.png")
        self.reports_btn = self.create_tab_button("Reports", False, "assets/icons/reports.png")

        self.analytics_btn.clicked.connect(lambda: self.switch_tab("analytics"))
        self.enrollees_btn.clicked.connect(lambda: self.switch_tab("enrollees"))
        self.reports_btn.clicked.connect(lambda: self.switch_tab("reports"))

        layout.addWidget(self.analytics_btn)
        layout.addWidget(self.enrollees_btn)
        layout.addWidget(self.reports_btn)
        layout.addStretch()
        return nav

    def switch_tab(self, tab_name):
        self.current_tab = tab_name

        # Reset all button styles
        buttons = [self.analytics_btn, self.enrollees_btn, self.reports_btn]
        for btn in buttons:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                    color: #666;
                    padding: 0 24px;
                    font-size: 15px;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background-color: #F9FAFB;
                    color: #060C0B;
                }
            """)

        # Activate current button
        btn_map = {
            "analytics": self.analytics_btn,
            "enrollees": self.enrollees_btn,
            "reports": self.reports_btn
        }
        active_btn = btn_map[tab_name]
        active_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #060C0B;
                border: none;
                border-bottom: 3px solid #2D9B84;
                font-size: 16px;
                font-weight: 600;
                padding: 0 24px;
            }
        """)

        # Clear old content first
        self.clear_content()

        # Force process pending events to ensure deletion
        from PyQt6.QtWidgets import QApplication
        QApplication.processEvents()

        # Load new content
        method_map = {
            "analytics": self.show_analytics_content,
            "enrollees": self.show_enrollees_content,
            "reports": self.show_reports_content
        }
        method_map[tab_name]()

    def clear_content(self):
        """Clear all content from layout - FIXED"""
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clear_layout(child.layout())

    def clear_layout(self, layout):
        """Recursively clear nested layouts"""
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clear_layout(child.layout())

    # ==================== ANALYTICS TAB ====================
    def show_analytics_content(self):
        self.clear_content()

        # Title with staff name
        if hasattr(self, 'current_user') and self.current_user:
            staff_name = self.current_user.get('full_name', 'Staff')
            title = QLabel(f"Analytics Dashboard - {staff_name}")
        else:
            title = QLabel("Analytics Dashboard")

        title.setStyleSheet("""
            font-size: 28px; 
            font-weight: 700; 
            color: #060C0B;
            background: transparent;
            border: none;
        """)
        self.content_layout.addWidget(title)

        subtitle = QLabel("Your assigned students' data")
        subtitle.setStyleSheet("""
            font-size: 14px; 
            color: #6B7280;
            background: transparent;
            border: none;
        """)
        self.content_layout.addWidget(subtitle)
        self.content_layout.addSpacing(40)

        # Top Metrics - 4 Cards (filtered by staff)
        top_cards = QHBoxLayout()
        top_cards.setSpacing(24)

        try:
            # Get staff-specific data
            if hasattr(self, 'current_user') and self.current_user:
                staff_id = self.current_user.get('id')
                my_students = self.db.get_students_by_staff(staff_id)
            else:
                my_students = []

            total = len(my_students)
            enrolled = sum(1 for s in my_students if s.get('status') == 'Enrolled')
            pending = sum(1 for s in my_students if s.get('status') == 'Pending')

            # Grade distribution from my students
            grade11 = sum(1 for s in my_students if s.get('grade') == "Grade 11")
            grade12 = sum(1 for s in my_students if s.get('grade') == "Grade 12")

            enrolled_pct = int((enrolled / total * 100)) if total > 0 else 0

            # Card 1: My Students
            card1 = self.create_metric_card(
                "My Students",
                str(total),
                "Assigned to you",
                "👥",
                "#111827"
            )

            # Card 2: Enrolled
            card2 = self.create_metric_card(
                "Enrolled",
                str(enrolled),
                f"{enrolled_pct}% of yours",
                "✓",
                "#10B981"
            )

            # Card 3: Grade 11
            card3 = self.create_metric_card(
                "Grade 11",
                str(grade11),
                "Your students",
                "🎓",
                "#3B82F6"
            )

            # Card 4: Grade 12
            card4 = self.create_metric_card(
                "Grade 12",
                str(grade12),
                "Your students",
                "📈",
                "#8B5CF6"
            )

            top_cards.addWidget(card1)
            top_cards.addWidget(card2)
            top_cards.addWidget(card3)
            top_cards.addWidget(card4)
            self.content_layout.addLayout(top_cards)

        except Exception as e:
            print(f"Error loading metrics: {e}")

        self.content_layout.addSpacing(40)

        # Charts Grid - 2x2 (using staff's data)
        charts_grid = QGridLayout()
        charts_grid.setSpacing(30)

        track_panel = self.create_my_track_distribution_panel()
        grade_panel = self.create_my_grade_distribution_panel()
        status_panel = self.create_my_status_distribution_panel()
        recent_panel = self.create_my_recent_enrollments_panel()

        charts_grid.addWidget(track_panel, 0, 0)
        charts_grid.addWidget(grade_panel, 0, 1)
        charts_grid.addWidget(status_panel, 1, 0)
        charts_grid.addWidget(recent_panel, 1, 1)

        self.content_layout.addLayout(charts_grid)
        self.content_layout.addSpacing(80)

    def create_my_track_distribution_panel(self):
        """Track distribution for MY students"""
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 16px;
                padding: 28px;
            }
        """)
        layout = QVBoxLayout(panel)
        layout.setSpacing(20)

        title = QLabel("My Students - Track Distribution")
        title.setStyleSheet("font-size: 18px; font-weight: 700; color: #060C0B;")
        layout.addWidget(title)

        try:
            if hasattr(self, 'current_user') and self.current_user:
                staff_id = self.current_user.get('id')
                my_students = self.db.get_students_by_staff(staff_id)

                # Count by track
                track_counts = {}
                for s in my_students:
                    track = s.get('track', 'Unknown')
                    track_counts[track] = track_counts.get(track, 0) + 1

                total = sum(track_counts.values()) if track_counts else 1

                for track, count in track_counts.items():
                    row = QHBoxLayout()
                    lbl = QLabel(track)
                    lbl.setStyleSheet("font-size: 14px; color: #111827;")

                    bar = QFrame()
                    bar.setFixedHeight(8)
                    bar.setStyleSheet("background-color: #059669; border-radius: 4px;")
                    bar.setFixedWidth(int((count / total) * 200))

                    val = QLabel(str(count))
                    val.setStyleSheet("font-size: 14px; color: #111827; font-weight: 600;")

                    row.addWidget(lbl)
                    row.addWidget(bar)
                    row.addWidget(val)
                    row.addStretch()
                    layout.addLayout(row)
            else:
                layout.addWidget(QLabel("No user logged in"))

        except Exception as e:
            print(f"Track error: {e}")
            layout.addWidget(QLabel("No data available"))

        layout.addStretch()
        return panel

    def create_my_grade_distribution_panel(self):
        """Grade distribution for MY students"""
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 16px;
                padding: 28px;
            }
        """)
        layout = QVBoxLayout(panel)
        layout.setSpacing(20)

        title = QLabel("My Students - Grade Distribution")
        title.setStyleSheet("font-size: 18px; font-weight: 700; color: #060C0B;")
        layout.addWidget(title)

        try:
            if hasattr(self, 'current_user') and self.current_user:
                staff_id = self.current_user.get('id')
                my_students = self.db.get_students_by_staff(staff_id)

                # Count by grade
                grade_counts = {}
                for s in my_students:
                    grade = s.get('grade', 'Unknown')
                    grade_counts[grade] = grade_counts.get(grade, 0) + 1

                total = sum(grade_counts.values()) if grade_counts else 1

                for grade, count in grade_counts.items():
                    row = QHBoxLayout()
                    lbl = QLabel(grade)
                    lbl.setStyleSheet("font-size: 14px; color: #111827;")

                    bar = QFrame()
                    bar.setFixedHeight(8)
                    bar.setStyleSheet("background-color: #2563EB; border-radius: 4px;")
                    bar.setFixedWidth(int((count / total) * 200))

                    val = QLabel(str(count))
                    val.setStyleSheet("font-size: 14px; color: #2563EB; font-weight: 600;")

                    row.addWidget(lbl)
                    row.addWidget(bar)
                    row.addWidget(val)
                    row.addStretch()
                    layout.addLayout(row)
            else:
                layout.addWidget(QLabel("No user logged in"))

        except Exception as e:
            print(f"Grade error: {e}")
            layout.addWidget(QLabel("No data available"))

        layout.addStretch()
        return panel

    def create_my_status_distribution_panel(self):
        """Status distribution for MY students"""
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 16px;
                padding: 28px;
            }
        """)
        layout = QVBoxLayout(panel)
        layout.setSpacing(20)

        title = QLabel("My Students - Status")
        title.setStyleSheet("font-size: 18px; font-weight: 700; color: #060C0B;")
        layout.addWidget(title)

        try:
            if hasattr(self, 'current_user') and self.current_user:
                staff_id = self.current_user.get('id')
                my_students = self.db.get_students_by_staff(staff_id)

                # Count by status
                status_counts = {}
                for s in my_students:
                    status = s.get('status', 'Unknown')
                    status_counts[status] = status_counts.get(status, 0) + 1

                total = sum(status_counts.values()) if status_counts else 1

                for status, count in status_counts.items():
                    color = "#10B981" if status == "Enrolled" else "#F59E0B" if status == "Pending" else "#EF4444"

                    row = QHBoxLayout()
                    lbl = QLabel(status)
                    lbl.setStyleSheet("font-size: 14px; color: #111827;")

                    bar = QFrame()
                    bar.setFixedHeight(8)
                    bar.setStyleSheet(f"background-color: {color}; border-radius: 4px;")
                    bar.setFixedWidth(int((count / total) * 200))

                    val = QLabel(str(count))
                    val.setStyleSheet(f"font-size: 14px; color: {color}; font-weight: 600;")

                    row.addWidget(lbl)
                    row.addWidget(bar)
                    row.addWidget(val)
                    row.addStretch()
                    layout.addLayout(row)
            else:
                layout.addWidget(QLabel("No user logged in"))

        except Exception as e:
            print(f"Status error: {e}")
            layout.addWidget(QLabel("No data available"))

        layout.addStretch()
        return panel

    def create_my_recent_enrollments_panel(self):
        """Recent enrollments for MY students"""
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 16px;
                padding: 28px;
            }
        """)
        layout = QVBoxLayout(panel)
        layout.setSpacing(20)

        title = QLabel("My Recent Students")
        title.setStyleSheet("font-size: 18px; font-weight: 700; color: #060C0B;")
        layout.addWidget(title)

        try:
            if hasattr(self, 'current_user') and self.current_user:
                staff_id = self.current_user.get('id')
                my_students = self.db.get_students_by_staff(staff_id)

                # Sort by created_at and get recent 5
                recent = sorted(my_students, key=lambda x: x.get('created_at', ''), reverse=True)[:5]

                for student in recent:
                    row = QHBoxLayout()

                    info_layout = QVBoxLayout()
                    info_layout.setSpacing(4)

                    name = QLabel(f"{student['firstname']} {student['lastname']}")
                    name.setStyleSheet("font-size: 14px; font-weight: 600; color: #111827;")

                    details = QLabel(f"{student['grade']} - {student['track']}")
                    details.setStyleSheet("font-size: 13px; color: #6B7280;")

                    info_layout.addWidget(name)
                    info_layout.addWidget(details)

                    date = QLabel(student.get('created_at', 'N/A').split()[0])
                    date.setStyleSheet("font-size: 13px; color: #6B7280;")

                    row.addLayout(info_layout)
                    row.addStretch()
                    row.addWidget(date)

                    layout.addLayout(row)
            else:
                layout.addWidget(QLabel("No user logged in"))

        except Exception as e:
            print(f"Recent error: {e}")
            layout.addWidget(QLabel("No recent students"))

        layout.addStretch()
        return panel

    def create_metric_card(self, title, value, subtext="", icon="", color="#6B7280"):
        """Create modern metric card matching the design"""
        card = QFrame()
        # REMOVE setFixedHeight → let layout manage height
        card.setMinimumHeight(160)  # Minimum height for consistency
        card.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 16px;
                padding: 24px;
            }}
        """)
        layout = QVBoxLayout(card)
        layout.setSpacing(16)  # Increased spacing
        layout.setContentsMargins(8, 8, 8, 8)  # Added padding

        # Icon + Title
        header_layout = QHBoxLayout()
        icon_label = self.load_icon(f"{title.lower().replace(' ', '_')}.png")
        icon_label.setStyleSheet(f"""
            font-size: 20px;
            color: {color};
            border: none;
            background: transparent;
            margin: 0;
            padding: 0;
        """)
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            font-size: 14px;
            color: #666;
            font-weight: 500;
            border: none;
            background: transparent;
            margin: 0;
            padding: 0;
        """)
        header_layout.addWidget(icon_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        layout.addLayout(header_layout)

        # Value + Subtext
        value_layout = QHBoxLayout()
        value_label = QLabel(value)
        value_label.setStyleSheet(f"""
            font-size: 32px;
            font-weight: 700;
            color: {color};
            border: none;
            background: transparent;
            margin: 0;
            padding: 0;
        """)
        if subtext:
            sub_label = QLabel(subtext)
            sub_label.setStyleSheet(f"""
                font-size: 14px;
                font-weight: 600;
                color: {color};
                border: none;
                background: transparent;
                margin: 0;
                padding: 0;
                margin-left: 12px;
            """)
            value_layout.addWidget(value_label)
            value_layout.addWidget(sub_label)
            value_layout.addStretch()
        else:
            value_layout.addWidget(value_label)
            value_layout.addStretch()
        layout.addLayout(value_layout)
        layout.addStretch()
        return card

    def create_track_distribution_panel(self):
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 16px;
                padding: 28px;
            }
        """)
        layout = QVBoxLayout(panel)
        layout.setSpacing(20)

        title = QLabel("Track Distribution")
        title.setStyleSheet("""
            font-size: 20px; 
            font-weight: 700; 
            color: #060C0B;
            background: transparent;
            border: none;
        """)
        subtitle = QLabel("Students per track")
        subtitle.setStyleSheet("""
            font-size: 20px; 
            color: #6B7280;
            background: transparent;
            border: none;
        """)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(16)

        try:
            tracks = self.db.count_by_track()
            total = sum(tracks.values()) if tracks else 1

            for track, count in tracks.items():
                row = QHBoxLayout()
                lbl = QLabel(track)
                lbl.setStyleSheet("""
                    font-size: 14px; 
                    color: #111827;
                    background: transparent;
                    border: none;
                """)

                bar = QFrame()
                bar.setFixedHeight(8)
                bar.setStyleSheet("""
                    background-color: #059669; 
                    border-radius: 4px;
                """)
                bar.setFixedWidth(int((count / total) * 200))

                val = QLabel(str(count))
                val.setStyleSheet("""
                    font-size: 14px; 
                    color: #111827; 
                    font-weight: 600;
                    background: transparent;
                    border: none;
                """)

                row.addWidget(lbl)
                row.addWidget(bar)
                row.addWidget(val)
                row.addStretch()
                layout.addLayout(row)

        except Exception as e:
            print(f"Track error: {e}")
            error_lbl = QLabel("No track data available")
            error_lbl.setStyleSheet("color: #EF4444; font-size: 13px;")
            layout.addWidget(error_lbl)

        layout.addStretch()
        return panel

    def create_grade_distribution_panel(self):
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 16px;
                padding: 28px;
            }
        """)
        layout = QVBoxLayout(panel)
        layout.setSpacing(20)

        title = QLabel("Grade Distribution")
        title.setStyleSheet("""
            font-size: 18px; 
            font-weight: 700; 
            color: #060C0B;
            background: transparent;
            border: none;
        """)
        subtitle = QLabel("Students per grade level")
        subtitle.setStyleSheet("""
            font-size: 20px; 
            color: #6B7280;
            background: transparent;
            border: none;
        """)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(16)

        try:
            grades = self.db.count_by_grade()
            total = sum(grades.values()) if grades else 1

            for grade, count in grades.items():
                row = QHBoxLayout()
                lbl = QLabel(grade)
                lbl.setStyleSheet("""
                    font-size: 14px; 
                    color: #111827;
                    background: transparent;
                    border: none;
                """)

                bar = QFrame()
                bar.setFixedHeight(8)
                bar.setStyleSheet("""
                    background-color: #2563EB; 
                    border-radius: 4px;
                """)
                bar.setFixedWidth(int((count / total) * 200))

                val = QLabel(str(count))
                val.setStyleSheet("""
                    font-size: 14px; 
                    color: #2563EB; 
                    font-weight: 600;
                    background: transparent;
                    border: none;
                """)

                row.addWidget(lbl)
                row.addWidget(bar)
                row.addWidget(val)
                row.addStretch()
                layout.addLayout(row)

        except Exception as e:
            print(f"Grade error: {e}")
            error_lbl = QLabel("No grade data available")
            error_lbl.setStyleSheet("color: #EF4444; font-size: 13px;")
            layout.addWidget(error_lbl)

        layout.addStretch()
        return panel

    def create_status_distribution_panel(self):
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 16px;
                padding: 28px;
            }
        """)
        layout = QVBoxLayout(panel)
        layout.setSpacing(20)

        title = QLabel("Enrollment Status")
        title.setStyleSheet("""
            font-size: 18px; 
            font-weight: 700; 
            color: #060C0B;
            background: transparent;
            border: none;
        """)
        subtitle = QLabel("Application status breakdown")
        subtitle.setStyleSheet("""
            font-size: 20px; 
            color: #6B7280;
            background: transparent;
            border: none;
        """)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(16)

        try:
            statuses = self.db.count_enrollment_status()

            for status, count in statuses.items():
                row = QHBoxLayout()
                lbl = QLabel(status)
                lbl.setStyleSheet("""
                    font-size: 14px; 
                    color: #111827;
                    background: transparent;
                    border: none;
                """)

                color = "#10B981" if "enrolled" in status.lower() else "#F59E0B" if "pending" in status.lower() else "#EF4444"

                bar = QFrame()
                bar.setFixedHeight(8)
                bar.setStyleSheet(f"""
                    background-color: {color}; 
                    border-radius: 4px;
                """)
                total = sum(statuses.values()) if statuses else 1
                bar.setFixedWidth(int((count / total) * 200))

                val = QLabel(str(count))
                val.setStyleSheet(f"""
                    font-size: 14px; 
                    color: {color}; 
                    font-weight: 600;
                    background: transparent;
                    border: none;
                """)

                row.addWidget(lbl)
                row.addWidget(bar)
                row.addWidget(val)
                row.addStretch()
                layout.addLayout(row)

        except Exception as e:
            print(f"Status error: {e}")
            error_lbl = QLabel("No status data available")
            error_lbl.setStyleSheet("color: #EF4444; font-size: 13px;")
            layout.addWidget(error_lbl)

        layout.addStretch()
        return panel

    def create_recent_enrollments_panel(self):
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 16px;
                padding: 28px;
            }
        """)
        layout = QVBoxLayout(panel)
        layout.setSpacing(20)

        title = QLabel("Recent Enrollments")
        title.setStyleSheet("""
            font-size: 18px; 
            font-weight: 700; 
            color: #060C0B;
            background: transparent;
            border: none;
        """)
        subtitle = QLabel("Latest enrolled students")
        subtitle.setStyleSheet("""
            font-size: 20px; 
            color: #6B7280;
            background: transparent;
            border: none;
        """)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(16)

        try:
            students = self.db.get_all_students()
            recent = sorted(students, key=lambda x: x.get('created_at', ''), reverse=True)[:5]

            for student in recent:
                row = QHBoxLayout()

                info_layout = QVBoxLayout()
                info_layout.setSpacing(4)

                name = QLabel(f"{student['firstname']} {student['lastname']}")
                name.setStyleSheet("""
                    font-size: 14px; 
                    font-weight: 600; 
                    color: #111827;
                    background: transparent;
                    border: none;
                """)

                details = QLabel(f"{student['grade']} - {student['track']}")
                details.setStyleSheet("""
                    font-size: 13px; 
                    color: #6B7280;
                    background: transparent;
                    border: none;
                """)

                info_layout.addWidget(name)
                info_layout.addWidget(details)

                date = QLabel(student.get('created_at', 'N/A').split()[0])
                date.setStyleSheet("""
                    font-size: 13px; 
                    color: #6B7280;
                    background: transparent;
                    border: none;
                """)

                row.addLayout(info_layout)
                row.addStretch()
                row.addWidget(date)

                layout.addLayout(row)

        except Exception as e:
            print(f"Recent enrollments error: {e}")
            error_lbl = QLabel("No recent enrollments")
            error_lbl.setStyleSheet("color: #EF4444; font-size: 13px;")
            layout.addWidget(error_lbl)

        layout.addStretch()
        return panel

    # ==================== ENROLLEES TAB ====================
    def show_enrollees_content(self):
        self.clear_content()

        # Title
        title = QLabel("Enrolled Students")
        title.setStyleSheet("""
            font-size: 28px; 
            font-weight: 700; 
            color: #060C0B;
            background: transparent;
            border: none;
        """)
        self.content_layout.addWidget(title)

        subtitle = QLabel("Manage and view all enrolled students")
        subtitle.setStyleSheet("""
            font-size: 20px; 
            color: #6B7280;
            background: transparent;
            border: none;
        """)
        self.content_layout.addWidget(subtitle)
        self.content_layout.addSpacing(40)

        # Filters
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(16)

        # Search
        search_frame = QFrame()
        search_frame.setStyleSheet("""
            QFrame {
                background-color: #F9FAFB;
                border: 1px solid #E5E7EB;
                border-radius: 8px;
                padding: 8px 16px;
            }
        """)
        search_layout = QHBoxLayout(search_frame)
        search_icon = self.load_icon("search.png")
        search_icon.setStyleSheet("font-size: 16px;")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name or LRN...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                background: transparent;
                border: none;
                font-size: 14px;
                color: #111827;
                padding: 4px;
            }
            QLineEdit::placeholder {
                color: #9CA3AF;
            }
        """)
        self.search_input.textChanged.connect(self.filter_enrollees)
        search_layout.addWidget(search_icon)
        search_layout.addWidget(self.search_input)

        # Grade Filter
        self.grade_combo = QComboBox()
        self.grade_combo.addItems(["All Grades", "Grade 11", "Grade 12"])
        self.grade_combo.setStyleSheet("""
            QComboBox {
                background: #F9FAFB;
                border: 1px solid #E5E7EB;
                border-radius: 8px;
                padding: 8px 16px;
                font-size: 14px;
                color: #111827;
                min-width: 120px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                color: #111827;
                background-color: white;
                selection-background-color: #E8F4F2;
                selection-color: #111827;
            }
        """)
        self.grade_combo.currentIndexChanged.connect(self.filter_enrollees)

        # Track Filter
        self.track_combo = QComboBox()
        self.track_combo.addItem("All Tracks")
        try:
            tracks = self.db.get_all_tracks()
            for track in tracks:
                self.track_combo.addItem(track)
        except:
            pass
        self.track_combo.setStyleSheet("""
            QComboBox {
                background: #F9FAFB;
                border: 1px solid #E5E7EB;
                border-radius: 8px;
                padding: 8px 16px;
                font-size: 14px;
                color: #111827;
                min-width: 120px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                color: #111827;
                background-color: white;
                selection-background-color: #E8F4F2;
                selection-color: #111827;
            }
        """)
        self.track_combo.currentIndexChanged.connect(self.filter_enrollees)

        # Status Filter
        self.status_combo = QComboBox()
        self.status_combo.addItems(["All Status", "Enrolled", "Pending", "Rejected"])
        self.status_combo.setStyleSheet("""
            QComboBox {
                background: #F9FAFB;
                border: 1px solid #E5E7EB;
                border-radius: 8px;
                padding: 8px 16px;
                font-size: 14px;
                color: #111827;
                min-width: 120px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                color: #111827;
                background-color: white;
                selection-background-color: #E8F4F2;
                selection-color: #111827;
            }
        """)
        self.status_combo.currentIndexChanged.connect(self.filter_enrollees)

        filter_layout.addWidget(search_frame)
        filter_layout.addWidget(self.grade_combo)
        filter_layout.addWidget(self.track_combo)
        filter_layout.addWidget(self.status_combo)
        filter_layout.addStretch()

        self.content_layout.addLayout(filter_layout)
        self.content_layout.addSpacing(10)  # Reduced from 20

        # Table - EXPANDED TO FILL SPACE
        self.enrollees_table = QTableWidget()
        self.enrollees_table.setColumnCount(7)
        self.enrollees_table.setHorizontalHeaderLabels(
            ["LRN", "Name", "Grade", "Track", "Status", "Contact", "Actions"])

        # Set column resize modes to fit content
        header = self.enrollees_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # LRN
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # Name
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Grade
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # Track
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)  # Status (fixed to prevent overlap)
        header.resizeSection(4, 150)  # Set Status column to 150px
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)  # Contact (email can stretch)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)  # Actions (fixed width)
        header.resizeSection(6, 120)  # Set Actions column to 120px

        self.enrollees_table.setRowHeight(0, 60)  # Increased row height
        self.enrollees_table.verticalHeader().setDefaultSectionSize(60)  # Default row height
        self.enrollees_table.setMinimumHeight(600)  # Set minimum height for table
        self.enrollees_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 12px;
                gridline-color: #F3F4F6;
                font-size: 14px;
                color: #111827;
            }
            QTableWidget::item {
                padding: 18px 16px;
                color: #111827;
                border-bottom: 1px solid #F3F4F6;
            }
            QHeaderView::section {
                background-color: #F9FAFB;
                padding: 16px 16px;
                font-size: 14px;
                font-weight: 600;
                color: #111827;
                border: none;
                border-bottom: 2px solid #E5E7EB;
            }
        """)

        # Prevent text wrapping
        self.enrollees_table.setWordWrap(False)

        self.content_layout.addWidget(self.enrollees_table, 1)  # Stretch factor = 1
        self.content_layout.addSpacing(30)  # Reduced from 80

        # Load data
        self.load_enrollees_data()

    def load_enrollees_data(self):
        """Load and display MY enrollees with filtering"""
        search_text = self.search_input.text().strip().lower()
        selected_grade = self.grade_combo.currentText()
        selected_track = self.track_combo.currentText()
        selected_status = self.status_combo.currentText()

        # Get only MY students
        if hasattr(self, 'current_user') and self.current_user:
            staff_id = self.current_user.get('id')
            students = self.db.get_students_by_staff(staff_id)
        else:
            students = []

        # Filter
        filtered = []
        for s in students:
            if search_text and search_text not in s[
                'lrn'].lower() and search_text not in f"{s['firstname']} {s['lastname']}".lower():
                continue
            if selected_grade != "All Grades" and s['grade'] != selected_grade:
                continue
            if selected_track != "All Tracks" and s['track'] != selected_track:
                continue
            if selected_status != "All Status" and s['status'] != selected_status:
                continue
            filtered.append(s)

        # Populate table (rest stays the same)
        self.enrollees_table.setRowCount(len(filtered))
        for row, student in enumerate(filtered):
            # ... (keep the existing table population code)
            # LRN
            lrn_item = QTableWidgetItem(student['lrn'])
            lrn_item.setForeground(Qt.GlobalColor.black)
            lrn_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            self.enrollees_table.setItem(row, 0, lrn_item)

            # Name
            name_item = QTableWidgetItem(f"{student['firstname']} {student['lastname']}")
            name_item.setForeground(Qt.GlobalColor.black)
            name_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            self.enrollees_table.setItem(row, 1, name_item)

            # Grade
            grade_item = QTableWidgetItem(student['grade'])
            grade_item.setForeground(Qt.GlobalColor.black)
            grade_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            self.enrollees_table.setItem(row, 2, grade_item)

            # Track
            track_item = QTableWidgetItem(student['track'])
            track_item.setForeground(Qt.GlobalColor.black)
            track_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            self.enrollees_table.setItem(row, 3, track_item)

            # Status dropdown
            status_widget = QWidget()
            status_layout = QHBoxLayout(status_widget)
            status_layout.setContentsMargins(4, 4, 4, 4)
            status_layout.setSpacing(0)

            status_combo = QComboBox()
            status_combo.addItems(["Enrolled", "Pending", "Rejected"])
            status_combo.setCurrentText(student['status'])
            status_combo.setFixedWidth(130)
            status_combo.setStyleSheet("""
                QComboBox {
                    background: white;
                    border: 1px solid #E5E7EB;
                    border-radius: 6px;
                    padding: 6px 10px;
                    font-size: 14px;
                    color: #111827;
                    font-weight: 500;
                }
            """)
            status_combo.currentTextChanged.connect(
                lambda new_status, lrn=student['lrn']: self.update_status(lrn, new_status))

            status_layout.addWidget(status_combo)
            status_layout.addStretch()
            self.enrollees_table.setCellWidget(row, 4, status_widget)

            # Contact
            email_item = QTableWidgetItem(student['email'])
            email_item.setForeground(Qt.GlobalColor.black)
            email_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            self.enrollees_table.setItem(row, 5, email_item)

            # Actions
            btn_widget = QWidget()
            btn_layout = QHBoxLayout(btn_widget)
            btn_layout.setContentsMargins(8, 4, 8, 4)
            btn_layout.setSpacing(8)

            view_btn = QPushButton("👁️")
            view_btn.setFixedSize(32, 32)
            view_btn.setStyleSheet("""
                QPushButton { background: #F3F4F6; border: none; border-radius: 6px; font-size: 16px; }
                QPushButton:hover { background: #E5E7EB; }
            """)
            view_btn.clicked.connect(lambda _, s=student: self.view_student(s))

            btn_layout.addWidget(view_btn)
            btn_layout.addStretch()

            self.enrollees_table.setCellWidget(row, 6, btn_widget)

        # Resize columns
        for col in [0, 1, 2, 3]:
            self.enrollees_table.resizeColumnToContents(col)

    def filter_enrollees(self):
        """Re-filter and reload table"""
        self.load_enrollees_data()

    def update_status(self, lrn, new_status):
        """Update student status in database - FULLY FUNCTIONAL"""
        reply = QMessageBox.question(
            self,
            "Confirm Status Change",
            f"Change status to '{new_status}' for student {lrn}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                # Update in database
                self.db.update_enrollment_status(lrn, new_status)

                # Log the action
                self.db.log_action(None, 'UPDATE_STATUS', f"Changed {lrn} status to {new_status}")

                # Show success message
                QMessageBox.information(
                    self,
                    "Success",
                    f"Status successfully updated to '{new_status}'"
                )

                # Refresh the enrollees table to show updated data
                self.load_enrollees_data()

                print(f"✅ Database updated: {lrn} → {new_status}")

            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Failed to update status: {str(e)}"
                )
                print(f"❌ Error updating status: {e}")
                # Reload data to revert any UI changes
                self.load_enrollees_data()

    def view_student(self, student):
        """View student details"""
        from PyQt6.QtWidgets import QDialog, QFormLayout

        dialog = QDialog(self)
        dialog.setWindowTitle(f"Student: {student['firstname']} {student['lastname']}")
        dialog.resize(500, 600)

        layout = QVBoxLayout(dialog)
        form = QFormLayout()

        fields = [
            ("LRN", student['lrn']),
            ("Name", f"{student['firstname']} {student['lastname']}"),
            ("Grade", student['grade']),
            ("Track", student['track']),
            ("Gender", student['gender']),
            ("Email", student['email']),
            ("Phone", student['phone']),
            ("Status", student['status'])
        ]

        for label, value in fields:
            form.addRow(label, QLabel(str(value)))

        layout.addLayout(form)

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn)

        dialog.exec()

    def delete_student(self, student):
        """Delete student"""
        reply = QMessageBox.question(self, "Confirm",
                                     f"Delete {student['firstname']} {student['lastname']}?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.db.delete_student(student['lrn'])
                QMessageBox.information(self, "Success", "Student deleted")
                self.load_enrollees_data()
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    # ==================== REPORTS TAB ====================
    def show_reports_content(self):
        self.clear_content()

        # Title
        title = QLabel("Reports")
        title.setStyleSheet("""
            font-size: 28px; 
            font-weight: 700; 
            color: #060C0B;
            background: transparent;
            border: none;
        """)
        self.content_layout.addWidget(title)

        subtitle = QLabel("Enrollment statistics and distributions")
        subtitle.setStyleSheet("""
            font-size: 20px; 
            color: #6B7280;
            background: transparent;
            border: none;
        """)
        self.content_layout.addWidget(subtitle)
        self.content_layout.addSpacing(40)

        # Reports Grid - 2x2
        reports_grid = QGridLayout()
        reports_grid.setSpacing(30)

        enrollment_panel = self.create_enrollment_report_panel()
        track_report_panel = self.create_track_report_panel()
        grade_report_panel = self.create_grade_report_panel()
        strand_report_panel = self.create_strand_report_panel()

        reports_grid.addWidget(enrollment_panel, 0, 0)
        reports_grid.addWidget(track_report_panel, 0, 1)
        reports_grid.addWidget(grade_report_panel, 1, 0)
        reports_grid.addWidget(strand_report_panel, 1, 1)

        self.content_layout.addLayout(reports_grid)
        self.content_layout.addSpacing(80)

    def create_enrollment_report_panel(self):
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 16px;
                padding: 32px;
            }
        """)
        layout = QVBoxLayout(panel)
        layout.setSpacing(20)

        title = QLabel("Enrollment Status")
        title.setStyleSheet("""
            font-size: 16px; 
            font-weight: 700; 
            color: #060C0B;
            background: transparent;
            border: none;
        """)
        subtitle = QLabel("Current status breakdown")
        subtitle.setStyleSheet("""
            font-size: 20px; 
            color: #6B7280;
            background: transparent;
            border: none;
        """)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(16)

        try:
            stats = self.db.get_statistics()

            rows = [
                ("Total Enrollees", stats['total_students'], "#F3F4F6"),
                ("Enrolled", stats['enrolled'], "#DCFCE7"),
                ("Pending", stats['pending'], "#FEF3C7")
            ]

            for label, value, bg in rows:
                row = QHBoxLayout()
                lbl = QLabel(label)
                lbl.setStyleSheet("""
                    font-size: 14px; 
                    color: #111827;
                    background: transparent;
                    border: none;
                """)
                val = QLabel(str(value))
                val.setStyleSheet(f"""
                    font-size: 14px; 
                    color: #111827; 
                    background: {bg}; 
                    padding: 4px 8px; 
                    border-radius: 8px; 
                    font-weight: 600;
                    border: none;
                """)
                row.addWidget(lbl)
                row.addStretch()
                row.addWidget(val)
                layout.addLayout(row)

        except Exception as e:
            print(f"Enrollment report error: {e}")
            error_lbl = QLabel("No enrollment data")
            error_lbl.setStyleSheet("color: #EF4444; font-size: 13px;")
            layout.addWidget(error_lbl)

        layout.addStretch()
        return panel

    def create_track_report_panel(self):
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 16px;
                padding: 32px;
            }
        """)
        layout = QVBoxLayout(panel)
        layout.setSpacing(20)

        title = QLabel("Track Distribution")
        title.setStyleSheet("""
            font-size: 16px; 
            font-weight: 700; 
            color: #060C0B;
            background: transparent;
            border: none;
        """)
        subtitle = QLabel("Students per track")
        subtitle.setStyleSheet("""
            font-size: 20px; 
            color: #6B7280;
            background: transparent;
            border: none;
        """)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(16)

        try:
            tracks = self.db.count_by_track()

            for track, count in tracks.items():
                row = QHBoxLayout()
                lbl = QLabel(track)
                lbl.setStyleSheet("""
                    font-size: 14px; 
                    color: #111827;
                    background: transparent;
                    border: none;
                """)
                val = QLabel(str(count))
                val.setStyleSheet("""
                    font-size: 14px; 
                    color: #111827; 
                    background: #F0fdfa; 
                    padding: 4px 8px; 
                    border-radius: 8px; 
                    font-weight: 600;
                    border: none;
                """)
                row.addWidget(lbl)
                row.addStretch()
                row.addWidget(val)
                layout.addLayout(row)

        except Exception as e:
            print(f"Track report error: {e}")
            error_lbl = QLabel("No track data")
            error_lbl.setStyleSheet("color: #EF4444; font-size: 13px;")
            layout.addWidget(error_lbl)

        layout.addStretch()
        return panel

    def create_grade_report_panel(self):
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 16px;
                padding: 32px;
            }
        """)
        layout = QVBoxLayout(panel)
        layout.setSpacing(20)

        title = QLabel("Grade Distribution")
        title.setStyleSheet("""
            font-size: 16px; 
            font-weight: 700; 
            color: #060C0B;
            background: transparent;
            border: none;
        """)
        subtitle = QLabel("Students per grade level")
        subtitle.setStyleSheet("""
            font-size: 20px; 
            color: #6B7280;
            background: transparent;
            border: none;
        """)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(16)

        try:
            grades = self.db.count_by_grade()

            for grade, count in grades.items():
                row = QHBoxLayout()
                lbl = QLabel(grade)
                lbl.setStyleSheet("""
                    font-size: 14px; 
                    color: #111827;
                    background: transparent;
                    border: none;
                """)
                val = QLabel(str(count))
                val.setStyleSheet("""
                    font-size: 14px; 
                    color: #111827; 
                    background: #DBEAFE; 
                    padding: 4px 8px; 
                    border-radius: 8px; 
                    font-weight: 600;
                    border: none;
                """)
                row.addWidget(lbl)
                row.addStretch()
                row.addWidget(val)
                layout.addLayout(row)

        except Exception as e:
            print(f"Grade report error: {e}")
            error_lbl = QLabel("No grade data")
            error_lbl.setStyleSheet("color: #EF4444; font-size: 13px;")
            layout.addWidget(error_lbl)

        layout.addStretch()
        return panel

    def create_strand_report_panel(self):
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 16px;
                padding: 32px;
            }
        """)
        layout = QVBoxLayout(panel)
        layout.setSpacing(20)

        title = QLabel("Strand Distribution")
        title.setStyleSheet("""
            font-size: 16px; 
            font-weight: 700; 
            color: #060C0B;
            background: transparent;
            border: none;
        """)
        subtitle = QLabel("Students per strand")
        subtitle.setStyleSheet("""
            font-size: 20px; 
            color: #6B7280;
            background: transparent;
            border: none;
        """)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(16)

        try:
            strands = self.db.count_by_strand()

            for strand, count in strands.items():
                row = QHBoxLayout()
                lbl = QLabel(strand)
                lbl.setStyleSheet("""
                    font-size: 14px; 
                    color: #111827;
                    background: transparent;
                    border: none;
                """)
                val = QLabel(str(count))
                val.setStyleSheet("""
                    font-size: 14px; 
                    color: #111827; 
                    background: #F3E8FF; 
                    padding: 4px 8px; 
                    border-radius: 8px; 
                    font-weight: 600;
                    border: none;
                """)
                row.addWidget(lbl)
                row.addStretch()
                row.addWidget(val)
                layout.addLayout(row)

        except Exception as e:
            print(f"Strand report error: {e}")
            error_lbl = QLabel("No strand data")
            error_lbl.setStyleSheet("color: #EF4444; font-size: 13px;")
            layout.addWidget(error_lbl)

        layout.addStretch()
        return panel