import mysql.connector
from mysql.connector import Error
from datetime import datetime
import json


class DatabaseManager:
    """Centralized database management for Enrollify system using MySQL"""

    def __init__(self, host="127.0.0.1", user="root", password="", database="enrollify_db"):
        """
        Initialize MySQL database connection
        
        Args:
            host: MySQL server host (default: localhost)
            user: MySQL username (default: root)
            password: MySQL password (default: empty)
            database: Database name (default: enrollify_db)
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.connect()

    def connect(self):
        """Establish connection to MySQL database"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                autocommit=False,
                use_pure=True
            )
            if self.connection.is_connected():
                pass  # Silent connection
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            raise

    def get_connection(self):
        """Get or create database connection"""
        try:
            if self.connection is None or not self.connection.is_connected():
                self.connect()
            return self.connection
        except Error as e:
            print(f"Connection error: {e}")
            raise

    def close_connection(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection closed")

    def init_database(self):
        """Initialize all required tables (tables should already exist from SQL dump)"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # Verify tables exist
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            table_names = [table[0] for table in tables]

            required_tables = ['students', 'enrollments', 'users']
            missing_tables = [t for t in required_tables if t not in table_names]

            if missing_tables:
                print(f"Warning: Missing tables: {missing_tables}")
                print("Please import the SQL dump to create the required tables")
            else:
                print("All required tables exist")

            cursor.close()
        except Error as e:
            print(f"Error initializing database: {e}")
            raise

    # ==================== STUDENT OPERATIONS ====================

    def add_student(self, student_data):
        """Add new student to database"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            query = '''
                INSERT INTO students 
                (lrn, firstname, middlename, lastname, gender, birthdate, 
                 email, phone, address, grade, track, strand, 
                 guardian_name, guardian_contact, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''

            values = (
                student_data['lrn'],
                student_data['firstname'],
                student_data.get('middlename', ''),
                student_data['lastname'],
                student_data['gender'],
                student_data['birthdate'],
                student_data['email'],
                student_data['phone'],
                student_data['address'],
                student_data['grade'],
                student_data['track'],
                student_data.get('strand', ''),
                student_data['guardian_name'],
                student_data['guardian_contact'],
                student_data.get('status', 'Pending')
            )

            cursor.execute(query, values)
            conn.commit()
            student_id = cursor.lastrowid

            cursor.close()
            self.log_action(None, 'ADD_STUDENT', f"Added student: {student_data['lrn']}")

            return student_id

        except Error as e:
            if "Duplicate entry" in str(e):
                raise Exception(f"Student with LRN {student_data['lrn']} already exists")
            raise Exception(f"Error adding student: {e}")

    def get_student_by_lrn(self, lrn):
        """Get student by LRN"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute('SELECT * FROM students WHERE lrn = %s', (lrn,))
            result = cursor.fetchone()

            cursor.close()
            return result

        except Error as e:
            raise Exception(f"Error retrieving student: {e}")

    def get_all_students(self):
        """Get all students"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute('SELECT * FROM students ORDER BY created_at DESC')
            results = cursor.fetchall()

            cursor.close()
            return results

        except Error as e:
            raise Exception(f"Error retrieving students: {e}")

    def update_student(self, lrn, student_data):
        """Update student information"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            query = '''
                UPDATE students SET
                    firstname = %s,
                    middlename = %s,
                    lastname = %s,
                    gender = %s,
                    birthdate = %s,
                    email = %s,
                    phone = %s,
                    address = %s,
                    grade = %s,
                    track = %s,
                    strand = %s,
                    guardian_name = %s,
                    guardian_contact = %s
                WHERE lrn = %s
            '''

            values = (
                student_data['firstname'],
                student_data.get('middlename', ''),
                student_data['lastname'],
                student_data['gender'],
                student_data['birthdate'],
                student_data['email'],
                student_data['phone'],
                student_data['address'],
                student_data['grade'],
                student_data['track'],
                student_data.get('strand', ''),
                student_data['guardian_name'],
                student_data['guardian_contact'],
                lrn
            )

            cursor.execute(query, values)
            conn.commit()

            cursor.close()
            self.log_action(None, 'UPDATE_STUDENT', f"Updated student: {lrn}")

            return True

        except Error as e:
            conn.rollback()
            raise Exception(f"Error updating student: {e}")

    def delete_student(self, lrn):
        """Delete student"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # Delete related enrollments first (foreign key constraint)
            cursor.execute('DELETE FROM enrollments WHERE student_id = (SELECT id FROM students WHERE lrn = %s)', (lrn,))

            # Delete student
            cursor.execute('DELETE FROM students WHERE lrn = %s', (lrn,))

            conn.commit()
            cursor.close()

            self.log_action(None, 'DELETE_STUDENT', f"Deleted student: {lrn}")

            return True

        except Error as e:
            conn.rollback()
            raise Exception(f"Error deleting student: {e}")

    def update_enrollment_status(self, lrn, status):
        """Update student enrollment status"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                UPDATE students SET 
                    status = %s
                WHERE lrn = %s
            ''', (status, lrn))

            conn.commit()
            cursor.close()

            self.log_action(None, 'UPDATE_STATUS', f"Changed status for {lrn} to {status}")

        except Error as e:
            conn.rollback()
            raise Exception(f"Error updating enrollment status: {e}")

    # ==================== ENROLLMENT OPERATIONS ====================

    def add_enrollment(self, student_id, status='PENDING'):
        """Add enrollment record for a student"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            query = '''
                INSERT INTO enrollments (student_id, status)
                VALUES (%s, %s)
            '''

            cursor.execute(query, (student_id, status))
            conn.commit()
            enrollment_id = cursor.lastrowid

            cursor.close()
            self.log_action(None, 'ADD_ENROLLMENT', f"Added enrollment for student_id: {student_id}")

            return enrollment_id

        except Error as e:
            conn.rollback()
            raise Exception(f"Error adding enrollment: {e}")

    def get_enrollment_by_student_id(self, student_id):
        """Get enrollment record by student ID"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute('SELECT * FROM enrollments WHERE student_id = %s', (student_id,))
            result = cursor.fetchone()

            cursor.close()
            return result

        except Error as e:
            raise Exception(f"Error retrieving enrollment: {e}")

    def update_enrollment_status_by_id(self, enrollment_id, status):
        """Update enrollment status by enrollment ID"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                UPDATE enrollments SET 
                    status = %s
                WHERE id = %s
            ''', (status, enrollment_id))

            conn.commit()
            cursor.close()

            self.log_action(None, 'UPDATE_ENROLLMENT', f"Updated enrollment {enrollment_id} to {status}")

        except Error as e:
            conn.rollback()
            raise Exception(f"Error updating enrollment: {e}")

    def get_all_enrollments(self):
        """Get all enrollments"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute('''
                SELECT e.*, s.lrn, s.firstname, s.lastname, s.email 
                FROM enrollments e
                JOIN students s ON e.student_id = s.id
                ORDER BY e.created_at DESC
            ''')
            results = cursor.fetchall()

            cursor.close()
            return results

        except Error as e:
            raise Exception(f"Error retrieving enrollments: {e}")

    # ==================== USER OPERATIONS ====================

    def authenticate_user(self, username, password):
        """Authenticate user login"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute('''
                SELECT id, username 
                FROM users 
                WHERE username = %s AND password = %s
            ''', (username, password))

            result = cursor.fetchone()
            cursor.close()

            if result:
                self.log_action(username, 'LOGIN', f"User logged in")
                return result
            return None

        except Error as e:
            raise Exception(f"Error authenticating user: {e}")

    def add_user(self, username, password):
        """Add new user"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            query = '''
                INSERT INTO users (username, password)
                VALUES (%s, %s)
            '''

            cursor.execute(query, (username, password))
            conn.commit()
            user_id = cursor.lastrowid

            cursor.close()
            self.log_action(None, 'ADD_USER', f"Added user: {username}")

            return user_id

        except Error as e:
            conn.rollback()
            if "Duplicate entry" in str(e):
                raise Exception(f"User with username {username} already exists")
            raise Exception(f"Error adding user: {e}")

    def get_user_by_username(self, username):
        """Get user by username"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
            result = cursor.fetchone()

            cursor.close()
            return result

        except Error as e:
            raise Exception(f"Error retrieving user: {e}")

    # ==================== REPORT HELPERS ====================

    def count_enrollment_status(self):
        """Return counts grouped by enrollment status"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                SELECT status, COUNT(*) FROM enrollments
                GROUP BY status
            ''')
            rows = cursor.fetchall()
            cursor.close()

            return {row[0] if row[0] else 'Unknown': row[1] for row in rows}

        except Error as e:
            raise Exception(f"Error counting enrollment status: {e}")

    def count_by_track(self):
        """Return dict mapping track -> count"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                SELECT track, COUNT(*) FROM students
                GROUP BY track
            ''')
            rows = cursor.fetchall()
            cursor.close()

            return {row[0] if row[0] else 'Unspecified': row[1] for row in rows}

        except Error as e:
            raise Exception(f"Error counting by track: {e}")

    def count_by_grade(self):
        """Return dict mapping grade -> count"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                SELECT grade, COUNT(*) FROM students
                GROUP BY grade
            ''')
            rows = cursor.fetchall()
            cursor.close()

            return {row[0] if row[0] else 'Unspecified': row[1] for row in rows}

        except Error as e:
            raise Exception(f"Error counting by grade: {e}")

    def count_by_strand(self, top_n=None):
        """
        Return dict mapping strand -> count.
        If top_n provided, returns top_n most common strands.
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            query = 'SELECT strand, COUNT(*) as c FROM students GROUP BY strand ORDER BY c DESC'
            if top_n:
                query += f' LIMIT {int(top_n)}'

            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()

            return {row[0] if row[0] else 'Unspecified': row[1] for row in rows}

        except Error as e:
            raise Exception(f"Error counting by strand: {e}")

    def get_all_strands(self):
        """Return list of distinct strands"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('SELECT DISTINCT strand FROM students WHERE strand IS NOT NULL AND strand != ""')
            rows = cursor.fetchall()
            cursor.close()

            return [r[0] for r in rows]

        except Error as e:
            raise Exception(f"Error retrieving strands: {e}")

    # ==================== STATISTICS ====================

    def get_statistics(self):
        """Get system statistics"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # Total students
            cursor.execute('SELECT COUNT(*) FROM students')
            total_students = cursor.fetchone()[0]

            # Enrolled students
            cursor.execute("SELECT COUNT(*) FROM students WHERE status = 'Enrolled'")
            enrolled = cursor.fetchone()[0]

            # Pending students
            cursor.execute("SELECT COUNT(*) FROM students WHERE status = 'Pending'")
            pending = cursor.fetchone()[0]

            # Grade 11
            cursor.execute("SELECT COUNT(*) FROM students WHERE grade = 'Grade 11'")
            grade11 = cursor.fetchone()[0]

            # Grade 12
            cursor.execute("SELECT COUNT(*) FROM students WHERE grade = 'Grade 12'")
            grade12 = cursor.fetchone()[0]

            # By track
            cursor.execute('SELECT track, COUNT(*) FROM students GROUP BY track')
            tracks = dict(cursor.fetchall())

            # Enrollment status counts
            cursor.execute('SELECT status, COUNT(*) FROM enrollments GROUP BY status')
            enrollment_statuses = dict(cursor.fetchall())

            cursor.close()

            return {
                'total_students': total_students,
                'enrolled': enrolled,
                'pending': pending,
                'grade11': grade11,
                'grade12': grade12,
                'tracks': tracks,
                'enrollment_statuses': enrollment_statuses
            }

        except Error as e:
            raise Exception(f"Error retrieving statistics: {e}")

    # ==================== AUDIT LOG ====================

    def log_action(self, user, action, details):
        """Log system action"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            query = '''
                INSERT INTO audit_log (user, action, details, timestamp)
                VALUES (%s, %s, %s, NOW())
            '''

            cursor.execute(query, (user, action, details))
            conn.commit()
            cursor.close()

        except Error as e:
            print(f"Error logging action: {e}")

    # ==================== SEARCH & FILTER ====================

    def search_students(self, query):
        """Search students by name or LRN"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)

            search_query = f"%{query}%"
            cursor.execute('''
                SELECT * FROM students 
                WHERE lrn LIKE %s OR firstname LIKE %s OR lastname LIKE %s
                ORDER BY created_at DESC
            ''', (search_query, search_query, search_query))

            results = cursor.fetchall()
            cursor.close()

            return results

        except Error as e:
            raise Exception(f"Error searching students: {e}")

    def filter_students(self, grade=None, track=None, status=None):
        """Filter students by criteria"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)

            query = 'SELECT * FROM students WHERE 1=1'
            params = []

            if grade:
                query += ' AND grade = %s'
                params.append(grade)

            if track:
                query += ' AND track = %s'
                params.append(track)

            if status:
                query += ' AND status = %s'
                params.append(status)

            query += ' ORDER BY created_at DESC'

            cursor.execute(query, params)
            results = cursor.fetchall()
            cursor.close()

            return results

        except Error as e:
            raise Exception(f"Error filtering students: {e}")


# Singleton instance
_db_instance = None


def get_database(host="127.0.0.1", user="root", password="", database="enrollify_db"):
    """Get database manager singleton instance"""
    global _db_instance
    if _db_instance is None:
        _db_instance = DatabaseManager(host=host, user=user, password=password, database=database)
    return _db_instance


def close_database():
    """Close database connection"""
    global _db_instance
    if _db_instance is not None:
        _db_instance.close_connection()
        _db_instance = None
