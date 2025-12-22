"""
Create test users for Enrollify
Run this script ONCE to create admin and staff accounts
"""

from database_manager_mysql import get_database


def create_test_users():
    """Create test admin and staff users"""

    print("=" * 60)
    print("Creating Test Users for Enrollify")
    print("=" * 60)

    try:
        # Connect to database
        db = get_database(
            host="127.0.0.1",
            user="root",
            password="",
            database="enrollify_db"
        )

        # Create admin user
        try:
            admin_id = db.add_user(
                email="admin@enrollify.edu",
                password="admin123",  # Min 6 characters
                role="ADMIN",
                full_name="System Administrator"
            )
            print(f"✅ Admin user created (ID: {admin_id})")
            print(f"   Email: admin@enrollify.edu")
            print(f"   Password: admin123")
        except Exception as e:
            if "already exists" in str(e):
                print(f"⚠️  Admin user already exists")
            else:
                print(f"❌ Admin user error: {e}")

        # Create staff user
        try:
            staff_id = db.add_user(
                email="staff@enrollify.edu",
                password="staff123",  # Min 6 characters
                role="STAFF",
                full_name="Staff Member"
            )
            print(f"✅ Staff user created (ID: {staff_id})")
            print(f"   Email: staff@enrollify.edu")
            print(f"   Password: staff123")
        except Exception as e:
            if "already exists" in str(e):
                print(f"⚠️  Staff user already exists")
            else:
                print(f"❌ Staff user error: {e}")

        print("\n" + "=" * 60)
        print("Test users created successfully!")
        print("You can now login with:")
        print("  Admin: admin@enrollify.edu / admin123")
        print("  Staff: staff@enrollify.edu / staff123")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    create_test_users()