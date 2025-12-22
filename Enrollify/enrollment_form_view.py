"""
ENROLLMENT FORM VIEW - MVC Pattern
Pure UI layer - NO business logic or database calls
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame,
    QScrollArea, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap
from form_components.FormInput import FormInput
from form_components.FormCombo import FormCombo
from form_components.FormDate import FormDate
from form_components.SectionHeader import SectionHeader
from form_components.SubmitButton import SubmitButton
import os


class EnrollmentFormView(QWidget):
    """
    ✅ VIEW LAYER - Pure UI, no business logic
    Emits signals for controller to handle
    """

    # Signals for controller to handle
    logout_clicked = pyqtSignal()
    submit_clicked = pyqtSignal(dict)  # Emits form data
    track_changed = pyqtSignal(str)    # Emits track name

    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #F8FAFA;")
        self.available_tracks = []  # Will be set by controller
        self.build_ui()

    def build_ui(self):
        """Build the enrollment form UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Header
        header = self.build_header()
        main_layout.addWidget(header)

        # Scroll Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(60, 40, 60, 40)
        container_layout.setSpacing(30)

        container_layout.addWidget(self.build_page_title())
        container_layout.addWidget(self.build_form_card())
        container_layout.addStretch()

        scroll.setWidget(container)
        main_layout.addWidget(scroll)

    def build_header(self):
        """Build header with logout button"""
        header = QWidget()
        header.setFixedHeight(100)
        header.setStyleSheet("background-color: white; border-bottom: none;")

        layout = QHBoxLayout(header)
        layout.setContentsMargins(60, 20, 60, 20)

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
        titles = QVBoxLayout()
        title = QLabel("Enrollify")
        title.setStyleSheet("font-size: 28px; color: #234940; font-weight: 700;")
        subtitle = QLabel("Student Enrollment Portal")
        subtitle.setStyleSheet("font-size: 15px; color: #6B7280; font-weight: 500;")
        titles.addWidget(title)
        titles.addWidget(subtitle)

        # Logout button
        logout_btn = QPushButton("↪ Logout")
        logout_btn.setFixedSize(110, 40)
        logout_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #2D9B84;
                border: 2px solid #2D9B84;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover { background-color: #F0FAF8; }
        """)
        logout_btn.clicked.connect(self.logout_clicked.emit)

        layout.addWidget(logo)
        layout.addLayout(titles)
        layout.addStretch()
        layout.addWidget(logout_btn)

        return header

    def build_page_title(self):
        """Build page title banner"""
        box = QFrame()
        box.setStyleSheet("background-color: #E8F5F3; border-radius: 12px;")

        layout = QVBoxLayout(box)
        layout.setContentsMargins(30, 25, 30, 25)

        title = QLabel("Student Enrollment Form")
        title.setStyleSheet("font-size: 28px; font-weight: 700; color: #234940;")

        subtitle = QLabel("Fill out all required fields to complete your application")
        subtitle.setStyleSheet("font-size: 15px; font-weight: 500; color: #6B7280;")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        return box

    def build_form_card(self):
        """Build the main form card"""
        self.form = QFrame()
        self.form.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 16px;
                border: none;
            }
        """)
        layout = QVBoxLayout(self.form)
        layout.setContentsMargins(70, 60, 70, 60)
        layout.setSpacing(42)

        # PERSONAL INFO
        layout.addWidget(SectionHeader("Personal Information"))
        self.lrn = FormInput("Learner Reference Number (LRN) *", "Enter 12-digit LRN")
        self.gender = FormCombo("Gender *", ["Select gender", "Male", "Female"])
        self.firstname = FormInput("First Name *", "")
        self.middlename = FormInput("Middle Name", "")
        self.lastname = FormInput("Last Name *", "")
        self.birthdate = FormDate("Birthdate *")

        layout.addLayout(self.row(self.lrn, self.gender))
        layout.addLayout(self.row(self.firstname, self.middlename))
        layout.addLayout(self.row(self.lastname, self.birthdate))

        # CONTACT INFO
        layout.addWidget(SectionHeader("Contact Information"))
        self.email = FormInput("Email Address *", "student@example.com")
        self.phone = FormInput("Phone Number *", "+63 XXX XXX XXXX")
        layout.addLayout(self.row(self.email, self.phone))

        self.address = FormInput("Complete Address *", "Street, Barangay, City, Province")
        layout.addWidget(self.address)

        # ACADEMIC INFO
        layout.addWidget(SectionHeader("Academic Information"))
        self.grade = FormCombo("Grade Level *", ["Select grade level", "Grade 11", "Grade 12"])
        self.track = FormCombo("Track *", ["Select track"])  # Will be populated by controller
        layout.addLayout(self.row(self.grade, self.track))

        # STRAND / SPECIALIZATION
        self.strand_label = QLabel("Strand / Specialization")
        self.strand_label.setStyleSheet("""
            color: #374151;
            font-size: 14px;
            font-weight: 600;
            letter-spacing: 0.3px;
        """)
        self.strand_label.hide()

        self.strand_input = FormInput("", "")
        self.strand_input.hide()

        self.strand_combo = FormCombo("", ["Select strand"])
        self.strand_combo.hide()

        # Connect track change signal
        self.track.value_changed.connect(self.on_track_changed)

        layout.addWidget(self.strand_label)
        layout.addWidget(self.strand_input)
        layout.addWidget(self.strand_combo)

        # GUARDIAN INFO
        layout.addWidget(SectionHeader("Guardian Information"))
        self.guardian_name = FormInput("Guardian Name *", "")
        self.guardian_phone = FormInput("Guardian Contact *", "+63 XXX XXX XXXX")
        layout.addLayout(self.row(self.guardian_name, self.guardian_phone))

        # SUBMIT BUTTON
        submit = SubmitButton("Enroll Student")
        submit.clicked.connect(self.handle_submit)

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        btn_row.addWidget(submit)

        layout.addLayout(btn_row)

        return self.form

    def row(self, w1, w2):
        """Create a row layout with two widgets"""
        row = QHBoxLayout()
        row.setSpacing(40)
        row.addWidget(w1)
        row.addWidget(w2)
        return row

    def on_track_changed(self, track_name):
        """Handle track selection - emit signal for controller"""
        self.track_changed.emit(track_name)

    def handle_submit(self):
        """Collect form data and emit signal"""
        data = self.get_form_data()
        self.submit_clicked.emit(data)

    # ========================================================================
    # PUBLIC METHODS - Called by Controller
    # ========================================================================

    def set_tracks(self, tracks):
        """Set available tracks"""
        self.available_tracks = tracks
        self.track.set_options(["Select track"] + tracks)

    def show_strand_combo(self, strands):
        """Show strand dropdown with options"""
        self.strand_label.setText("Strand *")
        self.strand_label.show()
        self.strand_combo.set_options(strands)
        self.strand_combo.show()
        self.strand_input.hide()

    def show_strand_input(self, placeholder):
        """Show strand text input"""
        self.strand_label.setText("Strand / Specialization")
        self.strand_label.show()
        self.strand_input.input.setPlaceholderText(placeholder)
        self.strand_input.show()
        self.strand_combo.hide()

    def hide_strand_options(self):
        """Hide all strand options"""
        self.strand_label.hide()
        self.strand_input.hide()
        self.strand_combo.hide()

    def get_form_data(self):
        """Collect form data"""
        return {
            "lrn": self.lrn.value(),
            "gender": self.gender.value(),
            "firstname": self.firstname.value(),
            "middlename": self.middlename.value(),
            "lastname": self.lastname.value(),
            "birthdate": self.birthdate.value(),
            "email": self.email.value(),
            "phone": self.phone.value(),
            "address": self.address.value(),
            "grade": self.grade.value(),
            "track": self.track.value(),
            "strand": self.strand_combo.value() if self.strand_combo.isVisible() else self.strand_input.value(),
            "guardian_name": self.guardian_name.value(),
            "guardian_contact": self.guardian_phone.value()
        }

    def clear_form(self):
        """Clear all form fields"""
        self.lrn.clear()
        self.gender.clear()
        self.firstname.clear()
        self.middlename.clear()
        self.lastname.clear()
        self.birthdate.clear()
        self.email.clear()
        self.phone.clear()
        self.address.clear()
        self.grade.clear()
        self.track.clear()
        self.strand_input.clear()
        self.strand_combo.clear()
        self.strand_label.hide()
        self.strand_input.hide()
        self.strand_combo.hide()
        self.guardian_name.clear()
        self.guardian_phone.clear()

    def show_error(self, title, message):
        """Show error message"""
        QMessageBox.warning(self, title, message)

    def show_success(self, title, message):
        """Show success message"""
        QMessageBox.information(self, title, message)