from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame,
    QScrollArea, QGridLayout, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox, QApplication, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QPixmap, QIcon
import os
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QListWidget, QMessageBox

plt.style.use('default')
from database_manager_mysql import get_database


class AdminScreen(QWidget):
    logout_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #F8F9FA;")
        self.current_tab = "overview"
        self.db = get_database()
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        header = self.create_header()
        main_layout.addWidget(header)

        nav_tabs = self.create_nav_tabs()
        main_layout.addWidget(nav_tabs)

        # Scroll area
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
            QScrollBar::handle:vertical:hover {
                background: #A0A0A0;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        self.content_container = QWidget()
        self.content_container.setStyleSheet("background-color: #F8F9FA;")
        self.content_layout = QVBoxLayout(self.content_container)
        self.content_layout.setContentsMargins(80, 60, 80, 100)
        self.content_layout.setSpacing(40)
        self.show_overview_content()
        scroll.setWidget(self.content_container)
        main_layout.addWidget(scroll)

    def create_header(self):
        header = QFrame()
        header.setStyleSheet("QFrame { background-color: #FFFFFF; border: none; }")
        header.setFixedHeight(100)
        layout = QHBoxLayout(header)
        layout.setContentsMargins(40, 20, 40, 20)

        # Logo
        logo = QLabel()
        if os.path.exists('assets/enrollify_logo.png'):
            pixmap = QPixmap('assets/enrollify_logo.png').scaled(
                50, 50, Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            logo.setPixmap(pixmap)
        else:
            logo.setText("ðŸ“š")
            logo.setStyleSheet("font-size: 32px;")

        # Text
        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)
        title = QLabel("Enrollify")
        title.setStyleSheet("font-size: 24px; font-weight: 700; color: #060C0B;")
        subtitle = QLabel("Admin Panel - System Administration")
        subtitle.setStyleSheet("font-size: 14px; color: #666; font-weight: 500;")
        text_layout.addWidget(title)
        text_layout.addWidget(subtitle)
        layout.addWidget(logo)
        layout.addLayout(text_layout)
        layout.addStretch()

        # Logout Button - should be around line 122
        logout_btn = QPushButton("Logout")
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
        # âœ… THIS LINE IS CRITICAL
        logout_btn.clicked.connect(self.logout_signal.emit)
        layout.addWidget(logout_btn)
        return header

    def create_nav_tabs(self):
        nav_container = QFrame()
        nav_container.setStyleSheet("""
            QFrame {
                background-color: #F3F4F6;
                border-radius: 20px;
                padding: 4px;
                margin: 0 40px;
            }
        """)
        nav_container.setFixedHeight(50)

        layout = QHBoxLayout(nav_container)
        layout.setContentsMargins(8, 0, 8, 0)
        layout.setSpacing(0)

        active_style = """
            QPushButton {
                background-color: white;
                color: #060C0B;
                border: none;
                border-radius: 16px;
                font-size: 14px;
                font-weight: 600;
                padding: 8px 20px;
            }
        """

        inactive_style = """
            QPushButton {
                background-color: transparent;
                color: #666;
                border: none;
                font-size: 14px;
                font-weight: 500;
                padding: 8px 20px;
            }
            QPushButton:hover {
                background-color: #E5E7EB;
                color: #060C0B;
            }
        """

        self.overview_btn = QPushButton("📊 Overview")
        self.analytics_btn = QPushButton("📈 Analytics")
        self.data_btn = QPushButton("💾 Data")
        self.staff_btn = QPushButton("👥 Staff")  # NEW TAB
        self.system_btn = QPushButton("⚙️ System")

        self.overview_btn.setStyleSheet(active_style)
        self.analytics_btn.setStyleSheet(inactive_style)
        self.data_btn.setStyleSheet(inactive_style)
        self.staff_btn.setStyleSheet(inactive_style)  # NEW
        self.system_btn.setStyleSheet(inactive_style)

        self.overview_btn.clicked.connect(lambda: self.switch_tab("overview"))
        self.analytics_btn.clicked.connect(lambda: self.switch_tab("analytics"))
        self.data_btn.clicked.connect(lambda: self.switch_tab("data"))
        self.staff_btn.clicked.connect(lambda: self.switch_tab("staff"))  # NEW
        self.system_btn.clicked.connect(lambda: self.switch_tab("system"))

        layout.addWidget(self.overview_btn)
        layout.addWidget(self.analytics_btn)
        layout.addWidget(self.data_btn)
        layout.addWidget(self.staff_btn)  # NEW
        layout.addWidget(self.system_btn)

        return nav_container

    def switch_tab(self, tab_name):
        """Switch between tabs with proper cleanup"""
        self.current_tab = tab_name

        # Reset styles for all buttons
        buttons = [self.overview_btn, self.analytics_btn, self.data_btn, self.staff_btn, self.system_btn]
        for btn in buttons:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                    color: #666;
                    font-size: 14px;
                    font-weight: 500;
                    padding: 8px 20px;
                }
                QPushButton:hover {
                    background-color: #E5E7EB;
                    color: #060C0B;
                }
            """)

        # Activate current button
        btn_map = {
            "overview": self.overview_btn,
            "analytics": self.analytics_btn,
            "data": self.data_btn,
            "staff": self.staff_btn,  # NEW
            "system": self.system_btn
        }
        active_btn = btn_map[tab_name]
        active_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #060C0B;
                border: none;
                border-radius: 16px;
                font-size: 14px;
                font-weight: 600;
                padding: 8px 20px;
            }
        """)

        # Clear and load content
        self.clear_content()
        QApplication.processEvents()
        QTimer.singleShot(10, lambda: self.load_tab_content(tab_name))

    def load_tab_content(self, tab_name):
        """Load content for the selected tab"""
        method_map = {
            "overview": self.show_overview_content,
            "analytics": self.show_analytics_content,
            "data": self.show_data_content,
            "staff": self.show_staff_content,  # NEW
            "system": self.show_system_content
        }
        method_map[tab_name]()

    def clear_content(self):
        """Clear all content from layout - IMPROVED"""
        # Delete all child widgets recursively
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                widget = item.widget()
                widget.setParent(None)
                widget.deleteLater()
            elif item.layout():
                self.clear_layout_recursive(item.layout())

        # Force garbage collection
        QApplication.processEvents()

    def clear_layout_recursive(self, layout):
        """Recursively clear a layout and all its children"""
        if layout is None:
            return

        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                widget = item.widget()
                widget.setParent(None)
                widget.deleteLater()
            elif item.layout():
                self.clear_layout_recursive(item.layout())

    def create_metric_card(self, title, value, subtext="", icon="", color="#6B7280", border_color=""):
        card = QFrame()
        card.setFixedHeight(150)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: 1px solid {border_color if border_color else '#E5E7EB'};
                border-radius: 16px;
                padding: 24px;
            }}
        """)
        layout = QVBoxLayout(card)
        layout.setSpacing(12)
        layout.setContentsMargins(0, 0, 0, 0)

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
        layout.addWidget(title_label)

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
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"""
            font-size: 20px;
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
                margin-left: 8px;
            """)
            value_layout.addWidget(value_label)
            value_layout.addWidget(icon_label)
            value_layout.addWidget(sub_label)
            value_layout.addStretch()
        else:
            value_layout.addWidget(value_label)
            value_layout.addWidget(icon_label)
            value_layout.addStretch()

        layout.addLayout(value_layout)
        layout.addStretch()
        return card

    def create_quick_stats_panel(self):
        panel = QFrame()
        panel.setMinimumHeight(200)
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

        title = QLabel("Quick Stats")
        title.setStyleSheet("""
            font-size: 18px;
            font-weight: 700;
            color: #060C0B;
            border: none;
            background: transparent;
        """)
        subtitle = QLabel("System-wide statistics")
        subtitle.setStyleSheet("""
            font-size: 13px;
            color: #666;
            border: none;
            background: transparent;
        """)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(16)

        try:
            students = self.db.get_all_students()
            tracks = len(set(s['track'] for s in students))
            strands = len(set(s['strand'] for s in students if s.get('strand')))
            grades = len(set(s['grade'] for s in students))
            rejected = sum(1 for s in students if s.get('status', '').lower() in ['rejected', 'cancelled', 'dropped'])

            stats = [
                ("Total Tracks", tracks),
                ("Total Strands", strands),
                ("Grade Levels", grades),
                ("Rejected Applications", rejected)
            ]

            for label, value in stats:
                row = QHBoxLayout()
                lbl = QLabel(label)
                lbl.setStyleSheet("""
                    font-size: 14px;
                    color: #333;
                    border: none;
                    background: transparent;
                """)
                val = QLabel(str(value))
                val.setStyleSheet("""
                    font-size: 14px;
                    font-weight: 600;
                    color: #111827;
                    padding: 4px 12px;
                    background: #F3F4F6;
                    border-radius: 8px;
                    border: none;
                """)
                if label == "Rejected Applications":
                    val.setStyleSheet("""
                        font-size: 14px;
                        font-weight: 600;
                        color: #DC2626;
                        padding: 4px 12px;
                        background: #FEE2E2;
                        border-radius: 8px;
                        border: none;
                    """)
                row.addWidget(lbl)
                row.addWidget(val)
                row.addStretch()
                layout.addLayout(row)
        except Exception as e:
            err = QLabel("âš ï¸ Data unavailable")
            err.setStyleSheet("""
                color: #EF4444;
                font-size: 13px;
                border: none;
                background: transparent;
            """)
            layout.addWidget(err)

        return panel

    def create_gender_distribution_panel(self):
        panel = QFrame()
        panel.setMinimumHeight(200)
        panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 16px;
                padding: 28px;
            }
        """)
        layout = QVBoxLayout(panel)
        layout.setSpacing(24)

        title = QLabel("Gender Distribution")
        title.setStyleSheet("""
            font-size: 18px;
            font-weight: 700;
            color: #060C0B;
            border: none;
            background: transparent;
        """)
        subtitle = QLabel("Student demographics")
        subtitle.setStyleSheet("""
            font-size: 13px;
            color: #666;
            border: none;
            background: transparent;
        """)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(16)

        try:
            gender_data = self.db.get_gender_distribution()
            gender_dict = dict(gender_data)
            male = gender_dict.get('Male', 0)
            female = gender_dict.get('Female', 0)
            total = male + female or 1

            for gender, count, color in [("Male", male, "#1F2937"), ("Female", female, "#374151")]:
                row_layout = QHBoxLayout()
                lbl = QLabel(gender)
                lbl.setStyleSheet("""
                    font-size: 14px;
                    color: #333;
                    border: none;
                    background: transparent;
                """)

                bar_container = QFrame()
                bar_container.setFixedHeight(8)
                bar_container.setStyleSheet("background-color: #E5E7EB; border-radius: 4px;")

                bar = QFrame(bar_container)
                bar.setFixedHeight(8)
                bar.setStyleSheet(f"background-color: {color}; border-radius: 4px;")
                bar_width = max(20, int((count / total) * 200))  # Minimum 20px for visibility
                bar.setMaximumWidth(bar_width)
                bar.setFixedWidth(bar_width)

                bar_layout = QHBoxLayout(bar_container)
                bar_layout.setContentsMargins(0, 0, 0, 0)
                bar_layout.addWidget(bar)
                bar_layout.addStretch()

                val = QLabel(str(count))
                val.setStyleSheet("""
                    font-size: 14px;
                    color: #333;
                    border: none;
                    background: transparent;
                """)
                row_layout.addWidget(lbl)
                row_layout.addWidget(bar_container)
                row_layout.addWidget(val)
                row_layout.addStretch()
                layout.addLayout(row_layout)
        except Exception as e:
            err = QLabel("âš ï¸ Gender data unavailable")
            err.setStyleSheet("""
                color: #EF4444;
                font-size: 13px;
                border: none;
                background: transparent;
            """)
            layout.addWidget(err)

        return panel

    # ==================== OVERVIEW TAB ====================
    def show_overview_content(self):
        """Show overview content with accurate data"""
        self.clear_content()

        title = QLabel("Admin Overview")
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: 700;
            color: #060C0B;
            border: none;
            background: transparent;
        """)
        self.content_layout.addWidget(title)

        subtitle = QLabel("System statistics and key metrics")
        subtitle.setStyleSheet("""
            font-size: 14px;
            color: #666;
            border: none;
            background: transparent;
        """)
        self.content_layout.addWidget(subtitle)

        self.content_layout.addSpacing(40)

        # Top metrics cards
        top_cards_layout = QHBoxLayout()
        top_cards_layout.setSpacing(24)
        top_cards_layout.setContentsMargins(0, 0, 0, 0)

        try:
            stats = self.db.get_statistics()
            total_students = stats['total_students']
            enrolled = stats['enrolled']
            pending = stats['pending']

            enrolled_pct = int((enrolled / total_students * 100)) if total_students > 0 else 0
            pending_pct = int((pending / total_students * 100)) if total_students > 0 else 0

            # ✅ CALCULATE RECENT ENROLLMENTS (Last 30 days)
            recent_30_days = self.get_recent_enrollments(30)

            card1 = self.create_metric_card(
                "Total Enrollments", str(total_students),
                icon="●", color="#111827", border_color="#E5E7EB"
            )

            card2 = self.create_metric_card(
                "Enrolled Students", str(enrolled), subtext=f"{enrolled_pct}%",
                icon="✓", color="#10B981", border_color="#D1FAE5"
            )

            card3 = self.create_metric_card(
                "Pending Review", str(pending), subtext=f"{pending_pct}%",
                icon="○", color="#F59E0B", border_color="#FEF3C7"
            )

            card4 = self.create_metric_card(
                "Recent (30 days)", str(recent_30_days),
                icon="▲", color="#3B82F6", border_color="#DBEAFE"
            )

            top_cards_layout.addWidget(card1)
            top_cards_layout.addWidget(card2)
            top_cards_layout.addWidget(card3)
            top_cards_layout.addWidget(card4)

            self.content_layout.addLayout(top_cards_layout)

        except Exception as e:
            print(f"Error loading top stats: {e}")
            error_label = QLabel("⚠️ Error loading metrics")
            error_label.setStyleSheet("""
                color: #EF4444; font-size: 14px; padding: 20px;
                background: #FEF2F2; border-radius: 12px; border: none;
            """)
            self.content_layout.addWidget(error_label)

        self.content_layout.addSpacing(50)

        # Bottom section - 2x2 grid
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(40)
        bottom_layout.setContentsMargins(0, 0, 0, 0)

        # Left column
        left_column = QVBoxLayout()
        left_column.setSpacing(30)
        left_column.addWidget(self.create_quick_stats_panel())
        left_column.addWidget(self.create_enrollment_status_panel())

        # Right column
        right_column = QVBoxLayout()
        right_column.setSpacing(30)
        right_column.addWidget(self.create_gender_distribution_panel())
        right_column.addWidget(self.create_track_distribution_mini_panel())

        bottom_layout.addLayout(left_column, 1)
        bottom_layout.addLayout(right_column, 1)

        self.content_layout.addLayout(bottom_layout)
        self.content_layout.addSpacing(80)

        spacer = QSpacerItem(20, 100, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.content_layout.addItem(spacer)

    def get_recent_enrollments(self, days=30):
        """Get number of enrollments in last N days"""
        try:
            from datetime import datetime, timedelta

            conn = self.db.get_connection()
            cursor = conn.cursor()

            cutoff_date = datetime.now() - timedelta(days=days)
            cutoff_str = cutoff_date.strftime('%Y-%m-%d %H:%M:%S')

            cursor.execute('''
                           SELECT COUNT(*)
                           FROM students
                           WHERE created_at >= %s
                           ''', (cutoff_str,))

            count = cursor.fetchone()[0]
            cursor.close()
            return count

        except Exception as e:
            print(f"Error calculating recent enrollments: {e}")
            return 0

    def create_enrollment_status_panel(self):
        """Create enrollment status breakdown panel"""
        panel = QFrame()
        panel.setMinimumHeight(200)
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
        title.setStyleSheet("font-size: 18px; font-weight: 700; color: #060C0B;")
        subtitle = QLabel("Current status breakdown")
        subtitle.setStyleSheet("font-size: 13px; color: #666;")
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(16)

        try:
            statuses = self.db.count_enrollment_status()
            total = sum(statuses.values()) if statuses else 1

            status_colors = {
                'Enrolled': '#10B981', 'Pending': '#F59E0B',
                'Rejected': '#EF4444', 'Cancelled': '#6B7280', 'Dropped': '#9CA3AF'
            }

            for status, count in statuses.items():
                percentage = int((count / total) * 100)
                color = status_colors.get(status, '#6B7280')

                row_layout = QHBoxLayout()

                lbl = QLabel(status)
                lbl.setStyleSheet("font-size: 14px; color: #333;")
                lbl.setFixedWidth(100)

                bar_container = QFrame()
                bar_container.setFixedHeight(8)
                bar_container.setStyleSheet("background-color: #E5E7EB; border-radius: 4px;")

                bar = QFrame(bar_container)
                bar.setFixedHeight(8)
                bar.setStyleSheet(f"background-color: {color}; border-radius: 4px;")
                bar_width = max(20, int((count / total) * 200))
                bar.setFixedWidth(bar_width)

                bar_layout = QHBoxLayout(bar_container)
                bar_layout.setContentsMargins(0, 0, 0, 0)
                bar_layout.addWidget(bar)
                bar_layout.addStretch()

                val = QLabel(f"{count} ({percentage}%)")
                val.setStyleSheet(f"font-size: 14px; color: {color}; font-weight: 600;")

                row_layout.addWidget(lbl)
                row_layout.addWidget(bar_container, 1)
                row_layout.addWidget(val)
                row_layout.addStretch()
                layout.addLayout(row_layout)

        except Exception as e:
            print(f"Error: {e}")
            layout.addWidget(QLabel("⚠️ Data unavailable"))

        layout.addStretch()
        return panel

    def create_track_distribution_mini_panel(self):
        """Create compact track distribution panel"""
        panel = QFrame()
        panel.setMinimumHeight(200)
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
        title.setStyleSheet("font-size: 18px; font-weight: 700; color: #060C0B;")
        subtitle = QLabel("Students per track")
        subtitle.setStyleSheet("font-size: 13px; color: #666;")
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(16)

        try:
            tracks = self.db.count_by_track()
            total = sum(tracks.values()) if tracks else 1

            track_colors = ['#8B5CF6', '#EC4899', '#F59E0B', '#10B981']

            for idx, (track, count) in enumerate(tracks.items()):
                percentage = int((count / total) * 100)
                color = track_colors[idx % len(track_colors)]

                row_layout = QHBoxLayout()

                lbl = QLabel(track[:20])
                lbl.setStyleSheet("font-size: 14px; color: #333;")
                lbl.setFixedWidth(120)

                bar_container = QFrame()
                bar_container.setFixedHeight(8)
                bar_container.setStyleSheet("background-color: #E5E7EB; border-radius: 4px;")

                bar = QFrame(bar_container)
                bar.setFixedHeight(8)
                bar.setStyleSheet(f"background-color: {color}; border-radius: 4px;")
                bar_width = max(20, int((count / total) * 150))
                bar.setFixedWidth(bar_width)

                bar_layout = QHBoxLayout(bar_container)
                bar_layout.setContentsMargins(0, 0, 0, 0)
                bar_layout.addWidget(bar)
                bar_layout.addStretch()

                val = QLabel(str(count))
                val.setStyleSheet(f"font-size: 14px; color: {color}; font-weight: 600;")

                row_layout.addWidget(lbl)
                row_layout.addWidget(bar_container, 1)
                row_layout.addWidget(val)
                row_layout.addStretch()
                layout.addLayout(row_layout)

        except Exception as e:
            print(f"Error: {e}")
            layout.addWidget(QLabel("⚠️ No track data"))

        layout.addStretch()
        return panel

    def create_receipts_panel(self):
        """Panel for viewing all payment receipts"""
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

        # Header
        header_layout = QHBoxLayout()

        title = QLabel("Payment Receipts")
        title.setStyleSheet("font-size: 20px; font-weight: 700; color: #060C0B;")

        search_input = QLineEdit()
        search_input.setPlaceholderText("🔍 Search by receipt #, LRN, or student name...")
        search_input.setFixedHeight(40)
        search_input.setFixedWidth(350)
        search_input.setStyleSheet("""
            QLineEdit {
                background: #F9FAFB;
                border: 1px solid #E5E7EB;
                border-radius: 8px;
                padding: 0 15px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #2D9B84;
            }
        """)

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(search_input)

        layout.addLayout(header_layout)

        # Receipt table
        from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView

        table = QTableWidget()
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels([
            "Receipt #", "Student", "LRN", "Amount", "Date", "Actions"
        ])

        # Style table
        table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: none;
                gridline-color: #F3F4F6;
            }
            QTableWidget::item {
                padding: 12px;
                border-bottom: 1px solid #F3F4F6;
            }
            QHeaderView::section {
                background-color: #F9FAFB;
                padding: 12px;
                font-weight: 700;
                font-size: 13px;
                color: #111827;
                border: none;
                border-bottom: 2px solid #E5E7EB;
            }
        """)

        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.verticalHeader().setVisible(False)
        table.setMinimumHeight(400)

        # Load receipts
        try:
            receipts = self.db.get_all_receipts(limit=50)
            table.setRowCount(len(receipts))

            for row, receipt in enumerate(receipts):
                # Receipt number
                receipt_item = QTableWidgetItem(receipt['receipt_number'])
                table.setItem(row, 0, receipt_item)

                # Student name
                name_item = QTableWidgetItem(f"{receipt['firstname']} {receipt['lastname']}")
                table.setItem(row, 1, name_item)

                # LRN
                lrn_item = QTableWidgetItem(receipt['lrn'])
                table.setItem(row, 2, lrn_item)

                # Amount
                amount_item = QTableWidgetItem(f"₱{receipt['amount']:,.2f}")
                table.setItem(row, 3, amount_item)

                # Date
                date_str = receipt['payment_date'].strftime("%b %d, %Y") if receipt.get('payment_date') else "N/A"
                date_item = QTableWidgetItem(date_str)
                table.setItem(row, 4, date_item)

                # Actions button
                actions_widget = QWidget()
                actions_layout = QHBoxLayout(actions_widget)
                actions_layout.setContentsMargins(8, 4, 8, 4)

                view_btn = QPushButton("👁️ View")
                view_btn.setFixedHeight(32)
                view_btn.setStyleSheet("""
                    QPushButton {
                        background: #F3F4F6;
                        border: none;
                        border-radius: 6px;
                        font-size: 13px;
                        font-weight: 600;
                        padding: 0 12px;
                    }
                    QPushButton:hover {
                        background: #E5E7EB;
                    }
                """)
                view_btn.clicked.connect(lambda _, r=receipt: self.view_receipt_details(r))

                actions_layout.addWidget(view_btn)
                actions_layout.addStretch()

                table.setCellWidget(row, 5, actions_widget)

        except Exception as e:
            print(f"Error loading receipts: {e}")

        layout.addWidget(table)

        # Search functionality
        def search_receipts():
            query = search_input.text().strip()
            if query:
                results = self.db.search_receipt(query)
                table.setRowCount(len(results))

                for row, receipt in enumerate(results):
                    # Populate table with search results
                    table.setItem(row, 0, QTableWidgetItem(receipt['receipt_number']))
                    table.setItem(row, 1, QTableWidgetItem(f"{receipt['firstname']} {receipt['lastname']}"))
                    table.setItem(row, 2, QTableWidgetItem(receipt['lrn']))
                    table.setItem(row, 3, QTableWidgetItem(f"₱{receipt['amount']:,.2f}"))
                    date_str = receipt['payment_date'].strftime("%b %d, %Y") if receipt.get('payment_date') else "N/A"
                    table.setItem(row, 4, QTableWidgetItem(date_str))

                    # Actions button
                    actions_widget = QWidget()
                    actions_layout = QHBoxLayout(actions_widget)
                    actions_layout.setContentsMargins(8, 4, 8, 4)

                    view_btn = QPushButton("👁️ View")
                    view_btn.setFixedHeight(32)
                    view_btn.setStyleSheet("""
                        QPushButton {
                            background: #F3F4F6;
                            border: none;
                            border-radius: 6px;
                            font-size: 13px;
                            font-weight: 600;
                            padding: 0 12px;
                        }
                        QPushButton:hover { background: #E5E7EB; }
                    """)
                    view_btn.clicked.connect(lambda _, r=receipt: self.view_receipt_details(r))

                    actions_layout.addWidget(view_btn)
                    actions_layout.addStretch()

                    table.setCellWidget(row, 5, actions_widget)
            else:
                # Reload all receipts
                self.show_data_content()  # Or refresh current view

        search_input.returnPressed.connect(search_receipts)

        return panel

    def view_receipt_details(self, receipt_data):
        """View receipt details and allow reprint"""
        from receipt_dialog import ReceiptDialog

        # Convert receipt data to payment_data format
        payment_data = {
            'student_data': {
                'firstname': receipt_data.get('firstname', ''),
                'middlename': receipt_data.get('middlename', ''),
                'lastname': receipt_data.get('lastname', ''),
                'lrn': receipt_data.get('lrn', ''),
                'grade': receipt_data.get('grade', ''),
                'track': receipt_data.get('track', ''),
                'strand': receipt_data.get('strand', '')
            },
            'amount': receipt_data.get('amount', 0),
            'payment_method': receipt_data.get('payment_method', '')
        }

        receipt_number = receipt_data.get('receipt_number', 'N/A')

        # Show receipt dialog
        receipt_dialog = ReceiptDialog(payment_data, receipt_number, self)
        receipt_dialog.exec()

    # ==================== ANALYTICS TAB ====================
    def show_analytics_content(self):
        self.clear_content()

        title = QLabel("Analytics Dashboard")
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: 700;
            color: #060C0B;
            border: none;
            background: transparent;
        """)
        self.content_layout.addWidget(title)

        subtitle = QLabel("Visual insights from enrollment data")
        subtitle.setStyleSheet("""
            font-size: 14px;
            color: #666;
            border: none;
            background: transparent;
        """)
        self.content_layout.addWidget(subtitle)

        self.content_layout.addSpacing(40)

        # ==================== 2x2 GRID LAYOUT ====================
        grid_layout = QGridLayout()
        grid_layout.setSpacing(30)
        grid_layout.setContentsMargins(0, 0, 0, 0)

        # Panel 1: Track Distribution
        track_panel = self.create_track_distribution_panel()
        grid_layout.addWidget(track_panel, 0, 0)

        # Panel 2: Strand Distribution
        strand_panel = self.create_strand_distribution_panel()
        grid_layout.addWidget(strand_panel, 0, 1)

        # Panel 3: Grade Level Distribution
        grade_panel = self.create_grade_level_distribution_panel()
        grid_layout.addWidget(grade_panel, 1, 0)

        # Panel 4: Enrollment Status
        status_panel = self.create_enrollment_status_panel()
        grid_layout.addWidget(status_panel, 1, 1)

        self.content_layout.addLayout(grid_layout)
        self.content_layout.addSpacing(80)

        self.content_container.adjustSize()
        self.content_container.updateGeometry()

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
            font-size: 18px;
            font-weight: 700;
            color: #060C0B;
            border: none;
            background: transparent;
        """)
        subtitle = QLabel("Enrollment by academic track")
        subtitle.setStyleSheet("""
            font-size: 13px;
            color: #666;
            border: none;
            background: transparent;
        """)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(16)

        try:
            tracks = self.db.count_by_track()
            total = sum(tracks.values()) if tracks else 1

            for track, count in tracks.items():
                row_layout = QHBoxLayout()
                lbl = QLabel(track)
                lbl.setStyleSheet("""
                    font-size: 14px;
                    color: #333;
                    border: none;
                    background: transparent;
                """)

                bar_container = QFrame()
                bar_container.setFixedHeight(8)
                bar_container.setStyleSheet("background-color: #E5E7EB; border-radius: 4px;")

                bar = QFrame(bar_container)
                bar.setFixedHeight(8)
                bar.setStyleSheet("background-color: #059669; border-radius: 4px;")
                bar.setMaximumWidth(int((count / total) * 200))
                bar.setFixedWidth(int((count / total) * 200))

                bar_layout = QHBoxLayout(bar_container)
                bar_layout.setContentsMargins(0, 0, 0, 0)
                bar_layout.addWidget(bar)
                bar_layout.addStretch()

                val = QLabel(f"{count} ({int(count / total * 100)}%)")
                val.setStyleSheet("""
                    font-size: 14px;
                    color: #333;
                    border: none;
                    background: transparent;
                """)

                row_layout.addWidget(lbl)
                row_layout.addWidget(bar_container)
                row_layout.addWidget(val)
                row_layout.addStretch()
                layout.addLayout(row_layout)

        except Exception as e:
            err = QLabel("âš ï¸ No track data")
            err.setStyleSheet("""
                color: #EF4444;
                font-size: 13px;
                border: none;
                background: transparent;
            """)
            layout.addWidget(err)

        return panel

    def create_strand_distribution_panel(self):
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

        title = QLabel("Strand Distribution")
        title.setStyleSheet("""
            font-size: 18px;
            font-weight: 700;
            color: #060C0B;
            border: none;
            background: transparent;
        """)
        subtitle = QLabel("Enrollment by strand/course")
        subtitle.setStyleSheet("""
            font-size: 13px;
            color: #666;
            border: none;
            background: transparent;
        """)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(16)

        try:
            strands = self.db.get_all_strands()
            if not strands:
                layout.addWidget(QLabel("No strands defined"))
                return panel

            conn = self.db.get_connection()
            cursor = conn.cursor()
            strand_counts = {}
            for s in strands:
                cursor.execute('SELECT COUNT(*) FROM students WHERE strand = %s', (s,))
                cnt = cursor.fetchone()[0]
                strand_counts[s] = cnt
            conn.close()

            for strand, count in strand_counts.items():
                row_layout = QHBoxLayout()
                lbl = QLabel(strand)
                lbl.setStyleSheet("""
                    font-size: 14px;
                    color: #333;
                    border: none;
                    background: transparent;
                """)

                bar_container = QFrame()
                bar_container.setFixedHeight(8)
                bar_container.setStyleSheet("background-color: #E5E7EB; border-radius: 4px;")

                bar = QFrame(bar_container)
                bar.setFixedHeight(8)
                bar.setStyleSheet("background-color: #9333EA; border-radius: 4px;")
                bar.setMaximumWidth(
                    int((count / sum(strand_counts.values())) * 200) if sum(strand_counts.values()) else 0)
                bar.setFixedWidth(
                    int((count / sum(strand_counts.values())) * 200) if sum(strand_counts.values()) else 0)

                bar_layout = QHBoxLayout(bar_container)
                bar_layout.setContentsMargins(0, 0, 0, 0)
                bar_layout.addWidget(bar)
                bar_layout.addStretch()

                val = QLabel(str(count))
                val.setStyleSheet("""
                    font-size: 14px;
                    color: #333;
                    border: none;
                    background: transparent;
                """)

                row_layout.addWidget(lbl)
                row_layout.addWidget(bar_container)
                row_layout.addWidget(val)
                row_layout.addStretch()
                layout.addLayout(row_layout)

        except Exception as e:
            err = QLabel("âš ï¸ No strand data")
            err.setStyleSheet("""
                color: #EF4444;
                font-size: 13px;
                border: none;
                background: transparent;
            """)
            layout.addWidget(err)

        return panel

    def create_grade_level_distribution_panel(self):
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

        title = QLabel("Grade Level Distribution")
        title.setStyleSheet("""
            font-size: 18px;
            font-weight: 700;
            color: #060C0B;
            border: none;
            background: transparent;
        """)
        subtitle = QLabel("Students per grade level")
        subtitle.setStyleSheet("""
            font-size: 13px;
            color: #666;
            border: none;
            background: transparent;
        """)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(16)

        try:
            grades = self.db.count_by_grade()
            total = sum(grades.values()) if grades else 1

            for grade, count in grades.items():
                row_layout = QHBoxLayout()
                lbl = QLabel(grade)
                lbl.setStyleSheet("""
                    font-size: 14px;
                    color: #333;
                    border: none;
                    background: transparent;
                """)

                bar_container = QFrame()
                bar_container.setFixedHeight(8)
                bar_container.setStyleSheet("background-color: #E5E7EB; border-radius: 4px;")

                bar = QFrame(bar_container)
                bar.setFixedHeight(8)
                bar.setStyleSheet("background-color: #2563EB; border-radius: 4px;")
                bar.setMaximumWidth(int((count / total) * 200))
                bar.setFixedWidth(int((count / total) * 200))

                bar_layout = QHBoxLayout(bar_container)
                bar_layout.setContentsMargins(0, 0, 0, 0)
                bar_layout.addWidget(bar)
                bar_layout.addStretch()

                val = QLabel(str(count))
                val.setStyleSheet("""
                    font-size: 14px;
                    font-weight: 600;
                    color: #111827;
                    padding: 4px 12px;
                    background: #DBEAFE;
                    border-radius: 8px;
                    border: none;
                """)

                row_layout.addWidget(lbl)
                row_layout.addWidget(bar_container)
                row_layout.addWidget(val)
                row_layout.addStretch()
                layout.addLayout(row_layout)

        except Exception as e:
            err = QLabel("âš ï¸ No grade data")
            err.setStyleSheet("""
                color: #EF4444;
                font-size: 13px;
                border: none;
                background: transparent;
            """)
            layout.addWidget(err)

        return panel

    def create_enrollment_status_panel(self):
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
            border: none;
            background: transparent;
        """)
        subtitle = QLabel("Application status breakdown")
        subtitle.setStyleSheet("""
            font-size: 13px;
            color: #666;
            border: none;
            background: transparent;
        """)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(16)

        try:
            statuses = self.db.count_enrollment_status()

            for status, count in statuses.items():
                row_layout = QHBoxLayout()
                lbl = QLabel(status)
                lbl.setStyleSheet("""
                    font-size: 14px;
                    color: #333;
                    border: none;
                    background: transparent;
                """)

                color = "#10B981" if "enrolled" in status.lower() else \
                    "#F59E0B" if "pending" in status.lower() else \
                        "#EF4444"

                bar_container = QFrame()
                bar_container.setFixedHeight(8)
                bar_container.setStyleSheet("background-color: #E5E7EB; border-radius: 4px;")

                bar = QFrame(bar_container)
                bar.setFixedHeight(8)
                bar.setStyleSheet(f"background-color: {color}; border-radius: 4px;")
                total = sum(statuses.values()) if statuses else 1
                bar.setMaximumWidth(int((count / total) * 200))
                bar.setFixedWidth(int((count / total) * 200))

                bar_layout = QHBoxLayout(bar_container)
                bar_layout.setContentsMargins(0, 0, 0, 0)
                bar_layout.addWidget(bar)
                bar_layout.addStretch()

                val = QLabel(str(count))
                val.setStyleSheet(f"""
                    font-size: 14px;
                    font-weight: 600;
                    color: {color};
                    padding: 4px 12px;
                    background: {'#D1FAE5' if 'enrolled' in status.lower() else '#FEF3C7' if 'pending' in status.lower() else '#FEF2F2'};
                    border-radius: 8px;
                    border: none;
                """)

                row_layout.addWidget(lbl)
                row_layout.addWidget(bar_container)
                row_layout.addWidget(val)
                row_layout.addStretch()
                layout.addLayout(row_layout)

        except Exception as e:
            err = QLabel("âš ï¸ No status data")
            err.setStyleSheet("""
                color: #EF4444;
                font-size: 13px;
                border: none;
                background: transparent;
            """)
            layout.addWidget(err)

        return panel

    # ==================== DATA TAB ====================
    def show_data_content(self):
        self.clear_content()

        title = QLabel("Data Management")
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: 700;
            color: #060C0B;
            border: none;
            background: transparent;
        """)
        self.content_layout.addWidget(title)

        subtitle = QLabel("Manage enrollment data")
        subtitle.setStyleSheet("""
            font-size: 14px;
            color: #666;
            border: none;
            background: transparent;
        """)
        self.content_layout.addWidget(subtitle)

        self.content_layout.addSpacing(40)

        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 16px;
                padding: 32px;
            }
        """)
        panel_layout = QVBoxLayout(panel)
        panel_layout.setSpacing(24)
        panel_layout.setContentsMargins(0, 0, 0, 0)

        header_layout = QHBoxLayout()
        db_icon_path = 'assets/icons/database.png'
        db_icon = QLabel()
        if os.path.exists(db_icon_path):
            db_pixmap = QPixmap(db_icon_path).scaled(
                20, 20, Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            db_icon.setPixmap(db_pixmap)
        else:
            db_icon.setText("ðŸ“Š")

        header_title = QLabel("Database Information")
        header_title.setStyleSheet("""
            font-size: 18px;
            font-weight: 700;
            color: #060C0B;
            border: none;
            background: transparent;
            margin-left: 8px;
        """)
        header_layout.addWidget(db_icon)
        header_layout.addWidget(header_title)
        header_layout.addStretch()
        panel_layout.addLayout(header_layout)

        desc_label = QLabel("Manage enrollment data")
        desc_label.setStyleSheet("""
            font-size: 13px;
            color: #666;
            border: none;
            background: transparent;
            margin-top: 4px;
        """)
        panel_layout.addWidget(desc_label)
        panel_layout.addSpacing(20)

        metrics_layout = QHBoxLayout()
        metrics_layout.setSpacing(24)

        try:
            total_records = len(self.db.get_all_students())
        except Exception:
            total_records = 0

        total_card = QFrame()
        total_card.setStyleSheet("""
            QFrame {
                background-color: #F9FAFB;
                border-radius: 12px;
                padding: 20px;
            }
        """)
        total_layout = QVBoxLayout(total_card)
        total_layout.setSpacing(8)
        total_layout.setContentsMargins(0, 0, 0, 0)
        total_label = QLabel("Total Records")
        total_label.setStyleSheet("""
            font-size: 14px;
            color: #666;
            border: none;
            background: transparent;
        """)
        total_value = QLabel(str(total_records))
        total_value.setStyleSheet("""
            font-size: 24px;
            font-weight: 700;
            color: #111827;
            border: none;
            background: transparent;
        """)
        total_layout.addWidget(total_label)
        total_layout.addWidget(total_value)
        total_layout.addStretch()

        storage_card = QFrame()
        storage_card.setStyleSheet("""
            QFrame {
                background-color: #F9FAFB;
                border-radius: 12px;
                padding: 20px;
            }
        """)
        storage_layout = QVBoxLayout(storage_card)
        storage_layout.setSpacing(8)
        storage_layout.setContentsMargins(0, 0, 0, 0)
        storage_label = QLabel("Storage Type")
        storage_label.setStyleSheet("""
            font-size: 14px;
            color: #666;
            border: none;
            background: transparent;
        """)
        storage_value = QLabel("MySQL Database")
        storage_value.setStyleSheet("""
            font-size: 18px;
            font-weight: 600;
            color: #111827;
            border: none;
            background: transparent;
        """)
        storage_layout.addWidget(storage_label)
        storage_layout.addWidget(storage_value)
        storage_layout.addStretch()

        metrics_layout.addWidget(total_card)
        metrics_layout.addWidget(storage_card)

        panel_layout.addLayout(metrics_layout)
        panel_layout.addSpacing(30)

        divider = QFrame()
        divider.setFixedHeight(1)
        divider.setStyleSheet("background-color: #E5E7EB;")
        panel_layout.addWidget(divider)
        panel_layout.addSpacing(20)

        data_mgmt_title = QLabel("Data Management")
        data_mgmt_title.setStyleSheet("""
            font-size: 18px;
            font-weight: 700;
            color: #060C0B;
            border: none;
            background: transparent;
        """)
        panel_layout.addWidget(data_mgmt_title)
        data_mgmt_desc = QLabel("Export, backup, or clear enrollment data")
        data_mgmt_desc.setStyleSheet("""
            font-size: 13px;
            color: #666;
            border: none;
            background: transparent;
            margin-top: 4px;
        """)
        panel_layout.addWidget(data_mgmt_desc)
        panel_layout.addSpacing(16)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(16)

        export_btn = QPushButton("Export Data")
        export_btn.setFixedHeight(40)
        export_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #2563EB;
                border: 2px solid #3B82F6;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 600;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #DBEAFE;
            }
            QPushButton:pressed {
                background-color: #BFDBFE;
            }
        """)
        export_btn.clicked.connect(self.export_data)

        clear_btn = QPushButton("Clear All Data")
        clear_btn.setFixedHeight(40)
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #EF4444;
                border: 2px solid #F87171;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 600;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #FEF2F2;
            }
            QPushButton:pressed {
                background-color: #FEE2E2;
            }
        """)
        clear_btn.clicked.connect(self.clear_all_data)

        btn_layout.addWidget(export_btn)
        btn_layout.addWidget(clear_btn)
        btn_layout.addStretch()

        panel_layout.addLayout(btn_layout)

        self.content_layout.addWidget(panel)
        self.content_layout.addSpacing(80)

        self.content_container.adjustSize()
        self.content_container.updateGeometry()

    """
    UPDATED export_data() method for admin_screen.py
    Replace the existing export_data method with this version
    """

    def export_data(self):
        """Export all student data to PDF with professional formatting"""
        from datetime import datetime
        from PyQt6.QtWidgets import QFileDialog
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import letter, landscape
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.lib.enums import TA_CENTER, TA_LEFT

        try:
            # Get all students
            students = self.db.get_all_students()

            if not students:
                QMessageBox.warning(self, "Export Failed", "No data to export.")
                return

            # Generate filename with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            default_filename = f"enrollify_export_{timestamp}.pdf"

            # Open file dialog for user to choose save location
            filename, _ = QFileDialog.getSaveFileName(
                self,
                "Save Export As",
                default_filename,
                "PDF Files (*.pdf);;All Files (*)"
            )

            if not filename:  # User cancelled
                return

            # Ensure .pdf extension
            if not filename.lower().endswith('.pdf'):
                filename += '.pdf'

            # Create PDF document (landscape for more columns)
            doc = SimpleDocTemplate(
                filename,
                pagesize=landscape(letter),
                rightMargin=30,
                leftMargin=30,
                topMargin=50,
                bottomMargin=30
            )

            # Container for PDF elements
            elements = []

            # Styles
            styles = getSampleStyleSheet()

            # Custom title style
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#234940'),
                spaceAfter=12,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold'
            )

            # Custom subtitle style
            subtitle_style = ParagraphStyle(
                'CustomSubtitle',
                parent=styles['Normal'],
                fontSize=12,
                textColor=colors.HexColor('#6B7280'),
                spaceAfter=20,
                alignment=TA_CENTER,
                fontName='Helvetica'
            )

            # Add title
            title = Paragraph("Enrollify Student Database Export", title_style)
            elements.append(title)

            # Add export info
            export_info = Paragraph(
                f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}<br/>"
                f"Total Records: {len(students)}",
                subtitle_style
            )
            elements.append(export_info)
            elements.append(Spacer(1, 0.3 * inch))

            # Prepare table data
            # Headers (select most important columns to fit on page)
            headers = [
                'LRN', 'Name', 'Gender', 'Grade',
                'Track', 'Strand', 'Status', 'Email', 'Phone'
            ]

            # Format table data
            table_data = [headers]

            for student in students:
                full_name = f"{student.get('firstname', '')} {student.get('lastname', '')}".strip()

                row = [
                    student.get('lrn', 'N/A'),
                    full_name[:20],  # Truncate long names
                    student.get('gender', 'N/A'),
                    student.get('grade', 'N/A'),
                    student.get('track', 'N/A')[:15],  # Truncate
                    student.get('strand', 'N/A')[:15],  # Truncate
                    student.get('status', 'N/A'),
                    student.get('email', 'N/A')[:25],  # Truncate
                    student.get('phone', 'N/A')
                ]
                table_data.append(row)

            # Create table
            table = Table(table_data, repeatRows=1)

            # Style the table
            table.setStyle(TableStyle([
                # Header row
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#234940')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('TOPPADDING', (0, 0), (-1, 0), 12),

                # Data rows
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('TOPPADDING', (0, 1), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
                ('LEFTPADDING', (0, 1), (-1, -1), 4),
                ('RIGHTPADDING', (0, 1), (-1, -1), 4),

                # Grid
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E5E7EB')),

                # Alternating row colors
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F9FAFB')]),
            ]))

            elements.append(table)

            # Add footer
            elements.append(Spacer(1, 0.3 * inch))
            footer_style = ParagraphStyle(
                'Footer',
                parent=styles['Normal'],
                fontSize=8,
                textColor=colors.HexColor('#9CA3AF'),
                alignment=TA_CENTER,
                fontName='Helvetica-Oblique'
            )
            footer = Paragraph(
                "Enrollify - Student Enrollment Management System<br/>"
                "This document contains confidential student information",
                footer_style
            )
            elements.append(footer)

            # Build PDF
            doc.build(elements)

            # Show success message
            QMessageBox.information(
                self,
                "Export Successful",
                f"✅ Data exported successfully!\n\n"
                f"File saved to:\n{filename}\n\n"
                f"Total records: {len(students)}"
            )

            # Ask if user wants to open the file
            reply = QMessageBox.question(
                self,
                "Open File?",
                "Would you like to open the exported PDF?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                # Open PDF with default viewer
                import os
                import platform
                import subprocess

                if platform.system() == 'Windows':
                    os.startfile(filename)
                elif platform.system() == 'Darwin':  # macOS
                    subprocess.call(['open', filename])
                else:  # Linux
                    subprocess.call(['xdg-open', filename])

        except ImportError as e:
            QMessageBox.critical(
                self,
                "Missing Library",
                "PDF export requires the 'reportlab' library.\n\n"
                "Install it with:\n"
                "pip install reportlab\n\n"
                f"Error: {str(e)}"
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Export Failed",
                f"An error occurred while exporting:\n\n{str(e)}"
            )
            import traceback
            traceback.print_exc()

    def clear_all_data(self):
        """Clear all student and payment data"""
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            "Are you sure you want to clear ALL enrollment data? This cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            try:
                conn = self.db.get_connection()
                cursor = conn.cursor()
                cursor.execute('DELETE FROM students')
                cursor.execute('DELETE FROM payments')
                conn.commit()
                conn.close()
                self.db.log_action(None, 'CLEAR_DATA', "All enrollment data cleared by admin")
                QMessageBox.information(self, "Success", "All data has been cleared.")
                self.switch_tab("data")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    # ==================== SYSTEM TAB ====================
    def show_system_content(self):
        self.clear_content()

        title = QLabel("System Settings")
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: 700;
            color: #060C0B;
            border: none;
            background: transparent;
        """)
        self.content_layout.addWidget(title)

        subtitle = QLabel("Application settings and information")
        subtitle.setStyleSheet("""
            font-size: 14px;
            color: #666;
            border: none;
            background: transparent;
        """)
        self.content_layout.addWidget(subtitle)

        self.content_layout.addSpacing(40)

        sys_panel = QFrame()
        sys_panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 16px;
                padding: 32px;
            }
        """)
        sys_layout = QVBoxLayout(sys_panel)
        sys_layout.setSpacing(24)

        header_layout = QHBoxLayout()
        sys_icon_path = 'assets/icons/settings.png'
        sys_icon = QLabel()
        if os.path.exists(sys_icon_path):
            sys_pixmap = QPixmap(sys_icon_path).scaled(
                20, 20, Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            sys_icon.setPixmap(sys_pixmap)
        else:
            sys_icon.setText("âš™ï¸")

        header_title = QLabel("System Information")
        header_title.setStyleSheet("font-size: 18px; font-weight: 700; color: #060C0B; margin-left: 8px;")
        header_layout.addWidget(sys_icon)
        header_layout.addWidget(header_title)
        header_layout.addStretch()
        sys_layout.addLayout(header_layout)

        desc_label = QLabel("Application settings and information")
        desc_label.setStyleSheet("font-size: 13px; color: #666; margin-top: 4px;")
        sys_layout.addWidget(desc_label)
        sys_layout.addSpacing(20)

        info_layout = QVBoxLayout()
        info_layout.setSpacing(16)

        self.add_info_row(info_layout, "Application Name", "Enrollify")
        self.add_info_row(info_layout, "Version", "1.0.0")
        self.add_info_row(info_layout, "Database", "MySQL")

        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM users')
            user_count = cursor.fetchone()[0]
            cursor.execute('''
                           SELECT timestamp
                           FROM audit_log
                           WHERE action = 'LOGIN'
                           ORDER BY timestamp DESC
                               LIMIT 1
                           ''')
            last_login_row = cursor.fetchone()
            last_login = last_login_row[0] if last_login_row else "Never"
            conn.close()
            user_info = f"{user_count} (Student, Staff, Admin)"
        except Exception:
            user_info = "Unknown"
        self.add_info_row(info_layout, "Active Users", user_info)

        try:
            tracks = self.db.count_by_track()
            track_count = len(tracks)
        except Exception:
            track_count = 0
        self.add_info_row(info_layout, "Supported Tracks", str(track_count))

        sys_layout.addLayout(info_layout)
        sys_layout.addSpacing(24)

        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(16)

        edit_tracks_btn = QPushButton("Edit Tracks")
        edit_tracks_btn.setFixedHeight(40)
        edit_tracks_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #2563EB;
                border: 2px solid #3B82F6;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 600;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #DBEAFE;
            }
        """)
        edit_tracks_btn.clicked.connect(self.open_edit_tracks_dialog)

        update_btn = QPushButton("Check for Updates")
        update_btn.setFixedHeight(40)
        update_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #7C2D12;
                border: 2px solid #F59E0B;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 600;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #FEF3C7;
            }
        """)
        update_btn.clicked.connect(self.check_for_updates)

        actions_layout.addWidget(edit_tracks_btn)
        actions_layout.addWidget(update_btn)
        actions_layout.addStretch()

        sys_layout.addLayout(actions_layout)

        self.content_layout.addWidget(sys_panel)
        self.content_layout.addSpacing(30)

        self.refresh_tracks_panel()

        self.content_container.adjustSize()
        self.content_container.updateGeometry()

    def add_info_row(self, parent_layout, key, value):
        row = QHBoxLayout()
        key_label = QLabel(key)
        key_label.setStyleSheet("font-size: 14px; color: #666;")
        val_label = QLabel(value)
        val_label.setStyleSheet("font-size: 16px; font-weight: 600; color: #111827;")
        val_label.setWordWrap(True)
        row.addWidget(key_label)
        row.addStretch()
        row.addWidget(val_label)
        parent_layout.addLayout(row)

    def refresh_tracks_panel(self):
        tracks_panel = QFrame()
        tracks_panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 16px;
                padding: 32px;
            }
        """)
        tracks_layout = QVBoxLayout(tracks_panel)
        tracks_layout.setSpacing(24)

        header = QLabel("Available Tracks")
        header.setStyleSheet("font-size: 18px; font-weight: 700; color: #060C0B;")
        desc = QLabel("Supported SHS academic tracks")
        desc.setStyleSheet("font-size: 13px; color: #666; margin-top: 4px;")
        tracks_layout.addWidget(header)
        tracks_layout.addWidget(desc)
        tracks_layout.addSpacing(20)

        try:
            tracks = self.db.get_all_tracks()
        except Exception:
            tracks = []

        grid = QGridLayout()
        grid.setSpacing(16)
        for i, track in enumerate(tracks):
            btn = QPushButton(track)
            btn.setFixedHeight(40)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #F0fdfa;
                    color: #065F46;
                    border: 1px solid #6EE7B7;
                    border-radius: 8px;
                    font-size: 14px;
                    font-weight: 600;
                    padding: 0 16px;
                }
                QPushButton:hover {
                    background-color: #CCFBF1;
                }
            """)
            grid.addWidget(btn, i // 2, i % 2)

        tracks_layout.addLayout(grid)
        tracks_layout.addStretch()

        self.content_layout.addWidget(tracks_panel)
        self.content_layout.addSpacing(80)

    def open_edit_tracks_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Manage Tracks")
        dialog.setModal(True)
        dialog.resize(450, 500)
        layout = QVBoxLayout(dialog)

        instr = QLabel("Add or remove academic tracks. Tracks in use by students cannot be removed.")
        instr.setStyleSheet("font-size: 13px; color: #666; margin-bottom: 10px;")
        instr.setWordWrap(True)
        layout.addWidget(instr)

        add_layout = QHBoxLayout()
        self.track_input = QLineEdit()
        self.track_input.setPlaceholderText("Enter new track name")
        add_btn = QPushButton("Add Track")
        add_btn.clicked.connect(self.add_track_from_dialog)
        add_layout.addWidget(self.track_input)
        add_layout.addWidget(add_btn)
        layout.addLayout(add_layout)

        self.track_list = QListWidget()
        layout.addWidget(self.track_list)

        remove_btn = QPushButton("Remove Selected Track")
        remove_btn.clicked.connect(self.remove_track_from_dialog)
        layout.addWidget(remove_btn)

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn)

        self.load_tracks_into_list()
        dialog.exec()
        self.refresh_tracks_panel()

    def load_tracks_into_list(self):
        self.track_list.clear()
        try:
            tracks = self.db.get_all_tracks()
            self.track_list.addItems(tracks)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load tracks: {str(e)}")

    def add_track_from_dialog(self):
        name = self.track_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Invalid Input", "Track name cannot be empty.")
            return
        try:
            self.db.add_track(name)
            self.track_input.clear()
            self.load_tracks_into_list()
            QMessageBox.information(self, "Success", f"Track '{name}' added successfully!")
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add track: {str(e)}")

    def remove_track_from_dialog(self):
        current_item = self.track_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "No Selection", "Please select a track to remove.")
            return
        track_name = current_item.text()
        reply = QMessageBox.question(
            self, "Confirm Deletion",
            f"Are you sure you want to remove the track '{track_name}'? "
            "Note: Tracks currently assigned to students cannot be deleted.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.db.remove_track(track_name)
                self.load_tracks_into_list()
                QMessageBox.information(self, "Success", f"Track '{track_name}' removed!")
            except ValueError as e:
                QMessageBox.warning(self, "Cannot Delete", str(e))
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to remove track: {str(e)}")

    def check_for_updates(self):
        QMessageBox.information(self, "Check for Updates", "No updates available.")

    def show_staff_content(self):
        """Staff Management Tab - Assign students to staff"""
        self.clear_content()

        title = QLabel("Staff Management")
        title.setStyleSheet("font-size: 28px; font-weight: 700; color: #060C0B;")
        self.content_layout.addWidget(title)

        subtitle = QLabel("Manage staff users and student assignments")
        subtitle.setStyleSheet("font-size: 14px; color: #666;")
        self.content_layout.addWidget(subtitle)

        self.content_layout.addSpacing(40)

        # Two column layout
        columns = QHBoxLayout()
        columns.setSpacing(30)

        # LEFT: Staff List
        left_panel = self.create_staff_list_panel()
        columns.addWidget(left_panel, 1)

        # RIGHT: Unassigned Students
        right_panel = self.create_unassigned_students_panel()
        columns.addWidget(right_panel, 1)

        self.content_layout.addLayout(columns)
        self.content_layout.addSpacing(80)

    def create_staff_list_panel(self):
        """Panel showing all staff and their student counts"""
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

        title = QLabel("Staff Members")
        title.setStyleSheet("font-size: 18px; font-weight: 700; color: #060C0B;")
        layout.addWidget(title)

        try:
            staff_users = self.db.get_all_staff_users()

            for staff in staff_users:
                staff_id = staff['id']
                student_count = self.db.get_staff_student_count(staff_id)

                row = QHBoxLayout()

                # Staff info
                info_layout = QVBoxLayout()
                info_layout.setSpacing(4)

                name = QLabel(staff['full_name'])
                name.setStyleSheet("font-size: 14px; font-weight: 600; color: #111827;")

                email = QLabel(staff['email'])
                email.setStyleSheet("font-size: 13px; color: #6B7280;")

                info_layout.addWidget(name)
                info_layout.addWidget(email)

                # Student count badge
                count_label = QLabel(f"{student_count} students")
                count_label.setStyleSheet("""
                    font-size: 13px;
                    color: #059669;
                    background: #ECFDF5;
                    padding: 4px 12px;
                    border-radius: 8px;
                    font-weight: 600;
                """)

                # View button
                view_btn = QPushButton("View Students")
                view_btn.setFixedHeight(35)
                view_btn.setStyleSheet("""
                    QPushButton {
                        background: #F9FAFB;
                        border: 1px solid #E5E7EB;
                        border-radius: 8px;
                        padding: 0 16px;
                        font-size: 13px;
                        font-weight: 600;
                        color: #111827;
                    }
                    QPushButton:hover {
                        background: #E5E7EB;
                    }
                """)
                view_btn.clicked.connect(lambda _, s=staff: self.view_staff_students(s))

                row.addLayout(info_layout)
                row.addStretch()
                row.addWidget(count_label)
                row.addWidget(view_btn)

                layout.addLayout(row)

                # Divider
                divider = QFrame()
                divider.setFrameShape(QFrame.Shape.HLine)
                divider.setStyleSheet("background-color: #E5E7EB; max-height: 1px;")
                layout.addWidget(divider)

        except Exception as e:
            print(f"Error loading staff: {e}")
            error_label = QLabel("Failed to load staff members")
            error_label.setStyleSheet("color: #EF4444; font-size: 13px;")
            layout.addWidget(error_label)

        layout.addStretch()
        return panel

    def create_unassigned_students_panel(self):
        """Panel showing students not assigned to any staff"""
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

        title = QLabel("Unassigned Students")
        title.setStyleSheet("font-size: 18px; font-weight: 700; color: #060C0B;")
        layout.addWidget(title)

        subtitle = QLabel("Students not yet assigned to any staff member")
        subtitle.setStyleSheet("font-size: 13px; color: #6B7280;")
        layout.addWidget(subtitle)

        try:
            unassigned = self.db.get_unassigned_students()

            if not unassigned:
                empty_label = QLabel("✅ All students have been assigned!")
                empty_label.setStyleSheet("font-size: 14px; color: #059669; padding: 20px;")
                layout.addWidget(empty_label)
            else:
                for student in unassigned[:10]:  # Show first 10
                    row = QHBoxLayout()

                    # Student info
                    info_layout = QVBoxLayout()
                    info_layout.setSpacing(4)

                    name = QLabel(f"{student['firstname']} {student['lastname']}")
                    name.setStyleSheet("font-size: 14px; font-weight: 600; color: #111827;")

                    details = QLabel(f"{student['grade']} - {student['track']}")
                    details.setStyleSheet("font-size: 13px; color: #6B7280;")

                    info_layout.addWidget(name)
                    info_layout.addWidget(details)

                    # Assign button
                    assign_btn = QPushButton("Assign")
                    assign_btn.setFixedHeight(35)
                    assign_btn.setStyleSheet("""
                        QPushButton {
                            background: #059669;
                            border: none;
                            border-radius: 8px;
                            padding: 0 16px;
                            font-size: 13px;
                            font-weight: 600;
                            color: white;
                        }
                        QPushButton:hover {
                            background: #047857;
                        }
                    """)
                    assign_btn.clicked.connect(lambda _, s=student: self.assign_student_dialog(s))

                    row.addLayout(info_layout)
                    row.addStretch()
                    row.addWidget(assign_btn)

                    layout.addLayout(row)

                    # Divider
                    divider = QFrame()
                    divider.setFrameShape(QFrame.Shape.HLine)
                    divider.setStyleSheet("background-color: #E5E7EB; max-height: 1px;")
                    layout.addWidget(divider)

        except Exception as e:
            print(f"Error loading unassigned: {e}")
            error_label = QLabel("Failed to load students")
            error_label.setStyleSheet("color: #EF4444; font-size: 13px;")
            layout.addWidget(error_label)

        layout.addStretch()
        return panel

    def assign_student_dialog(self, student):
        """Dialog to assign student to a staff member"""
        from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton

        dialog = QDialog(self)
        dialog.setWindowTitle("Assign Student to Staff")
        dialog.setMinimumWidth(400)

        layout = QVBoxLayout(dialog)
        layout.setSpacing(20)

        # Student info
        student_label = QLabel(f"Student: {student['firstname']} {student['lastname']}")
        student_label.setStyleSheet("font-size: 16px; font-weight: 600;")
        layout.addWidget(student_label)

        grade_label = QLabel(f"{student['grade']} - {student['track']}")
        grade_label.setStyleSheet("font-size: 14px; color: #6B7280;")
        layout.addWidget(grade_label)

        # Staff dropdown
        layout.addWidget(QLabel("Select Staff Member:"))

        staff_combo = QComboBox()
        staff_combo.setFixedHeight(40)

        try:
            staff_users = self.db.get_all_staff_users()
            for staff in staff_users:
                staff_combo.addItem(
                    f"{staff['full_name']} ({staff['email']})",
                    staff  # Store staff data
                )
        except:
            pass

        layout.addWidget(staff_combo)

        # Buttons
        btn_layout = QHBoxLayout()

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(dialog.reject)

        assign_btn = QPushButton("Assign")
        assign_btn.setStyleSheet("""
            QPushButton {
                background: #059669;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: #047857;
            }
        """)

        def do_assign():
            selected_staff = staff_combo.currentData()
            if selected_staff:
                success = self.db.assign_student_to_staff(
                    student['lrn'],
                    selected_staff['id'],
                    selected_staff['email']
                )
                if success:
                    QMessageBox.information(
                        self,
                        "Success",
                        f"✅ {student['firstname']} {student['lastname']} assigned to {selected_staff['full_name']}"
                    )
                    dialog.accept()
                    self.show_staff_content()  # Refresh
                else:
                    QMessageBox.warning(self, "Error", "Failed to assign student")

        assign_btn.clicked.connect(do_assign)

        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(assign_btn)
        layout.addLayout(btn_layout)

        dialog.exec()

    def view_staff_students(self, staff):
        """View all students assigned to a staff member"""
        from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget

        dialog = QDialog(self)
        dialog.setWindowTitle(f"Students - {staff['full_name']}")
        dialog.setMinimumSize(600, 500)

        layout = QVBoxLayout(dialog)
        layout.setSpacing(20)

        # Header
        header = QLabel(f"{staff['full_name']}'s Students")
        header.setStyleSheet("font-size: 20px; font-weight: 700;")
        layout.addWidget(header)

        email = QLabel(staff['email'])
        email.setStyleSheet("font-size: 14px; color: #6B7280;")
        layout.addWidget(email)

        # Student list
        student_list = QListWidget()

        try:
            students = self.db.get_students_by_staff(staff['id'])

            for s in students:
                item_text = f"{s['firstname']} {s['lastname']} - {s['grade']} ({s['track']})"
                student_list.addItem(item_text)
        except Exception as e:
            print(f"Error: {e}")

        layout.addWidget(student_list)

        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn)

        dialog.exec()