"""
Setup script for MySQL database initialization
This script creates the enrollify_db database and imports the SQL schema
"""

import mysql.connector
from mysql.connector import Error
import os
from config import MYSQL_CONFIG


def create_database():
    """Create the enrollify_db database"""
    try:
        # Connect to MySQL without specifying database
        conn = mysql.connector.connect(
            host=MYSQL_CONFIG['host'],
            user=MYSQL_CONFIG['user'],
            password=MYSQL_CONFIG['password']
        )

        cursor = conn.cursor()

        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_CONFIG['database']}")
        print(f"✓ Database '{MYSQL_CONFIG['database']}' created or already exists")

        cursor.close()
        conn.close()

        return True

    except Error as e:
        print(f"✗ Error creating database: {e}")
        return False


def import_sql_dump(sql_file_path):
    """Import SQL dump file into the database"""
    try:
        conn = mysql.connector.connect(
            host=MYSQL_CONFIG['host'],
            user=MYSQL_CONFIG['user'],
            password=MYSQL_CONFIG['password'],
            database=MYSQL_CONFIG['database']
        )

        cursor = conn.cursor()

        # Read and execute SQL file
        with open(sql_file_path, 'r', encoding='utf-8') as sql_file:
            sql_script = sql_file.read()

        # Split by semicolon and execute each statement
        statements = sql_script.split(';')

        for statement in statements:
            statement = statement.strip()
            if statement and not statement.startswith('--') and not statement.startswith('/*'):
                try:
                    cursor.execute(statement)
                except Error as e:
                    # Skip errors for statements that might already exist
                    if "already exists" not in str(e):
                        print(f"Warning: {e}")

        conn.commit()
        print(f"✓ SQL dump imported successfully from {sql_file_path}")

        cursor.close()
        conn.close()

        return True

    except Error as e:
        print(f"✗ Error importing SQL dump: {e}")
        return False
    except FileNotFoundError:
        print(f"✗ SQL file not found: {sql_file_path}")
        return False


def verify_tables():
    """Verify that all required tables exist"""
    try:
        conn = mysql.connector.connect(
            host=MYSQL_CONFIG['host'],
            user=MYSQL_CONFIG['user'],
            password=MYSQL_CONFIG['password'],
            database=MYSQL_CONFIG['database']
        )

        cursor = conn.cursor()

        # Check for required tables
        required_tables = ['students', 'enrollments', 'users']

        cursor.execute("SHOW TABLES")
        existing_tables = [table[0] for table in cursor.fetchall()]

        missing_tables = [t for t in required_tables if t not in existing_tables]

        if missing_tables:
            print(f"✗ Missing tables: {', '.join(missing_tables)}")
            cursor.close()
            conn.close()
            return False
        else:
            print(f"✓ All required tables exist: {', '.join(required_tables)}")

        # Verify table structures
        for table in required_tables:
            cursor.execute(f"DESCRIBE {table}")
            columns = cursor.fetchall()
            print(f"  - {table}: {len(columns)} columns")

        cursor.close()
        conn.close()

        return True

    except Error as e:
        print(f"✗ Error verifying tables: {e}")
        return False


def test_connection():
    """Test MySQL connection"""
    try:
        conn = mysql.connector.connect(
            host=MYSQL_CONFIG['host'],
            user=MYSQL_CONFIG['user'],
            password=MYSQL_CONFIG['password'],
            database=MYSQL_CONFIG['database']
        )

        if conn.is_connected():
            print(f"✓ Successfully connected to MySQL")
            print(f"  Host: {MYSQL_CONFIG['host']}")
            print(f"  User: {MYSQL_CONFIG['user']}")
            print(f"  Database: {MYSQL_CONFIG['database']}")

            conn.close()
            return True

    except Error as e:
        print(f"✗ Connection failed: {e}")
        print(f"  Make sure MySQL is running and credentials are correct")
        return False


def setup_default_users():
    """Create default admin and staff users"""
    try:
        from database_manager_mysql_OLD import get_database

        db = get_database(
            host=MYSQL_CONFIG['host'],
            user=MYSQL_CONFIG['user'],
            password=MYSQL_CONFIG['password'],
            database=MYSQL_CONFIG['database']
        )

        # Check if users already exist
        admin_user = db.get_user_by_username('admin')
        staff_user = db.get_user_by_username('staff')

        if not admin_user:
            db.add_user('admin', 'admin123')
            print("✓ Default admin user created (username: admin, password: admin123)")
        else:
            print("✓ Admin user already exists")

        if not staff_user:
            db.add_user('staff', 'staff123')
            print("✓ Default staff user created (username: staff, password: staff123)")
        else:
            print("✓ Staff user already exists")

        return True

    except Exception as e:
        print(f"✗ Error setting up default users: {e}")
        return False


def main():
    """Main setup function"""
    print("=" * 60)
    print("Enrollify MySQL Database Setup")
    print("=" * 60)

    # Step 1: Test connection
    print("\n[1/4] Testing MySQL connection...")
    if not test_connection():
        print("\nSetup failed. Please check your MySQL configuration in config.py")
        return False

    # Step 2: Create database
    print("\n[2/4] Creating database...")
    if not create_database():
        print("\nSetup failed. Could not create database.")
        return False

    # Step 3: Import SQL dump
    print("\n[3/4] Importing SQL schema...")
    sql_file = os.path.join(os.path.dirname(__file__), 'enrollify_schema.sql')

    if os.path.exists(sql_file):
        if not import_sql_dump(sql_file):
            print("\nWarning: Could not import SQL dump. Tables may need to be created manually.")
    else:
        print(f"Note: SQL dump file not found at {sql_file}")
        print("You can manually import the SQL schema using PhpMyAdmin")

    # Step 4: Verify tables
    print("\n[4/4] Verifying database structure...")
    if not verify_tables():
        print("\nWarning: Some tables may be missing. Please import the SQL schema manually.")
    else:
        print("\n✓ Database structure verified successfully")

    # Step 5: Setup default users
    print("\n[5/5] Setting up default users...")
    setup_default_users()

    print("\n" + "=" * 60)
    print("✓ Setup completed successfully!")
    print("=" * 60)
    print("\nYou can now run the application with: python main.py")

    return True


if __name__ == "__main__":
    main()
