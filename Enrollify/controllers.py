"""
CONTROLLER LAYER - Handles Business Logic and Coordination
This is the "what connects them" part
"""

from PyQt6.QtWidgets import QMessageBox
from models import (
    Student, StudentRepository, TrackRepository,
    PaymentRepository, StatisticsRepository, Payment
)


class EnrollmentController:
    """
    Controller for Enrollment Form
    Handles all enrollment-related logic
    """

    def __init__(self, view):
        """
        Initialize controller with a view
        Args:
            view: The EnrollmentFormView instance
        """
        self.view = view
        self.student_repo = StudentRepository()
        self.track_repo = TrackRepository()

        # Connect view signals to controller methods
        self.connect_signals()

    def connect_signals(self):
        """Connect UI signals to controller methods"""
        # When track changes, update strand options
        if hasattr(self.view, 'on_track_changed_signal'):
            self.view.on_track_changed_signal.connect(self.handle_track_change)

        # When submit button clicked, process enrollment
        if hasattr(self.view, 'submit_clicked_signal'):
            self.view.submit_clicked_signal.connect(self.submit_enrollment)

    def load_initial_data(self):
        """Load initial data when form opens"""
        # Load available tracks
        tracks = self.track_repo.get_all()
        self.view.set_track_options(["Select track"] + tracks)

    def handle_track_change(self, track_name):
        """
        Handle when user selects a different track
        Args:
            track_name: The selected track name
        """
        print(f"📝 Controller: Track changed to {track_name}")

        # Hide strand options by default
        self.view.hide_strand_options()

        # If Academic or TVL, show strand dropdown
        if track_name in ["Academic", "TVL"]:
            strands = self.track_repo.get_strands_for_track(track_name)

            if strands:
                # Show dropdown with database strands
                self.view.show_strand_combo(["Select strand"] + strands)
            else:
                # Show text input if no strands in database
                self.view.show_strand_input("Enter strand (e.g., STEM, Cookery)")

        # If Sports or Arts, show optional specialization
        elif track_name in ["Sports", "Arts & Design"]:
            self.view.show_strand_input("Specialization (Optional)")

    def submit_enrollment(self):
        """
        Process enrollment form submission
        This is the main business logic method
        """
        print("\n" + "=" * 60)
        print("🎯 Controller: Processing Enrollment")
        print("=" * 60)

        # Step 1: Collect data from view
        form_data = self.view.get_form_data()

        # Step 2: Create Student model
        student = Student(form_data)

        # Step 3: Validate student data
        is_valid, error_message = student.validate()
        if not is_valid:
            self.view.show_error("Validation Error", error_message)
            return

        # Step 4: Check if track is valid
        if not self.track_repo.is_valid(student.track):
            self.view.show_error(
                "Invalid Track",
                f"'{student.track}' is not a valid track. Please select from available tracks."
            )
            return

        # Step 5: Save to database
        try:
            student_id = self.student_repo.save(student)

            print(f"✅ Student saved with ID: {student_id}")

            # Step 6: Show success message
            self.view.show_success(
                "Enrollment Successful!",
                f"Student: {student.get_full_name()}\n"
                f"LRN: {student.lrn}\n\n"
                f"Enrollment has been saved successfully!"
            )

            # Step 7: Clear form
            self.view.clear_form()

            # Step 8: Notify other parts of system (optional)
            self.view.notify_enrollment_complete(student)

            print("=" * 60)
            print("✅ Enrollment Complete!")
            print("=" * 60 + "\n")

        except Exception as e:
            print(f"❌ Error: {e}")
            self.view.show_error(
                "Database Error",
                f"Failed to save enrollment:\n{str(e)}"
            )


class StudentManagementController:
    """
    Controller for Student Management (Enrollees Screen)
    Handles viewing, editing, filtering students
    """

    def __init__(self, view):
        self.view = view
        self.student_repo = StudentRepository()
        self.all_students = []
        self.filtered_students = []

    def load_students(self):
        """Load all students and display them"""
        print("📋 Loading all students...")

        try:
            self.all_students = self.student_repo.find_all()
            self.filtered_students = self.all_students.copy()
            self.view.display_students(self.filtered_students)

            print(f"✅ Loaded {len(self.all_students)} students")
        except Exception as e:
            print(f"❌ Error loading students: {e}")
            self.view.show_error("Error", f"Failed to load students: {str(e)}")

    def filter_students(self, search_text="", grade=None, track=None, status=None):
        """
        Filter students based on criteria
        """
        print(f"🔍 Filtering: search='{search_text}', grade={grade}, track={track}, status={status}")

        self.filtered_students = []

        for student in self.all_students:
            # Search filter
            if search_text:
                search_lower = search_text.lower()
                if (search_lower not in student.lrn.lower() and
                        search_lower not in student.get_full_name().lower()):
                    continue

            # Grade filter
            if grade and grade != "All Grades" and student.grade != grade:
                continue

            # Track filter
            if track and track != "All Tracks" and student.track != track:
                continue

            # Status filter
            if status and status != "All Status" and student.status != status:
                continue

            self.filtered_students.append(student)

        # Update view
        self.view.display_students(self.filtered_students)
        print(f"✅ Found {len(self.filtered_students)} students")

    def update_student_status(self, lrn, new_status):
        """Update student enrollment status"""
        print(f"🔄 Updating {lrn} status to {new_status}")

        try:
            success = self.student_repo.update_status(lrn, new_status)

            if success:
                self.view.show_success(
                    "Success",
                    f"Status updated to '{new_status}'"
                )
                # Reload students to show updated data
                self.load_students()

        except Exception as e:
            print(f"❌ Error: {e}")
            self.view.show_error("Error", f"Failed to update status: {str(e)}")

    def delete_student(self, student):
        """Delete a student"""
        # Confirm with user first
        confirmed = self.view.confirm_delete(
            f"Delete {student.get_full_name()}?",
            "This action cannot be undone."
        )

        if confirmed:
            try:
                self.student_repo.delete(student.lrn)
                self.view.show_success("Success", "Student deleted")
                self.load_students()
            except Exception as e:
                print(f"❌ Error: {e}")
                self.view.show_error("Error", f"Failed to delete: {str(e)}")

    def view_student_details(self, student):
        """Show detailed view of a student"""
        self.view.show_student_details(student)


class PaymentController:
    """
    Controller for Payment Processing
    """

    def __init__(self, view):
        self.view = view
        self.payment_repo = PaymentRepository()
        self.student_data = None
        self.payment_amount = 0

    def set_student_data(self, student_data):
        """Set student data for payment"""
        self.student_data = student_data

        # Calculate fees based on track/strand
        from database_manager_mysql import get_database
        db = get_database()

        track = student_data.get('track', 'Academic')
        strand = student_data.get('strand', '').strip() or None

        fees = db.get_tuition_fees(track, strand)
        self.payment_amount = fees['total']

        # Update view with student info and fees
        self.view.display_student_info(student_data)
        self.view.display_fee_breakdown(fees)

    def process_payment(self, payment_method):
        """Process payment transaction"""
        print(f"💳 Processing payment: {payment_method}")

        if not payment_method:
            self.view.show_error("Error", "Please select a payment method")
            return

        # Confirm with user
        confirmed = self.view.confirm_payment(
            f"Confirm payment of ₱{self.payment_amount:,.2f}?",
            f"Payment method: {payment_method}"
        )

        if confirmed:
            try:
                # Create payment model
                payment = Payment(
                    self.student_data,
                    self.payment_amount,
                    payment_method
                )

                # Save payment
                payment_id = self.payment_repo.save(payment)

                print(f"✅ Payment saved with ID: {payment_id}")

                # Show success
                self.view.show_success(
                    "Payment Successful",
                    f"Payment of ₱{self.payment_amount:,.2f} recorded!\n\n"
                    f"Payment ID: {payment_id}\n"
                    f"Student: {self.student_data['firstname']} {self.student_data['lastname']}\n\n"
                    "Enrollment is now complete!"
                )

                # Notify completion
                self.view.notify_payment_complete(payment)

            except Exception as e:
                print(f"❌ Error: {e}")
                self.view.show_error("Error", f"Payment failed: {str(e)}")


class AnalyticsController:
    """
    Controller for Analytics Dashboard
    Handles statistics and reporting
    """

    def __init__(self, view):
        self.view = view
        self.stats_repo = StatisticsRepository()
        self.student_repo = StudentRepository()

    def load_overview_stats(self):
        """Load overview statistics"""
        try:
            stats = self.stats_repo.get_overview()
            self.view.display_overview(stats)
        except Exception as e:
            print(f"❌ Error loading stats: {e}")
            self.view.show_error("Error", f"Failed to load statistics: {str(e)}")

    def load_track_distribution(self):
        """Load track distribution data"""
        try:
            data = self.stats_repo.get_track_distribution()
            self.view.display_track_chart(data)
        except Exception as e:
            print(f"❌ Error loading tracks: {e}")

    def load_grade_distribution(self):
        """Load grade distribution data"""
        try:
            data = self.stats_repo.get_grade_distribution()
            self.view.display_grade_chart(data)
        except Exception as e:
            print(f"❌ Error loading grades: {e}")

    def refresh_all_data(self):
        """Refresh all analytics data"""
        self.load_overview_stats()
        self.load_track_distribution()
        self.load_grade_distribution()


class AuthenticationController:
    """
    Controller for Login/Authentication
    """

    def __init__(self, view):
        self.view = view
        from database_manager_mysql import get_database
        self.db = get_database()
        self.current_user = None

    def login(self, email, password):
        """
        Authenticate user login
        Returns: user_data if successful, None otherwise
        """
        print(f"🔐 Login attempt: {email}")

        # Validate inputs
        if not email or not password:
            self.view.show_error("Invalid Input", "Please enter email and password")
            return None

        if len(password) < 6:
            self.view.show_error("Invalid Input", "Password must be at least 6 characters")
            return None

        try:
            # Authenticate with database
            user = self.db.authenticate_user(email, password)

            if user:
                self.current_user = user
                print(f"✅ Login successful: {user['full_name']}")
                return user
            else:
                print("❌ Invalid credentials")
                self.view.show_error("Login Failed", "Invalid email or password")
                return None

        except Exception as e:
            print(f"❌ Login error: {e}")
            self.view.show_error("Error", f"Login failed: {str(e)}")
            return None

    def logout(self):
        """Logout current user"""
        if self.current_user:
            print(f"👋 Logout: {self.current_user['full_name']}")
        self.current_user = None

    def get_current_user(self):
        """Get currently logged in user"""
        return self.current_user