"""
MAIN.PY - MVC Integration Fixed
Properly integrates View and Controller
"""

import sys
import os

os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'

from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QMessageBox
from PyQt6.QtCore import Qt

QApplication.setHighDpiScaleFactorRoundingPolicy(
    Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
)

print("=" * 80)
print("🚀 ENROLLIFY - Starting...")
print("=" * 80)

# ============================================================================
#
# ============================================================================
print("\n[1/4] Loading MVC Components...")

try:
    # ✅ CORRECT: Import View and Controller separately
    from enrollment_form_view import EnrollmentFormView
    from enrollment_controller import EnrollmentFormController
    print("  ✅ EnrollmentFormView (MVC)")
    print("  ✅ EnrollmentFormController (MVC)")
except Exception as e:
    print(f"  ❌ Enrollment MVC: {e}")
    EnrollmentFormView = None
    EnrollmentFormController = None

try:
    from home_screen import HomeScreen
    print("  ✅ HomeScreen")
except Exception as e:
    print(f"  ❌ HomeScreen: {e}")
    sys.exit(1)

try:
    from payment_screen import PaymentScreen
    print("  ✅ PaymentScreen")
except Exception as e:
    print(f"  ⚠️ PaymentScreen: {e}")
    PaymentScreen = None

# Import staff screens
try:
    from staff_login import StaffLoginScreen
    from admin_login import AdminLoginScreen
    from staff_portal import StaffPortalScreen
    from enrollees_screen import EnrolleesScreen
    from reports_screen import ReportsScreen
    from admin_screen import AdminScreen
    print("  ✅ Staff Screens")
    HAS_STAFF_SCREENS = True
except Exception as e:
    print(f"  ⚠️ Staff Screens: {e}")
    HAS_STAFF_SCREENS = False

# ============================================================================
# STEP 2: Setup Database
# ============================================================================
print("\n[2/4] Setting Up Database...")

db_instance = None
try:
    from database_manager_mysql import get_database
    db_instance = get_database(
        host="127.0.0.1",
        user="root",
        password="",
        database="enrollify_db"
    )
    print("  ✅ MySQL Connected")
except Exception as e:
    print(f"  ⚠️ Database: {e}")
    db_instance = None


# ============================================================================
# MAIN APPLICATION CLASS (UPDATED FOR MVC)
# ============================================================================
class EnrollifyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_user = None
        self.db = db_instance

        print("\n[3/4] Initializing Main Window...")

        self.setWindowTitle("Enrollify - Student Enrollment System (MVC)")
        self.setMinimumSize(1200, 800)

        # Create stacked widget
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        print("[4/4] Creating Screens...")

        # ====================================================================
        # HOME SCREEN
        # ====================================================================
        try:
            self.home_screen = HomeScreen()
            self.stacked_widget.addWidget(self.home_screen)
            print("  ✅ Home Screen")
        except Exception as e:
            print(f"  ❌ Home Screen: {e}")
            raise

        # ====================================================================
        # ENROLLMENT FORM (✅ MVC VERSION - FIXED!)
        # ====================================================================
        if EnrollmentFormView and EnrollmentFormController:
            try:
                # Create View
                self.enrollment_view = EnrollmentFormView()

                # Create Controller and connect it to View
                self.enrollment_controller = EnrollmentFormController(self.enrollment_view)

                # Connect controller signals to main app
                self.enrollment_controller.enrollment_complete.connect(
                    self.handle_enrollment_complete
                )

                # Connect view logout signal
                self.enrollment_view.logout_clicked.connect(self.show_home)

                # Add view to stacked widget
                self.stacked_widget.addWidget(self.enrollment_view)

                print("  ✅ Enrollment Form (MVC - View + Controller)")
            except Exception as e:
                print(f"  ❌ Enrollment Form: {e}")
                import traceback
                traceback.print_exc()
                self.enrollment_view = None
        else:
            print("  ⚠️ Enrollment Form: MVC components not available")
            self.enrollment_view = None

        # ====================================================================
        # PAYMENT SCREEN
        # ====================================================================
        self.payment_screen = None
        if PaymentScreen:
            try:
                self.payment_screen = PaymentScreen()
                self.stacked_widget.addWidget(self.payment_screen)
                print("  ✅ Payment Screen")
            except Exception as e:
                print(f"  ⚠️ Payment Screen: {e}")

        # ====================================================================
        # STAFF SCREENS
        # ====================================================================
        self.staff_screens_available = False
        if HAS_STAFF_SCREENS:
            try:
                self.staff_login = StaffLoginScreen()
                self.stacked_widget.addWidget(self.staff_login)

                self.admin_login = AdminLoginScreen()
                self.stacked_widget.addWidget(self.admin_login)

                self.staff_portal = StaffPortalScreen()
                self.stacked_widget.addWidget(self.staff_portal)

                self.enrollees_screen = EnrolleesScreen()
                self.stacked_widget.addWidget(self.enrollees_screen)

                self.reports_screen = ReportsScreen()
                self.stacked_widget.addWidget(self.reports_screen)

                self.admin_screen = AdminScreen()
                self.stacked_widget.addWidget(self.admin_screen)

                self.staff_screens_available = True
                print("  ✅ Staff Screens")
            except Exception as e:
                print(f"  ⚠️ Staff Screens: {e}")

        # ====================================================================
        # CONNECT SIGNALS
        # ====================================================================
        print("\n[5/6] Connecting Signals...")

        # Home screen
        self.home_screen.enroll_now_signal.connect(self.show_enrollment_form)
        self.home_screen.staff_login_signal.connect(self.show_staff_login)
        self.home_screen.admin_login_signal.connect(self.show_admin_login)
        print("  ✅ Home Screen Signals")

        # Payment screen
        if self.payment_screen:
            self.payment_screen.logout_signal.connect(self.show_home)
            self.payment_screen.back_signal.connect(self.show_enrollment_form)
            self.payment_screen.payment_completed.connect(self.handle_payment_completion)
            print("  ✅ Payment Screen Signals")

        # Staff screens
        if self.staff_screens_available:
            self.staff_login.back_signal.connect(self.show_home)
            self.staff_login.login_signal.connect(self.handle_staff_login)

            self.admin_login.back_signal.connect(self.show_home)
            self.admin_login.login_signal.connect(self.handle_admin_login)

            self.staff_portal.logout_signal.connect(self.show_home)
            self.enrollees_screen.logout_signal.connect(self.show_home)
            self.reports_screen.logout_signal.connect(self.show_home)
            self.admin_screen.logout_signal.connect(self.show_home)

            print("  ✅ Staff Screen Signals")

        # Show home screen
        self.show_home()

        print("\n[6/6] ✅ Application Ready!")
        print("=" * 80)
        print(f"\n📊 Feature Status:")
        print(f"  • Core Features: ✅ Available")
        print(f"  • MVC Pattern: ✅ Enrollment Form Refactored")
        print(f"  • Database: {'✅ Connected' if self.db else '❌ Not Connected'}")
        print(f"  • Payment: {'✅ Available' if self.payment_screen else '❌ Disabled'}")
        print(f"  • Staff Portal: {'✅ Available' if self.staff_screens_available else '❌ Disabled'}")
        print("=" * 80 + "\n")

    # ========================================================================
    # NAVIGATION METHODS
    # ========================================================================

    def show_home(self):
        """Show home screen"""
        self.stacked_widget.setCurrentWidget(self.home_screen)
        print("🏠 Navigated to: Home")

    def show_enrollment_form(self):
        """Show enrollment form"""
        if self.enrollment_view:
            self.stacked_widget.setCurrentWidget(self.enrollment_view)
            print("📝 Navigated to: Enrollment Form (MVC)")
        else:
            QMessageBox.warning(self, "Error", "Enrollment form not available")

    def show_payment_screen(self, student_data):
        """Show payment screen"""
        if self.payment_screen:
            try:
                self.payment_screen.set_student_data(student_data)
                self.stacked_widget.setCurrentWidget(self.payment_screen)
                print("💳 Navigated to: Payment Screen")
            except Exception as e:
                print(f"❌ Payment screen error: {e}")
                QMessageBox.warning(self, "Error", "Could not open payment screen.")
        else:
            QMessageBox.information(
                self, "Feature Unavailable",
                "Payment screen is not available."
            )

    def show_staff_login(self):
        """Show staff login screen"""
        if self.staff_screens_available:
            self.staff_login.email_input.clear()
            self.staff_login.password_input.clear()
            self.stacked_widget.setCurrentWidget(self.staff_login)
            print("🔑 Navigated to: Staff Login")
        else:
            QMessageBox.warning(self, "Feature Unavailable", "Staff Portal is not available.")

    def show_admin_login(self):
        """Show admin login screen"""
        if self.staff_screens_available:
            self.admin_login.email_input.clear()
            self.admin_login.password_input.clear()
            self.stacked_widget.setCurrentWidget(self.admin_login)
            print("🔑 Navigated to: Admin Login")
        else:
            QMessageBox.warning(self, "Feature Unavailable", "Admin Panel is not available.")

    def show_staff_portal(self):
        """Show staff portal"""
        if self.staff_screens_available:
            self.stacked_widget.setCurrentWidget(self.staff_portal)
            print("📊 Navigated to: Staff Portal")

    def show_admin_portal(self):
        """Show admin screen"""
        if self.staff_screens_available:
            self.stacked_widget.setCurrentWidget(self.admin_screen)
            print("⚙️ Navigated to: Admin Panel")

    # ========================================================================
    # EVENT HANDLERS
    # ========================================================================

    def handle_enrollment_complete(self, student_data):
        """
        ✅ Handle enrollment completion from MVC controller
        """
        print("\n" + "=" * 60)
        print("🎉 ENROLLMENT COMPLETE:")
        print("=" * 60)
        print(f"  Student: {student_data['firstname']} {student_data['lastname']}")
        print(f"  LRN: {student_data['lrn']}")
        print(f"  Track: {student_data['track']}")
        print("=" * 60)

        # Ask if they want to proceed to payment
        reply = QMessageBox.question(
            self,
            "Enrollment Complete",
            f"✅ {student_data['firstname']} {student_data['lastname']} has been enrolled!\n\n"
            f"Would you like to proceed to payment?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.show_payment_screen(student_data)
        else:
            self.show_home()

    def handle_payment_completion(self, payment_data):
        """Handle payment completion - UPDATED WITH RECEIPT"""
        print("\n" + "=" * 60)
        print("💳 PAYMENT COMPLETED:")
        print("=" * 60)
        print(f"  Amount: ₱{payment_data['amount']:,}")
        print(f"  Method: {payment_data['payment_method']}")
        print("=" * 60)

        # Save to database with receipt
        if self.db:
            try:
                # Generate receipt number if not provided
                if 'receipt_number' not in payment_data:
                    import random
                    from PyQt6.QtCore import QDateTime
                    receipt_number = f"{QDateTime.currentDateTime().toString('yyyyMMdd')}{random.randint(1000, 9999)}"
                    payment_data['receipt_number'] = receipt_number

                # Save payment with receipt number
                payment_id = self.db.add_payment_with_receipt(
                    payment_data,
                    payment_data.get('receipt_number')
                )
                print(f"✅ Payment saved! ID: {payment_id}, Receipt: {payment_data.get('receipt_number')}")

            except Exception as e:
                print(f"❌ Payment save error: {e}")
                QMessageBox.critical(self, "Error", f"Payment recording failed: {str(e)}")

        self.show_home()

    def handle_staff_login(self):
        """Handle staff login - UPDATED"""
        email = self.staff_login.email_input.text().strip()
        password = self.staff_login.password_input.text()

        if not email or not password:
            QMessageBox.warning(self, "Invalid Input", "Please enter email and password")
            return

        if self.db:
            try:
                user = self.db.authenticate_user(email, password)
                if user and user['role'] == 'STAFF':
                    self.current_user = user

                    # ✅ SET CURRENT USER FOR STAFF PORTAL
                    self.staff_portal.set_current_user(user)
                    self.enrollees_screen.set_current_user(user)

                    print(f"✅ Staff logged in: {user['full_name']} (ID: {user['id']})")

                    self.show_staff_portal()
                else:
                    QMessageBox.warning(self, "Login Failed", "Invalid credentials or not a staff account")
            except Exception as e:
                print(f"Login error: {e}")
                QMessageBox.critical(self, "Error", f"Login error: {str(e)}")

    def handle_admin_login(self):
        """Handle admin login"""
        email = self.admin_login.email_input.text().strip()
        password = self.admin_login.password_input.text()

        if not email or not password:
            QMessageBox.warning(self, "Invalid Input", "Please enter email and password")
            return

        if self.db:
            try:
                user = self.db.authenticate_user(email, password)
                if user and user['role'] == 'ADMIN':
                    self.current_user = user
                    self.admin_screen.current_user = user
                    self.show_admin_portal()
                else:
                    QMessageBox.warning(self, "Login Failed", "Invalid credentials")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Login error: {str(e)}")


# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================
def main():
    """Main entry point"""
    try:
        print("\nCreating Application...")
        app = QApplication(sys.argv)
        app.setStyle('Fusion')

        window = EnrollifyApp()
        window.showMaximized()

        print("\n✅ ENROLLIFY (MVC) IS NOW RUNNING!\n")

        sys.exit(app.exec())

    except Exception as e:
        print("\n" + "=" * 80)
        print("❌ CRITICAL ERROR")
        print("=" * 80)
        print(f"Error: {e}\n")
        import traceback
        traceback.print_exc()
        print("=" * 80)

        try:
            QMessageBox.critical(
                None, "Critical Error",
                f"Failed to start Enrollify:\n\n{str(e)}"
            )
        except:
            pass

        sys.exit(1)


if __name__ == '__main__':
    main()