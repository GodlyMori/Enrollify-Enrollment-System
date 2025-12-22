"""
ENROLLIFY SYSTEM DIAGNOSTIC TOOL
Run this FIRST to identify all problems preventing your system from running
"""

import sys
import os
from pathlib import Path

print("=" * 80)
print("🔍 ENROLLIFY SYSTEM DIAGNOSTIC")
print("=" * 80)

# Track all issues
issues = []
warnings = []
passed = []

# ============================================================================
# TEST 1: Python Version
# ============================================================================
print("\n[TEST 1] Checking Python Version...")
if sys.version_info >= (3, 8):
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    passed.append("Python version is compatible")
else:
    print(f"❌ Python {sys.version_info.major}.{sys.version_info.minor} (Need 3.8+)")
    issues.append("CRITICAL: Upgrade Python to 3.8 or higher")

# ============================================================================
# TEST 2: Required Packages
# ============================================================================
print("\n[TEST 2] Checking Required Packages...")

required_packages = {
    'PyQt6': 'PyQt6',
    'PyQt6.QtWebEngineWidgets': 'PyQt6-WebEngine',
    'mysql.connector': 'mysql-connector-python',
    'plotly': 'plotly'
}

missing_packages = []

for module_name, package_name in required_packages.items():
    try:
        __import__(module_name)
        print(f"✅ {package_name}")
        passed.append(f"{package_name} installed")
    except ImportError:
        print(f"❌ {package_name} - NOT INSTALLED")
        missing_packages.append(package_name)
        issues.append(f"CRITICAL: Missing package '{package_name}'")

# ============================================================================
# TEST 3: File Structure
# ============================================================================
print("\n[TEST 3] Checking File Structure...")

required_files = [
    'main.py',
    'home_screen.py',
    'enrollment_form.py',
    'staff_login.py',
    'admin_login.py',
    'staff_portal.py',
    'admin_screen.py',
    'enrollees_screen.py',
    'reports_screen.py',
    'payment_screen.py',
    'components.py',
    'config.py',
    'database_manager.py'
]

missing_files = []

for file in required_files:
    if os.path.exists(file):
        print(f"✅ {file}")
        passed.append(f"File {file} exists")
    else:
        print(f"❌ {file} - MISSING")
        missing_files.append(file)
        issues.append(f"ERROR: Missing file '{file}'")

# ============================================================================
# TEST 4: Form Components Folder
# ============================================================================
print("\n[TEST 4] Checking form_components Folder...")

form_components_path = Path('form_components')
if form_components_path.exists() and form_components_path.is_dir():
    print(f"✅ form_components/ folder exists")

    required_components = [
        'FormInput.py',
        'FormCombo.py',
        'FormDate.py',
        'SectionHeader.py',
        'SubmitButton.py',
        '__init__.py'
    ]

    for component in required_components:
        component_path = form_components_path / component
        if component_path.exists():
            print(f"  ✅ {component}")
            passed.append(f"Form component {component} exists")
        else:
            print(f"  ❌ {component} - MISSING")
            issues.append(f"ERROR: Missing form component '{component}'")
else:
    print(f"❌ form_components/ folder - MISSING")
    issues.append("CRITICAL: form_components folder not found")

# ============================================================================
# TEST 5: Assets Folder
# ============================================================================
print("\n[TEST 5] Checking Assets...")

assets_path = Path('assets')
if assets_path.exists():
    print(f"✅ assets/ folder exists")
    if (assets_path / 'enrollify_logo.png').exists():
        print(f"  ✅ enrollify_logo.png")
        passed.append("Logo file exists")
    else:
        print(f"  ⚠️  enrollify_logo.png - MISSING (will use fallback)")
        warnings.append("Logo missing - system will use fallback icons")
else:
    print(f"⚠️  assets/ folder - MISSING (will use fallback icons)")
    warnings.append("Assets folder missing - system will use fallback icons")

# ============================================================================
# TEST 6: Database Configuration
# ============================================================================
print("\n[TEST 6] Checking Database Configuration...")

try:
    from config import Config

    print(f"✅ config.py loaded")
    print(f"  Database: {Config.DB_NAME}")
    print(f"  Host: {Config.DB_HOST}")
    print(f"  Port: {Config.DB_PORT}")
    print(f"  User: {Config.DB_USER}")
    passed.append("Configuration file loaded")
except Exception as e:
    print(f"❌ config.py - ERROR: {e}")
    issues.append(f"CRITICAL: Config file error - {e}")

# ============================================================================
# TEST 7: Database Manager Import
# ============================================================================
print("\n[TEST 7] Testing Database Manager...")

db_managers = [
    'database_manager.py',
    'database_manager_mysql_OLD.py',
    'database_manager_enhanced.py'
]

found_db_managers = [f for f in db_managers if os.path.exists(f)]

if len(found_db_managers) == 0:
    print(f"❌ No database manager found")
    issues.append("CRITICAL: No database manager file found")
elif len(found_db_managers) > 1:
    print(f"⚠️  Multiple database managers found:")
    for mgr in found_db_managers:
        print(f"    - {mgr}")
    warnings.append(f"Multiple database managers may cause confusion")
else:
    print(f"✅ Using {found_db_managers[0]}")
    passed.append(f"Database manager: {found_db_managers[0]}")

# ============================================================================
# TEST 8: Try Importing Main Components
# ============================================================================
print("\n[TEST 8] Testing Component Imports...")

components_to_test = [
    ('home_screen', 'HomeScreen'),
    ('staff_login', 'StaffLoginScreen'),
    ('admin_login', 'AdminLoginScreen'),
]

for module_name, class_name in components_to_test:
    try:
        module = __import__(module_name)
        getattr(module, class_name)
        print(f"✅ {module_name}.{class_name}")
        passed.append(f"Import {module_name}.{class_name} successful")
    except ImportError as e:
        print(f"❌ {module_name}.{class_name} - Import Error: {e}")
        issues.append(f"ERROR: Cannot import {module_name}.{class_name}")
    except AttributeError as e:
        print(f"❌ {module_name}.{class_name} - Class not found: {e}")
        issues.append(f"ERROR: Class {class_name} not found in {module_name}")
    except Exception as e:
        print(f"❌ {module_name}.{class_name} - Error: {e}")
        issues.append(f"ERROR: {module_name}.{class_name} - {e}")

# ============================================================================
# FINAL REPORT
# ============================================================================
print("\n" + "=" * 80)
print("📊 DIAGNOSTIC REPORT")
print("=" * 80)

print(f"\n✅ PASSED: {len(passed)} checks")
print(f"⚠️  WARNINGS: {len(warnings)} issues")
print(f"❌ ERRORS: {len(issues)} critical issues")

if issues:
    print("\n" + "🔴 CRITICAL ISSUES (Must fix these!):")
    print("-" * 80)
    for i, issue in enumerate(issues, 1):
        print(f"{i}. {issue}")

if warnings:
    print("\n" + "🟡 WARNINGS (Should fix but not critical):")
    print("-" * 80)
    for i, warning in enumerate(warnings, 1):
        print(f"{i}. {warning}")

# ============================================================================
# SOLUTION GUIDE
# ============================================================================
print("\n" + "=" * 80)
print("💡 SOLUTION GUIDE")
print("=" * 80)

if missing_packages:
    print("\n📦 STEP 1: Install Missing Packages")
    print("-" * 80)
    print("Copy and run this command:\n")
    install_cmd = "pip install " + " ".join(missing_packages)
    print(f"    {install_cmd}")

if missing_files:
    print("\n📁 STEP 2: Missing Files")
    print("-" * 80)
    print("The following files are missing:")
    for file in missing_files:
        print(f"    - {file}")
    print("\nYou need to ensure all files are in your project folder.")

if not issues:
    print("\n🎉 GREAT NEWS!")
    print("-" * 80)
    print("Your system appears to be configured correctly!")
    print("\nTry running: python main.py")
else:
    print("\n🔧 NEXT STEPS:")
    print("-" * 80)
    print("1. Fix all CRITICAL issues listed above")
    print("2. Run this diagnostic again: python diagnostic_complete.py")
    print("3. Once all issues are fixed, run: python main.py")

print("\n" + "=" * 80)
print("Need help? Share this diagnostic output!")
print("=" * 80)