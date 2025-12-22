"""
Setup script to create users with properly hashed passwords
Run this AFTER importing the fixed SQL schema
"""

import mysql.connector
from auth_utils import hash_password


def setup_users():
    """Create admin and staff users with proper password hashing"""

    try:
        # Connect to database
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="",  # Change if you have a password
            database="enrollify_db"
        )

        cursor = connection.cursor()

        # Clear existing users (optional - remove if you want to keep existing users)
        print("Clearing existing users...")
        cursor.execute("DELETE FROM users")
        connection.commit()

        # Create users with hashed passwords
        users = [
            {
                'email': 'admin@enrollify.edu',
                'password': 'admin123',
                'role': 'ADMIN',
                'full_name': 'System Administrator'
            },
            {
                'email': 'staff@enrollify.edu',
                'password': 'staff123',
                'role': 'STAFF',
                'full_name': 'Enrollment Staff'
            }
        ]

        print("\n" + "=" * 60)
        print("Creating users with hashed passwords...")
        print("=" * 60)

        for user in users:
            # Hash the password
            password_hash = hash_password(user['password'])

            # Insert user
            cursor.execute('''
                           INSERT INTO users (email, password_hash, role, full_name, is_active)
                           VALUES (%s, %s, %s, %s, %s)
                           ''', (user['email'], password_hash, user['role'], user['full_name'], True))

            print(f"\n✓ Created {user['role']} user:")
            print(f"  Email: {user['email']}")
            print(f"  Password: {user['password']}")
            print(f"  Hash: {password_hash[:50]}...")

        connection.commit()

        # Verify users were created
        print("\n" + "=" * 60)
        print("Verifying users in database...")
        print("=" * 60)

        cursor.execute("SELECT id, email, role, full_name, is_active FROM users")
        results = cursor.fetchall()

        for row in results:
            print(f"\nUser ID: {row[0]}")
            print(f"  Email: {row[1]}")
            print(f"  Role: {row[2]}")
            print(f"  Name: {row[3]}")
            print(f"  Active: {row[4]}")

        print("\n" + "=" * 60)
        print("✓ Setup complete! You can now login with:")
        print("=" * 60)
        print("\nADMIN LOGIN:")
        print("  Email: admin@enrollify.edu")
        print("  Password: admin123")
        print("\nSTAFF LOGIN:")
        print("  Email: staff@enrollify.edu")
        print("  Password: staff123")
        print("=" * 60 + "\n")

        cursor.close()
        connection.close()

    except mysql.connector.Error as e:
        print(f"\n❌ Database error: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

    return True


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("ENROLLIFY USER SETUP")
    print("=" * 60)

    success = setup_users()

    if not success:
        print("\n❌ Setup failed. Please check the errors above.")
    else:
        print("\n✓ All users created successfully!")