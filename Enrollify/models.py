"""
MODEL LAYER - Handles Data and Database Operations
This is the "what you store" part
"""

from database_manager_mysql import get_database
from datetime import datetime


class Student:
    """
    Student Model - Represents a student and handles student data
    """

    def __init__(self, data=None):
        """Initialize a student with optional data dictionary"""
        if data is None:
            data = {}

        # Student attributes
        self.id = data.get('id')
        self.lrn = data.get('lrn', '')
        self.firstname = data.get('firstname', '')
        self.middlename = data.get('middlename', '')
        self.lastname = data.get('lastname', '')
        self.gender = data.get('gender', '')
        self.birthdate = data.get('birthdate', '')
        self.email = data.get('email', '')
        self.phone = data.get('phone', '')
        self.address = data.get('address', '')
        self.grade = data.get('grade', '')
        self.track = data.get('track', '')
        self.strand = data.get('strand', '')
        self.guardian_name = data.get('guardian_name', '')
        self.guardian_contact = data.get('guardian_contact', '')
        self.status = data.get('status', 'Pending')
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')

    def to_dict(self):
        """Convert student object to dictionary for database storage"""
        return {
            'lrn': self.lrn,
            'firstname': self.firstname,
            'middlename': self.middlename,
            'lastname': self.lastname,
            'gender': self.gender,
            'birthdate': self.birthdate,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'grade': self.grade,
            'track': self.track,
            'strand': self.strand,
            'guardian_name': self.guardian_name,
            'guardian_contact': self.guardian_contact,
            'status': self.status
        }

    def get_full_name(self):
        """Return student's full name"""
        return f"{self.firstname} {self.middlename} {self.lastname}".strip()

    def validate(self):
        """
        Validate student data
        Returns: (is_valid, error_message)
        """
        # Check required fields
        required = {
            'lrn': 'LRN',
            'firstname': 'First Name',
            'lastname': 'Last Name',
            'gender': 'Gender',
            'birthdate': 'Birthdate',
            'email': 'Email',
            'phone': 'Phone',
            'address': 'Address',
            'grade': 'Grade Level',
            'track': 'Track',
            'guardian_name': 'Guardian Name',
            'guardian_contact': 'Guardian Contact'
        }

        for field, label in required.items():
            value = getattr(self, field, '')
            if not value or value.startswith('Select '):
                return False, f"{label} is required"

        # Validate LRN format (12 digits)
        if not self.lrn.isdigit() or len(self.lrn) != 12:
            return False, "LRN must be exactly 12 digits"

        # Track-specific strand validation
        if self.track in ["Academic", "TVL"]:
            if not self.strand or self.strand == "Select strand":
                return False, "Please select or enter a strand for this track"

        return True, ""


class StudentRepository:
    """
    Repository Pattern - Handles all database operations for students
    This keeps database code separate from business logic
    """

    def __init__(self):
        self.db = get_database()

    def save(self, student):
        """
        Save a student to the database
        Returns: student_id if successful, None if failed
        """
        try:
            student_id = self.db.add_student(student.to_dict())
            return student_id
        except Exception as e:
            print(f"Error saving student: {e}")
            raise

    def find_by_lrn(self, lrn):
        """
        Find a student by LRN
        Returns: Student object or None
        """
        try:
            data = self.db.get_student_by_lrn(lrn)
            if data:
                return Student(data)
            return None
        except Exception as e:
            print(f"Error finding student: {e}")
            return None

    def find_all(self):
        """
        Get all students
        Returns: List of Student objects
        """
        try:
            students_data = self.db.get_all_students()
            return [Student(data) for data in students_data]
        except Exception as e:
            print(f"Error getting all students: {e}")
            return []

    def update(self, student):
        """
        Update a student in the database
        Returns: True if successful, False otherwise
        """
        try:
            return self.db.update_student(student.lrn, student.to_dict())
        except Exception as e:
            print(f"Error updating student: {e}")
            raise

    def delete(self, lrn):
        """
        Delete a student by LRN
        Returns: True if successful, False otherwise
        """
        try:
            return self.db.delete_student(lrn)
        except Exception as e:
            print(f"Error deleting student: {e}")
            raise

    def update_status(self, lrn, new_status):
        """
        Update student enrollment status
        Returns: True if successful, False otherwise
        """
        try:
            self.db.update_enrollment_status(lrn, new_status)
            return True
        except Exception as e:
            print(f"Error updating status: {e}")
            raise

    def search(self, query):
        """
        Search students by name or LRN
        Returns: List of Student objects
        """
        try:
            results = self.db.search_students(query)
            return [Student(data) for data in results]
        except Exception as e:
            print(f"Error searching students: {e}")
            return []

    def filter(self, grade=None, track=None, status=None):
        """
        Filter students by criteria
        Returns: List of Student objects
        """
        try:
            results = self.db.filter_students(grade, track, status)
            return [Student(data) for data in results]
        except Exception as e:
            print(f"Error filtering students: {e}")
            return []


class Track:
    """Track Model - Represents an academic track"""

    def __init__(self, name, description=""):
        self.name = name
        self.description = description


class TrackRepository:
    """Repository for Track operations"""

    def __init__(self):
        self.db = get_database()

    def get_all(self):
        """Get all tracks"""
        try:
            return self.db.get_all_tracks()
        except Exception as e:
            print(f"Error getting tracks: {e}")
            return ["Academic", "TVL", "Sports", "Arts & Design"]

    def get_strands_for_track(self, track_name):
        """Get strands for a specific track"""
        try:
            return self.db.get_strands_by_track(track_name)
        except Exception as e:
            print(f"Error getting strands: {e}")
            return []

    def is_valid(self, track_name):
        """Check if track exists"""
        try:
            return self.db.is_valid_track(track_name)
        except Exception as e:
            print(f"Error validating track: {e}")
            return False


class Payment:
    """Payment Model"""

    def __init__(self, student_data, amount, payment_method):
        self.student_data = student_data
        self.amount = amount
        self.payment_method = payment_method
        self.payment_date = datetime.now()


class PaymentRepository:
    """Repository for Payment operations"""

    def __init__(self):
        self.db = get_database()

    def save(self, payment):
        """Save a payment"""
        try:
            payment_data = {
                'student_data': payment.student_data,
                'amount': payment.amount,
                'payment_method': payment.payment_method
            }
            return self.db.add_payment(payment_data)
        except Exception as e:
            print(f"Error saving payment: {e}")
            raise

    def get_by_lrn(self, lrn):
        """Get payments for a student"""
        try:
            return self.db.get_payments_by_lrn(lrn)
        except Exception as e:
            print(f"Error getting payments: {e}")
            return []


class Statistics:
    """Statistics Model"""

    def __init__(self, data):
        self.total_students = data.get('total_students', 0)
        self.enrolled = data.get('enrolled', 0)
        self.pending = data.get('pending', 0)
        self.total_revenue = data.get('total_revenue', 0.0)


class StatisticsRepository:
    """Repository for Statistics"""

    def __init__(self):
        self.db = get_database()

    def get_overview(self):
        """Get overview statistics"""
        try:
            data = self.db.get_statistics()
            return Statistics(data)
        except Exception as e:
            print(f"Error getting statistics: {e}")
            return Statistics({})

    def get_track_distribution(self):
        """Get track distribution"""
        try:
            return self.db.count_by_track()
        except Exception as e:
            print(f"Error getting track distribution: {e}")
            return {}

    def get_grade_distribution(self):
        """Get grade distribution"""
        try:
            return self.db.count_by_grade()
        except Exception as e:
            print(f"Error getting grade distribution: {e}")
            return {}