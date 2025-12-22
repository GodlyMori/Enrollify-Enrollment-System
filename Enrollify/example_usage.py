"""
Example usage of the MySQL Database Manager for Enrollify
This script demonstrates common database operations
"""

from database_manager_mysql_OLD import get_database, close_database
from config import MYSQL_CONFIG
from datetime import datetime, timedelta


def example_student_operations():
    """Demonstrate student CRUD operations"""
    print("\n" + "="*60)
    print("STUDENT OPERATIONS EXAMPLE")
    print("="*60)

    db = get_database(
        host=MYSQL_CONFIG['host'],
        user=MYSQL_CONFIG['user'],
        password=MYSQL_CONFIG['password'],
        database=MYSQL_CONFIG['database']
    )

    # Example 1: Add a new student
    print("\n[1] Adding a new student...")
    student_data = {
        'lrn': '123456789012',
        'firstname': 'Juan',
        'middlename': 'M',
        'lastname': 'Dela Cruz',
        'gender': 'Male',
        'birthdate': '2005-03-15',
        'email': 'juan.delacruz@example.com',
        'phone': '09123456789',
        'address': '123 Main Street, Manila',
        'grade': 'Grade 11',
        'track': 'Academic',
        'strand': 'STEM',
        'guardian_name': 'Maria Dela Cruz',
        'guardian_contact': '09987654321',
        'status': 'Pending'
    }

    try:
        student_id = db.add_student(student_data)
        print(f"✓ Student added successfully with ID: {student_id}")
    except Exception as e:
        print(f"✗ Error adding student: {e}")
        return

    # Example 2: Get student by LRN
    print("\n[2] Retrieving student by LRN...")
    try:
        student = db.get_student_by_lrn('123456789012')
        if student:
            print(f"✓ Student found:")
            print(f"  Name: {student['firstname']} {student['lastname']}")
            print(f"  Email: {student['email']}")
            print(f"  Grade: {student['grade']}")
            print(f"  Status: {student['status']}")
        else:
            print("✗ Student not found")
    except Exception as e:
        print(f"✗ Error retrieving student: {e}")

    # Example 3: Update student
    print("\n[3] Updating student information...")
    updated_data = student_data.copy()
    updated_data['email'] = 'juan.updated@example.com'
    updated_data['phone'] = '09111111111'

    try:
        db.update_student('123456789012', updated_data)
        print("✓ Student updated successfully")
    except Exception as e:
        print(f"✗ Error updating student: {e}")

    # Example 4: Get all students
    print("\n[4] Retrieving all students...")
    try:
        students = db.get_all_students()
        print(f"✓ Total students in database: {len(students)}")
        for student in students[:3]:  # Show first 3
            print(f"  - {student['firstname']} {student['lastname']} ({student['lrn']})")
    except Exception as e:
        print(f"✗ Error retrieving students: {e}")

    # Example 5: Search students
    print("\n[5] Searching for students...")
    try:
        results = db.search_students('Juan')
        print(f"✓ Found {len(results)} student(s) matching 'Juan'")
        for student in results:
            print(f"  - {student['firstname']} {student['lastname']}")
    except Exception as e:
        print(f"✗ Error searching students: {e}")

    # Example 6: Filter students
    print("\n[6] Filtering students by grade...")
    try:
        results = db.filter_students(grade='Grade 11')
        print(f"✓ Found {len(results)} Grade 11 student(s)")
    except Exception as e:
        print(f"✗ Error filtering students: {e}")


def example_enrollment_operations():
    """Demonstrate enrollment operations"""
    print("\n" + "="*60)
    print("ENROLLMENT OPERATIONS EXAMPLE")
    print("="*60)

    db = get_database(
        host=MYSQL_CONFIG['host'],
        user=MYSQL_CONFIG['user'],
        password=MYSQL_CONFIG['password'],
        database=MYSQL_CONFIG['database']
    )

    # Get a student to work with
    try:
        student = db.get_student_by_lrn('123456789012')
        if not student:
            print("✗ Student not found. Please add a student first.")
            return

        student_id = student['id']

        # Example 1: Add enrollment
        print("\n[1] Adding enrollment record...")
        try:
            enrollment_id = db.add_enrollment(student_id, status='PENDING')
            print(f"✓ Enrollment created with ID: {enrollment_id}")
        except Exception as e:
            print(f"✗ Error adding enrollment: {e}")

        # Example 2: Get enrollment by student ID
        print("\n[2] Retrieving enrollment record...")
        try:
            enrollment = db.get_enrollment_by_student_id(student_id)
            if enrollment:
                print(f"✓ Enrollment found:")
                print(f"  Status: {enrollment['status']}")
                print(f"  Created: {enrollment['created_at']}")
            else:
                print("✗ Enrollment not found")
        except Exception as e:
            print(f"✗ Error retrieving enrollment: {e}")

        # Example 3: Update enrollment status
        print("\n[3] Updating enrollment status...")
        try:
            if enrollment:
                db.update_enrollment_status_by_id(enrollment['id'], 'REQUIREMENTS_SUBMITTED')
                print("✓ Enrollment status updated to REQUIREMENTS_SUBMITTED")
        except Exception as e:
            print(f"✗ Error updating enrollment: {e}")

        # Example 4: Get all enrollments
        print("\n[4] Retrieving all enrollments...")
        try:
            enrollments = db.get_all_enrollments()
            print(f"✓ Total enrollments: {len(enrollments)}")
            for enr in enrollments[:3]:
                print(f"  - {enr['firstname']} {enr['lastname']}: {enr['status']}")
        except Exception as e:
            print(f"✗ Error retrieving enrollments: {e}")

    except Exception as e:
        print(f"✗ Error: {e}")


def example_user_operations():
    """Demonstrate user authentication operations"""
    print("\n" + "="*60)
    print("USER OPERATIONS EXAMPLE")
    print("="*60)

    db = get_database(
        host=MYSQL_CONFIG['host'],
        user=MYSQL_CONFIG['user'],
        password=MYSQL_CONFIG['password'],
        database=MYSQL_CONFIG['database']
    )

    # Example 1: Authenticate user
    print("\n[1] Authenticating user...")
    try:
        user = db.authenticate_user('admin', 'admin123')
        if user:
            print(f"✓ Authentication successful")
            print(f"  Username: {user['username']}")
            print(f"  ID: {user['id']}")
        else:
            print("✗ Authentication failed - invalid credentials")
    except Exception as e:
        print(f"✗ Error authenticating user: {e}")

    # Example 2: Get user by username
    print("\n[2] Retrieving user by username...")
    try:
        user = db.get_user_by_username('admin')
        if user:
            print(f"✓ User found: {user['username']}")
        else:
            print("✗ User not found")
    except Exception as e:
        print(f"✗ Error retrieving user: {e}")

    # Example 3: Add new user
    print("\n[3] Adding new user...")
    try:
        user_id = db.add_user('testuser', 'testpass123')
        print(f"✓ User created with ID: {user_id}")
    except Exception as e:
        print(f"✗ Error adding user: {e}")


def example_statistics():
    """Demonstrate statistics and reporting"""
    print("\n" + "="*60)
    print("STATISTICS & REPORTING EXAMPLE")
    print("="*60)

    db = get_database(
        host=MYSQL_CONFIG['host'],
        user=MYSQL_CONFIG['user'],
        password=MYSQL_CONFIG['password'],
        database=MYSQL_CONFIG['database']
    )

    # Example 1: Get statistics
    print("\n[1] System Statistics...")
    try:
        stats = db.get_statistics()
        print(f"✓ Statistics retrieved:")
        print(f"  Total Students: {stats['total_students']}")
        print(f"  Enrolled: {stats['enrolled']}")
        print(f"  Pending: {stats['pending']}")
        print(f"  Grade 11: {stats['grade11']}")
        print(f"  Grade 12: {stats['grade12']}")
        print(f"  Tracks: {stats['tracks']}")
    except Exception as e:
        print(f"✗ Error retrieving statistics: {e}")

    # Example 2: Count by track
    print("\n[2] Students by Track...")
    try:
        tracks = db.count_by_track()
        print(f"✓ Track distribution:")
        for track, count in tracks.items():
            print(f"  {track}: {count}")
    except Exception as e:
        print(f"✗ Error counting by track: {e}")

    # Example 3: Count by grade
    print("\n[3] Students by Grade...")
    try:
        grades = db.count_by_grade()
        print(f"✓ Grade distribution:")
        for grade, count in grades.items():
            print(f"  {grade}: {count}")
    except Exception as e:
        print(f"✗ Error counting by grade: {e}")

    # Example 4: Count by strand
    print("\n[4] Students by Strand (Top 5)...")
    try:
        strands = db.count_by_strand(top_n=5)
        print(f"✓ Strand distribution:")
        for strand, count in strands.items():
            print(f"  {strand}: {count}")
    except Exception as e:
        print(f"✗ Error counting by strand: {e}")

    # Example 5: Enrollment status counts
    print("\n[5] Enrollment Status Distribution...")
    try:
        statuses = db.count_enrollment_status()
        print(f"✓ Enrollment status distribution:")
        for status, count in statuses.items():
            print(f"  {status}: {count}")
    except Exception as e:
        print(f"✗ Error counting enrollment status: {e}")


def main():
    """Run all examples"""
    print("\n" + "="*60)
    print("ENROLLIFY MYSQL DATABASE MANAGER - USAGE EXAMPLES")
    print("="*60)

    try:
        # Run examples
        example_student_operations()
        example_enrollment_operations()
        example_user_operations()
        example_statistics()

        print("\n" + "="*60)
        print("✓ All examples completed successfully!")
        print("="*60)

    except Exception as e:
        print(f"\n✗ Error: {e}")
    finally:
        # Close database connection
        close_database()
        print("\nDatabase connection closed.")


if __name__ == "__main__":
    main()
