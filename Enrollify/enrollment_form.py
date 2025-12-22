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
import traceback
import os

class EnrollmentForm(QWidget):
    logout_signal = pyqtSignal()
    enrollment_submitted = pyqtSignal(dict)
    proceed_to_payment = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #F8FAFA;")

        # Initialize database connection safely
        self.db = None
        try:
            from database_manager_mysql import get_database
            self.db = get_database()
            print("✅ Database connected successfully")
        except Exception as e:
            print(f"⚠️ Database connection failed: {e}")

        # Load tracks safely
        self.available_tracks = self.load_tracks()

        # Build UI
        try:
            self.build_ui()
            print("✅ Enrollment form UI built successfully")
        except Exception as e:
            print(f"❌ Error building UI: {e}")
            traceback.print_exc()

    def load_tracks(self):
        """Safely load available tracks from database"""
        try:
            if self.db:
                tracks = self.db.get_all_tracks()
                print(f"✅ Loaded {len(tracks)} tracks from database")
                return tracks
        except Exception as e:
            print(f"⚠️ Failed to load tracks: {e}")

        # Fallback to default tracks
        return ["Academic", "TVL", "Sports", "Arts & Design"]

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
        """Build header with logout button - text-only logo"""
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
            QPushButton:hover {
                background-color: #F0FAF8;
            }
        """)
        logout_btn.clicked.connect(self.safe_logout)

        layout.addWidget(logo)
        layout.addLayout(titles)
        layout.addStretch()
        layout.addWidget(logout_btn)

        return header

    def safe_logout(self):
        """Safely emit logout signal"""
        try:
            print("🔓 Logout button clicked")
            self.logout_signal.emit()
        except Exception as e:
            print(f"❌ Logout error: {e}")

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

    def on_track_changed(self, track_name):
        """Handle track selection changes"""
        try:
            print(f"📝 Track changed to: {track_name}")

            self.strand_label.hide()
            self.strand_input.hide()
            self.strand_combo.hide()

            if track_name in ["Academic", "TVL"]:
                self.strand_label.setText("Strand *")
                self.strand_label.show()

                if self.db:
                    try:
                        strands = self.db.get_strands_by_track(track_name)
                        if strands:
                            self.strand_combo.set_options(["Select strand"] + strands)
                            self.strand_combo.show()
                        else:
                            self.strand_input.set_placeholder("Enter strand (e.g., STEM, Cookery)")
                            self.strand_input.show()
                    except Exception as e:
                        print(f"⚠️ Error loading strands: {e}")
                        self.strand_input.set_placeholder("Enter strand")
                        self.strand_input.show()
                else:
                    self.strand_input.set_placeholder("Enter strand")
                    self.strand_input.show()

            elif track_name in ["Sports", "Arts & Design"]:
                self.strand_label.setText("Specialization (Optional)")
                self.strand_label.show()
                self.strand_input.set_placeholder("e.g., Basketball, Digital Art")
                self.strand_input.show()

        except Exception as e:
            print(f"❌ Error in track change handler: {e}")
            traceback.print_exc()

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

        track_options = ["Select track"] + self.available_tracks
        self.track = FormCombo("Track *", track_options)
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

        # Connect track change signal safely
        try:
            self.track.value_changed.connect(self.on_track_changed)
        except Exception as e:
            print(f"⚠️ Error connecting track signal: {e}")

        layout.addWidget(self.strand_label)
        layout.addWidget(self.strand_input)
        layout.addWidget(self.strand_combo)

        # GUARDIAN INFO
        layout.addWidget(SectionHeader("Guardian Information"))
        self.guardian_name = FormInput("Guardian Name *", "")
        self.guardian_phone = FormInput("Guardian Contact *", "+63 XXX XXX XXX XXXX")
        layout.addLayout(self.row(self.guardian_name, self.guardian_phone))

        # SUBMIT BUTTON
        submit = SubmitButton("Enroll Student")
        submit.clicked.connect(self.safe_submit_enrollment)

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

    def collect_data(self):
        """Safely collect form data"""
        try:
            data = {
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
            print("✅ Form data collected successfully")
            return data
        except Exception as e:
            print(f"❌ Error collecting form data: {e}")
            traceback.print_exc()
            return None

    def validate(self):
        """Validate form data with proper error messages"""
        try:
            data = self.collect_data()
            if not data:
                QMessageBox.warning(self, "Error", "Failed to collect form data")
                return False

            required_fields = {
                "lrn": "Learner Reference Number (LRN)",
                "gender": "Gender",
                "firstname": "First Name",
                "lastname": "Last Name",
                "birthdate": "Birthdate",
                "email": "Email Address",
                "phone": "Phone Number",
                "address": "Complete Address",
                "grade": "Grade Level",
                "track": "Track",
                "guardian_name": "Guardian Name",
                "guardian_contact": "Guardian Contact"
            }

            for key, label in required_fields.items():
                value = data.get(key, "")
                if not value or value.startswith("Select "):
                    QMessageBox.warning(self, "Validation Error", f"Please fill in: {label}")
                    return False

            # Track-specific strand validation
            if data["track"] in ["Academic", "TVL"]:
                strand = data["strand"]
                if not strand or strand == "Select strand":
                    QMessageBox.warning(self, "Validation Error",
                                        "Please select or enter a valid strand for this track")
                    return False

            # Validate track against database
            if self.db:
                try:
                    if not self.db.is_valid_track(data["track"]):
                        QMessageBox.warning(self, "Validation Error",
                                            "Invalid track selected. Please choose a valid track.")
                        return False
                except Exception as e:
                    print(f"⚠️ Track validation error: {e}")

            # Validate LRN format
            if not data["lrn"].isdigit() or len(data["lrn"]) != 12:
                QMessageBox.warning(self, "Validation Error",
                                    "LRN must be exactly 12 digits")
                return False

            print("✅ All validations passed")
            return True

        except Exception as e:
            print(f"❌ Validation error: {e}")
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Validation failed: {str(e)}")
            return False

    def safe_submit_enrollment(self):
        """Safely submit enrollment with comprehensive error handling"""
        try:
            print("\n" + "=" * 60)
            print("📝 STARTING ENROLLMENT SUBMISSION")
            print("=" * 60)

            # Step 1: Validate
            print("Step 1: Validating form...")
            if not self.validate():
                print("❌ Validation failed")
                return
            print("✅ Validation passed")

            # Step 2: Collect data
            print("Step 2: Collecting data...")
            data = self.collect_data()
            if not data:
                QMessageBox.critical(self, "Error", "Failed to collect form data")
                return
            print("✅ Data collected")

            # Step 3: Save to database
            if self.db:
                print("Step 3: Saving to database...")
                try:
                    student_id = self.db.add_student(data)
                    print(f"✅ Student saved with ID: {student_id}")

                    QMessageBox.information(
                        self, "Success",
                        f"✅ Enrollment Submitted!\n\n"
                        f"Student: {data['firstname']} {data['lastname']}\n"
                        f"LRN: {data['lrn']}\n\n"
                        f"Your enrollment has been saved successfully!"
                    )
                except Exception as db_error:
                    print(f"❌ Database error: {db_error}")
                    traceback.print_exc()
                    QMessageBox.critical(
                        self, "Database Error",
                        f"Failed to save enrollment:\n{str(db_error)}"
                    )
                    return
            else:
                print("⚠️ No database connection - showing mock success")
                QMessageBox.information(
                    self, "Submitted",
                    "Enrollment form submitted!\n(Database not connected - this is a demo)"
                )

            # Step 4: Emit signals
            print("Step 4: Emitting signals...")
            try:
                self.enrollment_submitted.emit(data)
                print("✅ enrollment_submitted signal emitted")
            except Exception as signal_error:
                print(f"⚠️ Signal emit error: {signal_error}")

            # Step 5: Proceed to payment (optional)
            try:
                self.proceed_to_payment.emit(data)
                print("✅ proceed_to_payment signal emitted")
            except Exception as payment_error:
                print(f"⚠️ Payment signal error: {payment_error}")

            # Step 6: Clear form
            print("Step 5: Clearing form...")
            self.clear_form()
            print("✅ Form cleared")

            print("=" * 60)
            print("✅ ENROLLMENT SUBMISSION COMPLETED")
            print("=" * 60 + "\n")

        except Exception as e:
            print(f"\n❌ CRITICAL ERROR IN SUBMISSION:")
            print(f"Error: {e}")
            traceback.print_exc()
            print("=" * 60 + "\n")

            try:
                QMessageBox.critical(
                    self, "Submission Error",
                    f"An error occurred during submission:\n\n{str(e)}\n\n"
                    f"Please try again or contact support."
                )
            except:
                print("❌ Failed to show error message box")

    def clear_form(self):
        """Clear all form fields"""
        try:
            self.lrn.setValue("")
            self.gender.setValue("Select gender")
            self.firstname.setValue("")
            self.middlename.setValue("")
            self.lastname.setValue("")
            self.birthdate.setValue("")
            self.email.setValue("")
            self.phone.setValue("")
            self.address.setValue("")
            self.grade.setValue("Select grade level")
            self.track.setValue("Select track")
            self.strand_input.setValue("")
            self.strand_input.hide()
            self.strand_combo.setValue("Select strand")
            self.strand_combo.hide()
            self.strand_label.hide()
            self.guardian_name.setValue("")
            self.guardian_phone.setValue("")
            print("✅ Form cleared successfully")
        except Exception as e:
            print(f"⚠️ Error clearing form: {e}")