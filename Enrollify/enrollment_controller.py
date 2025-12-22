"""
ENROLLMENT FORM CONTROLLER - MVC Pattern
Handles business logic and coordinates between View and Model
"""

from PyQt6.QtCore import QObject, pyqtSignal


class EnrollmentFormController(QObject):
    """
    ✅ CONTROLLER LAYER - Business logic, no UI code
    """

    # Signals to communicate with main app
    enrollment_complete = pyqtSignal(dict)  # Emits student data when enrollment succeeds

    def __init__(self, view):
        super().__init__()
        self.view = view

        # Initialize database and repositories
        self.db = None
        self.init_database()

        # Connect view signals to controller methods
        self.connect_signals()

        # Load initial data
        self.load_tracks()

    def init_database(self):
        """Initialize database connection"""
        try:
            from database_manager_mysql import get_database
            self.db = get_database()
            print("✅ Controller: Database connected")
        except Exception as e:
            print(f"⚠️ Controller: Database connection failed: {e}")
            self.db = None

    def connect_signals(self):
        """Connect view signals to controller methods"""
        self.view.submit_clicked.connect(self.handle_submit)
        self.view.track_changed.connect(self.handle_track_change)

    def load_tracks(self):
        """Load available tracks from database"""
        try:
            if self.db:
                tracks = self.db.get_all_tracks()
                self.view.set_tracks(tracks)
                print(f"✅ Loaded {len(tracks)} tracks")
            else:
                # Fallback tracks
                self.view.set_tracks(["Academic", "TVL", "Sports", "Arts & Design"])
        except Exception as e:
            print(f"⚠️ Error loading tracks: {e}")
            self.view.set_tracks(["Academic", "TVL", "Sports", "Arts & Design"])

    def handle_track_change(self, track_name):
        """Handle track selection change"""
        print(f"🔄 Track changed: {track_name}")

        # Hide strand options by default
        self.view.hide_strand_options()

        # If Academic or TVL, show strand options
        if track_name in ["Academic", "TVL", "Academic Track", "TVL Track"]:
            if self.db:
                try:
                    strands = self.db.get_strands_by_track(track_name)
                    if strands:
                        self.view.show_strand_combo(["Select strand"] + strands)
                    else:
                        self.view.show_strand_input("Enter strand (e.g., STEM, Cookery)")
                except Exception as e:
                    print(f"⚠️ Error loading strands: {e}")
                    self.view.show_strand_input("Enter strand")
            else:
                self.view.show_strand_input("Enter strand")

        # If Sports or Arts, show optional specialization
        elif track_name in ["Sports", "Arts & Design", "Sports Track", "Arts and Design Track"]:
            self.view.show_strand_input("Specialization (Optional)")

    def handle_submit(self, form_data):
        """Handle form submission"""
        print("\n" + "=" * 60)
        print("🎯 ENROLLMENT SUBMISSION")
        print("=" * 60)

        # Step 1: Validate
        is_valid, error_msg = self.validate_form(form_data)
        if not is_valid:
            self.view.show_error("Validation Error", error_msg)
            return

        print("✅ Validation passed")

        # Step 2: Save to database
        if self.db:
            try:
                student_id = self.db.add_student(form_data)
                print(f"✅ Student saved with ID: {student_id}")

                # Show success message
                self.view.show_success(
                    "Enrollment Successful!",
                    f"Student: {form_data['firstname']} {form_data['lastname']}\n"
                    f"LRN: {form_data['lrn']}\n\n"
                    f"Enrollment has been saved successfully!"
                )

                # Clear form
                self.view.clear_form()

                # Emit signal for main app
                self.enrollment_complete.emit(form_data)

                print("=" * 60)
                print("✅ ENROLLMENT COMPLETE")
                print("=" * 60 + "\n")

            except Exception as e:
                print(f"❌ Database error: {e}")
                self.view.show_error("Database Error", f"Failed to save enrollment:\n{str(e)}")
        else:
            # No database - show mock success
            self.view.show_success(
                "Form Submitted",
                "Enrollment form submitted!\n(Database not connected - this is a demo)"
            )
            self.view.clear_form()

    def validate_form(self, data):
        """Validate form data"""
        # Required fields
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
                return False, f"Please fill in: {label}"

        # Validate LRN format
        if not data["lrn"].isdigit() or len(data["lrn"]) != 12:
            return False, "LRN must be exactly 12 digits"

        # Track-specific strand validation
        if data["track"] in ["Academic", "TVL", "Academic Track", "TVL Track"]:
            strand = data["strand"]
            if not strand or strand == "Select strand":
                return False, "Please select or enter a valid strand for this track"

        # Validate track against database
        if self.db:
            try:
                if not self.db.is_valid_track(data["track"]):
                    return False, "Invalid track selected. Please choose a valid track."
            except Exception as e:
                print(f"⚠️ Track validation error: {e}")

        return True, ""