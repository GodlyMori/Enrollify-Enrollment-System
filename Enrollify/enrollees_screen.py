from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QFrame, QTableWidget, QTableWidgetItem,
                             QHeaderView, QLineEdit, QComboBox, QSizePolicy, QMessageBox)
from PyQt6.QtCore import pyqtSignal
from components import HeaderWidget, NavTabsWidget
from database_manager_mysql import get_database


class EnrolleesScreen(QWidget):
    logout_signal = pyqtSignal()
    show_overview_signal = pyqtSignal()
    show_enrollees_signal = pyqtSignal()
    show_reports_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #F5F7FA;")
        self.db = get_database()
        self.all_students = []
        self.filtered_students = []
        self.setup_ui()

    def set_current_user(self, user):
        """
        Set the currently logged-in user
        ADD THIS METHOD to your existing class
        """
        self.current_user = user
        # Optionally refresh data with user context
        try:
            if hasattr(self, 'load_students'):
                self.load_students()
        except:
            pass

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        self.header = HeaderWidget(subtitle="Staff Portal - Student Management")
        self.header.logout_signal.connect(self.logout_signal.emit)
        layout.addWidget(self.header)

        # Navigation tabs
        self.nav_tabs = NavTabsWidget(active="enrollees")
        self.nav_tabs.show_overview_signal.connect(self.show_overview_signal.emit)
        self.nav_tabs.show_enrollees_signal.connect(self.show_enrollees_signal.emit)
        self.nav_tabs.show_reports_signal.connect(self.show_reports_signal.emit)
        layout.addWidget(self.nav_tabs)

        # Content
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(70, 60, 70, 60)
        content_layout.setSpacing(30)

        # Card
        card = QFrame()
        card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        card.setStyleSheet("""
            QFrame { 
                background-color: white; 
                border-radius: 15px; 
                border: none;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(50, 50, 50, 50)
        card_layout.setSpacing(30)

        # Title
        title = QLabel("Enrolled Students")
        title.setStyleSheet("color: #060C0B; font-size: 26px; font-weight: 700;")
        card_layout.addWidget(title)

        subtitle = QLabel("Manage and view all enrolled students")
        subtitle.setStyleSheet("color: #999; font-size: 14px; margin-bottom: 15px;")
        card_layout.addWidget(subtitle)

        # Search and filters
        filters_widget = QWidget()
        filters_layout = QHBoxLayout(filters_widget)
        filters_layout.setContentsMargins(0, 0, 0, 0)
        filters_layout.setSpacing(25)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Search by name or LRN...")
        self.search_input.setMinimumHeight(50)
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: #F8F9FA;
                border: none;
                border-bottom: 2px solid #E9ECEF;
                border-radius: 0px;
                padding: 12px 0px;
                padding-left: 15px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-bottom: 2px solid #5DBAA3;
                background-color: #FAFBFC;
            }
            QLineEdit::placeholder {
                color: #D1D5DB;
            }
        """)
        self.search_input.textChanged.connect(self.apply_filters)
        filters_layout.addWidget(self.search_input, 3)

        # Grade filter
        self.grade_filter = QComboBox()
        self.grade_filter.addItems(["All Grades", "Grade 11", "Grade 12"])
        self.grade_filter.setMinimumHeight(50)
        self.grade_filter.setStyleSheet("""
            QComboBox {
                background-color: #F8F9FA;
                border: none;
                border-bottom: 2px solid #E9ECEF;
                border-radius: 0px;
                padding: 12px 0px;
                padding-left: 15px;
                font-size: 14px;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 15px;
            }
            QComboBox:focus {
                border-bottom: 2px solid #5DBAA3;
                background-color: #FAFBFC;
            }
        """)
        self.grade_filter.currentTextChanged.connect(self.apply_filters)
        filters_layout.addWidget(self.grade_filter, 1)

        # Track filter
        self.track_filter = QComboBox()
        self.track_filter.addItems(["All Tracks", "Academic Track", "TVL Track", "Sports Track", "Arts and Design Track"])
        self.track_filter.setMinimumHeight(50)
        self.track_filter.setStyleSheet("""
            QComboBox {
                background-color: #F8F9FA;
                border: none;
                border-bottom: 2px solid #E9ECEF;
                border-radius: 0px;
                padding: 12px 0px;
                padding-left: 15px;
                font-size: 14px;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 15px;
            }
            QComboBox:focus {
                border-bottom: 2px solid #5DBAA3;
                background-color: #FAFBFC;
            }
        """)
        self.track_filter.currentTextChanged.connect(self.apply_filters)
        filters_layout.addWidget(self.track_filter, 1)

        # Status filter
        self.status_filter = QComboBox()
        self.status_filter.addItems(["All Status", "Enrolled", "Pending"])
        self.status_filter.setMinimumHeight(50)
        self.status_filter.setStyleSheet("""
            QComboBox {
                background-color: #F8F9FA;
                border: none;
                border-bottom: 2px solid #E9ECEF;
                border-radius: 0px;
                padding: 12px 0px;
                padding-left: 15px;
                font-size: 14px;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 15px;
            }
            QComboBox:focus {
                border-bottom: 2px solid #5DBAA3;
                background-color: #FAFBFC;
            }
        """)
        self.status_filter.currentTextChanged.connect(self.apply_filters)
        filters_layout.addWidget(self.status_filter, 1)

        card_layout.addWidget(filters_widget)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["LRN", "Name", "Grade", "Track", "Status", "Contact", "Actions"])
        self.table.verticalHeader().setDefaultSectionSize(75)

        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: none;
                gridline-color: #F0F0F0;
                font-size: 14px;
                selection-background-color: #E8F4F2;
            }
            QTableWidget::item {
                padding: 18px 15px;
                border-bottom: 1px solid #F0F0F0;
            }
            QHeaderView::section {
                background-color: #FAFAFA;
                color: #666;
                font-weight: 700;
                font-size: 14px;
                border: none;
                border-bottom: 2px solid #E0E0E0;
                padding: 18px 15px;
                text-align: left;
            }
        """)

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        card_layout.addWidget(self.table)

        # Load data from database
        self.load_students()

        content_layout.addWidget(card)
        content_layout.addStretch()

        layout.addWidget(content)

    def load_students(self):
        """Load all students from database"""
        try:
            self.all_students = self.db.get_all_students()
            self.filtered_students = self.all_students.copy()
            self.populate_table()
        except Exception as e:
            print(f"Error loading students: {e}")
            QMessageBox.warning(self, "Database Error", f"Failed to load students: {str(e)}")

    def apply_filters(self):
        """Apply search and filter criteria"""
        search_text = self.search_input.text().lower()
        grade = self.grade_filter.currentText()
        track = self.track_filter.currentText()
        status = self.status_filter.currentText()

        self.filtered_students = []

        for student in self.all_students:
            # Search filter
            if search_text:
                lrn = student.get('lrn', '').lower()
                name = f"{student.get('firstname', '')} {student.get('lastname', '')}".lower()
                if search_text not in lrn and search_text not in name:
                    continue

            # Grade filter
            if grade != "All Grades" and student.get('grade_level', '') != grade:
                continue

            # Track filter
            if track != "All Tracks" and student.get('track', '') != track:
                continue

            # Status filter
            if status != "All Status" and student.get('enrollment_status', '') != status:
                continue

            self.filtered_students.append(student)

        self.populate_table()

    def populate_table(self):
        """Populate table with filtered students"""
        self.table.setRowCount(0)

        for row, student in enumerate(self.filtered_students):
            self.table.insertRow(row)

            # LRN
            self.table.setItem(row, 0, QTableWidgetItem(student.get('lrn', '')))

            # Name
            name = f"{student.get('lastname', '')}, {student.get('firstname', '')} {student.get('middlename', '')}"
            self.table.setItem(row, 1, QTableWidgetItem(name.strip()))

            # Grade
            self.table.setItem(row, 2, QTableWidgetItem(student.get('grade_level', '')))

            # Track
            self.table.setItem(row, 3, QTableWidgetItem(student.get('track', '')))

            # Status - dropdown
            status_combo = self.create_status_combo(student.get('enrollment_status', 'Pending'), student.get('lrn', ''))
            self.table.setCellWidget(row, 4, status_combo)

            # Contact
            self.table.setItem(row, 5, QTableWidgetItem(student.get('email', '')))

            # Actions
            actions_widget = self.create_actions_widget(student)
            self.table.setCellWidget(row, 6, actions_widget)

    def create_status_combo(self, current_status, lrn):
        """Create status dropdown with styling"""
        status_combo = QComboBox()
        status_combo.addItems(["Enrolled", "Pending"])
        status_combo.setCurrentText(current_status)
        status_combo.setMinimumHeight(50)

        def apply_status_color(combo, status_text):
            if status_text == "Enrolled":
                combo.setStyleSheet("""
                    QComboBox {
                        background-color: #ECFDF5;
                        border: none;
                        border-bottom: 2px solid #10B981;
                        border-radius: 0px;
                        padding: 8px 12px;
                        font-size: 13px;
                        font-weight: 600;
                        color: #065F46;
                    }
                    QComboBox:focus {
                        border-bottom: 2px solid #059669;
                    }
                    QComboBox::drop-down {
                        border: none;
                    }
                """)
            elif status_text == "Pending":
                combo.setStyleSheet("""
                    QComboBox {
                        background-color: #FFFBEB;
                        border: none;
                        border-bottom: 2px solid #F59E0B;
                        border-radius: 0px;
                        padding: 8px 12px;
                        font-size: 13px;
                        font-weight: 600;
                        color: #92400E;
                    }
                    QComboBox:focus {
                        border-bottom: 2px solid #D97706;
                    }
                    QComboBox::drop-down {
                        border: none;
                    }
                """)

        apply_status_color(status_combo, current_status)
        status_combo.currentTextChanged.connect(lambda text, c=status_combo, l=lrn: self.update_status(l, text, c))
        status_combo.currentTextChanged.connect(lambda text, combo=status_combo: apply_status_color(combo, text))

        return status_combo

    def create_actions_widget(self, student):
        """Create actions buttons widget"""
        actions_widget = QWidget()
        actions_layout = QHBoxLayout(actions_widget)
        actions_layout.setContentsMargins(10, 0, 10, 0)
        actions_layout.setSpacing(12)

        # View button
        view_btn = QPushButton("👁")
        view_btn.setFixedSize(45, 45)
        view_btn.setToolTip("View Details")
        view_btn.setStyleSheet("""
            QPushButton {
                background-color: #F8F9FA;
                border: 2px solid #E9ECEF;
                border-radius: 8px;
                font-size: 18px;
                padding: 5px;
                color: #060C0B;
            }
            QPushButton:hover {
                background-color: #E9ECEF;
                border: 2px solid #5DBAA3;
            }
            QPushButton:pressed {
                background-color: #D9E0E7;
            }
        """)
        view_btn.clicked.connect(lambda: self.view_student(student))
        actions_layout.addWidget(view_btn)

        # Edit button
        edit_btn = QPushButton("✏")
        edit_btn.setFixedSize(45, 45)
        edit_btn.setToolTip("Edit")
        edit_btn.setStyleSheet("""
            QPushButton {
                background-color: #F8F9FA;
                border: 2px solid #E9ECEF;
                border-radius: 8px;
                font-size: 18px;
                padding: 5px;
                color: #060C0B;
            }
            QPushButton:hover {
                background-color: #E9ECEF;
                border: 2px solid #5DBAA3;
            }
            QPushButton:pressed {
                background-color: #D9E0E7;
            }
        """)
        edit_btn.clicked.connect(lambda: self.edit_student(student))
        actions_layout.addWidget(edit_btn)

        # Delete button
        delete_btn = QPushButton("🗑")
        delete_btn.setFixedSize(45, 45)
        delete_btn.setToolTip("Delete")
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #F8F9FA;
                border: 2px solid #E9ECEF;
                border-radius: 8px;
                font-size: 18px;
                padding: 5px;
                color: #060C0B;
            }
            QPushButton:hover {
                background-color: #FEE2E2;
                border: 2px solid #EF4444;
            }
            QPushButton:pressed {
                background-color: #FECACA;
            }
        """)
        delete_btn.clicked.connect(lambda: self.delete_student(student))
        actions_layout.addWidget(delete_btn)

        actions_layout.addStretch()
        return actions_widget

    def update_status(self, lrn, new_status, combo):
        """Update student enrollment status"""
        try:
            self.db.update_enrollment_status(lrn, new_status)
            QMessageBox.information(self, "Success", f"Status updated to {new_status}")
            self.load_students()
        except Exception as e:
            print(f"Error updating status: {e}")
            QMessageBox.warning(self, "Error", f"Failed to update status: {str(e)}")

    def view_student(self, student):
        """View student details"""
        details = f"""
Student Details:

LRN: {student.get('lrn', '')}
Name: {student.get('firstname', '')} {student.get('middlename', '')} {student.get('lastname', '')}
Gender: {student.get('gender', '')}
Birthdate: {student.get('birthdate', '')}
Email: {student.get('email', '')}
Phone: {student.get('phone', '')}
Address: {student.get('address', '')}

Academic Information:
Grade Level: {student.get('grade_level', '')}
Track: {student.get('track', '')}
Strand: {student.get('strand', '')}

Guardian Information:
Guardian Name: {student.get('guardian_name', '')}
Guardian Contact: {student.get('guardian_contact', '')}

Enrollment Status: {student.get('enrollment_status', '')}
Created: {student.get('created_at', '')}
        """
        QMessageBox.information(self, "Student Details", details)

    def edit_student(self, student):
        """Edit student (placeholder)"""
        QMessageBox.information(self, "Edit Student", f"Edit functionality for {student.get('firstname', '')} {student.get('lastname', '')} will be implemented here.")

    def delete_student(self, student):
        """Delete student"""
        reply = QMessageBox.question(
            self, 'Confirm Delete',
            f"Are you sure you want to delete {student.get('firstname', '')} {student.get('lastname', '')}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.db.delete_student(student.get('lrn', ''))
                QMessageBox.information(self, "Success", "Student deleted successfully")
                self.load_students()
            except Exception as e:
                print(f"Error deleting student: {e}")
                QMessageBox.warning(self, "Error", f"Failed to delete student: {str(e)}")