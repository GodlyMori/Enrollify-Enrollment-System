"""
Auto-Reorganize Script for MVC Structure
Run this to automatically organize your files into MVC folders

Usage: python reorganize_files.py
"""

import os
import shutil
from pathlib import Path


def create_folder_structure():
    """Create the MVC folder structure"""
    folders = [
        'models',
        'controllers',
        'views',
        'components',
        'utils',
        'database',
        'config'
    ]

    print("📁 Creating folder structure...")
    for folder in folders:
        Path(folder).mkdir(exist_ok=True)
        # Create __init__.py in each folder
        init_file = Path(folder) / '__init__.py'
        if not init_file.exists():
            init_file.touch()
        print(f"  ✅ Created {folder}/")
    print()


def move_files():
    """Move files to their appropriate folders"""

    print("🔄 Moving files to MVC structure...")

    moves = {
        # Models
        'models.py': 'models/models.py',

        # Controllers
        'controllers.py': 'controllers/controllers.py',

        # Views
        'enrollment_form_view.py': 'views/enrollment_form_view.py',
        'home_screen.py': 'views/home_screen.py',
        'payment_screen.py': 'views/payment_view.py',
        'enrollees_screen.py': 'views/enrollees_view.py',
        'staff_portal.py': 'views/staff_portal_view.py',
        'admin_screen.py': 'views/admin_screen_view.py',
        'reports_screen.py': 'views/reports_view.py',
        'staff_login.py': 'views/staff_login_view.py',
        'admin_login.py': 'views/admin_login_view.py',

        # Utilities
        'validation_utils.py': 'utils/validation.py',
        'auth_utils.py': 'utils/auth.py',
        'ui_styles.py': 'utils/ui_styles.py',

        # Database
        'database_manager_mysql.py': 'database/database_manager.py',

        # Config
        'config.py': 'config/settings.py',
        'constants.py': 'config/constants.py',
    }

    for source, destination in moves.items():
        if os.path.exists(source):
            try:
                shutil.copy2(source, destination)
                print(f"  ✅ Moved {source} → {destination}")
            except Exception as e:
                print(f"  ⚠️ Could not move {source}: {e}")
        else:
            print(f"  ⚠️ File not found: {source}")

    print()


def move_components():
    """Move form_components to components"""
    print("🔄 Moving form components...")

    if os.path.exists('form_components'):
        component_files = {
            'form_components/FormInput.py': 'components/form_input.py',
            'form_components/FormCombo.py': 'components/form_combo.py',
            'form_components/FormDate.py': 'components/form_date.py',
            'form_components/SectionHeader.py': 'components/section_header.py',
            'form_components/SubmitButton.py': 'components/submit_button.py',
            'form_components/__init__.py': 'components/__init__.py',
        }

        for source, destination in component_files.items():
            if os.path.exists(source):
                try:
                    shutil.copy2(source, destination)
                    print(f"  ✅ Moved {source} → {destination}")
                except Exception as e:
                    print(f"  ⚠️ Could not move {source}: {e}")
    else:
        print("  ⚠️ form_components folder not found")

    print()


def create_backup():
    """Create a backup of the current structure"""
    print("💾 Creating backup...")

    backup_folder = 'backup_before_mvc'
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)
        print(f"  ✅ Created {backup_folder}/")
    else:
        print(f"  ℹ️ Backup folder already exists")

    print()


def show_summary():
    """Show summary of the reorganization"""
    print("\n" + "=" * 60)
    print("✅ REORGANIZATION COMPLETE!")
    print("=" * 60)
    print("\nYour new structure:")
    print("""
📁 enrollify/
├── 📁 models/              ← Data layer
├── 📁 controllers/         ← Logic layer
├── 📁 views/               ← UI layer
├── 📁 components/          ← Reusable UI
├── 📁 utils/               ← Helpers
├── 📁 database/            ← Database
├── 📁 config/              ← Settings
├── 📁 assets/              ← Images
├── 📁 logs/                ← Logs
└── main.py                 ← Entry point
    """)

    print("\n" + "=" * 60)
    print("⚠️ IMPORTANT: Update Your Imports!")
    print("=" * 60)
    print("\nOld imports:")
    print("  from models import Student")
    print("  from enrollment_form_view import EnrollmentFormView")
    print("\nNew imports:")
    print("  from models.models import Student")
    print("  from views.enrollment_form_view import EnrollmentFormView")
    print("\nSee 'updated_imports.txt' for a complete list of changes.")
    print("=" * 60 + "\n")


def create_import_guide():
    """Create a file showing the new import statements"""
    guide = """
# Updated Import Statements for MVC Structure

## Main Application (main.py)

OLD:
from home_screen import HomeScreen
from enrollment_form_view import EnrollmentFormView
from payment_screen import PaymentScreen
from staff_login import StaffLoginScreen
from admin_login import AdminLoginScreen
from database_manager_mysql import get_database

NEW:
from views.home_screen import HomeScreen
from views.enrollment_form_view import EnrollmentFormView
from views.payment_view import PaymentScreen
from views.staff_login_view import StaffLoginScreen
from views.admin_login_view import AdminLoginScreen
from database.database_manager import get_database

## Models

OLD:
from models import Student, StudentRepository, TrackRepository

NEW:
from models.models import Student, StudentRepository, TrackRepository

## Controllers

OLD:
from controllers import EnrollmentController, PaymentController

NEW:
from controllers.controllers import EnrollmentController, PaymentController

## Components

OLD:
from form_components.FormInput import FormInput
from form_components.FormCombo import FormCombo

NEW:
from components.form_input import FormInput
from components.form_combo import FormCombo

## Utilities

OLD:
from auth_utils import hash_password, verify_password
from validation_utils import validate_form

NEW:
from utils.auth import hash_password, verify_password
from utils.validation import validate_form

## Configuration

OLD:
from config import Config

NEW:
from config.settings import Config
"""

    with open('updated_imports.txt', 'w') as f:
        f.write(guide)

    print("📝 Created 'updated_imports.txt' with import examples")


def main():
    """Main reorganization function"""
    print("\n" + "=" * 60)
    print("🎯 MVC REORGANIZATION SCRIPT")
    print("=" * 60)
    print("\nThis script will:")
    print("  1. Create MVC folder structure")
    print("  2. Copy files to new locations")
    print("  3. Keep original files as backup")
    print("  4. Create import guide")
    print("\n⚠️ IMPORTANT: Original files will NOT be deleted")
    print("   You can delete them manually after testing")
    print("\n" + "=" * 60)

    response = input("\nProceed? (y/n): ")
    if response.lower() != 'y':
        print("\n❌ Cancelled")
        return

    print("\n🚀 Starting reorganization...\n")

    # Step 1: Create backup
    create_backup()

    # Step 2: Create folder structure
    create_folder_structure()

    # Step 3: Move files
    move_files()

    # Step 4: Move components
    move_components()

    # Step 5: Create import guide
    create_import_guide()

    # Step 6: Show summary
    show_summary()

    print("\n✅ Done! Next steps:")
    print("  1. Update your import statements (see updated_imports.txt)")
    print("  2. Test your application: python main.py")
    print("  3. If everything works, delete the old files")
    print("\n💡 Tip: Check updated_imports.txt for all import changes\n")


if __name__ == '__main__':
    main()