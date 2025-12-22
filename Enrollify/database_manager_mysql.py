import mysql.connector
from mysql.connector import Error
from datetime import datetime


class DatabaseManager:
    """MySQL Database Manager for Enrollify - Updated for new schema"""

    def __init__(self, host="127.0.0.1", user="root", password="", database="enrollify_db"):
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
                print(f"✅ Connected to MySQL database: {self.database}")
        except Error as e:
            print(f"❌ MySQL connection error: {e}")
            raise

    def get_connection(self):
        """Get or reconnect to database"""
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

    # ==================== TRACK OPERATIONS ====================

    def get_all_tracks(self):
        """Get all available tracks"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT name FROM tracks ORDER BY name')
            tracks = [row[0] for row in cursor.fetchall()]
            cursor.close()
            return tracks
        except Error as e:
            print(f"Error fetching tracks: {e}")
            return []

    def add_track(self, name, description=""):
        """Add new track"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO tracks (name, description) VALUES (%s, %s)', (name, description))
            conn.commit()
            cursor.close()
            self.log_action(None, 'ADD_TRACK', f"Added track: {name}")
        except Error as e:
            conn.rollback()
            if "Duplicate entry" in str(e):
                raise ValueError(f"Track '{name}' already exists")
            raise e

    def remove_track(self, name):
        """Remove track (only if no students use it)"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # Check if any student uses this track
            cursor.execute('SELECT COUNT(*) FROM students WHERE track = %s', (name,))
            if cursor.fetchone()[0] > 0:
                cursor.close()
                raise ValueError("Cannot delete track in use by students")

            cursor.execute('DELETE FROM tracks WHERE name = %s', (name,))
            conn.commit()
            cursor.close()
            self.log_action(None, 'REMOVE_TRACK', f"Removed track: {name}")
        except Error as e:
            conn.rollback()
            raise e

    def is_valid_track(self, track_name):
        """Check if track exists"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT 1 FROM tracks WHERE name = %s', (track_name,))
            exists = cursor.fetchone() is not None
            cursor.close()
            return exists
        except Error as e:
            print(f"Error checking track: {e}")
            return False

    def get_strands_by_track(self, track_name):
        """Get strands for a specific track"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT name FROM strands WHERE track = %s ORDER BY name', (track_name,))
            strands = [row[0] for row in cursor.fetchall()]
            cursor.close()
            return strands
        except Error as e:
            print(f"Error fetching strands: {e}")
            return []

    def get_all_strands(self):
        """Get all strands"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT DISTINCT name FROM strands ORDER BY name')
            strands = [row[0] for row in cursor.fetchall()]
            cursor.close()
            return strands
        except Error as e:
            print(f"Error fetching strands: {e}")
            return []

    # ==================== TUITION FEE OPERATIONS ====================

    def get_tuition_fees(self, track, strand=None):
        """Get tuition fee breakdown for a track/strand"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)

            if strand is None or strand.strip() == "":
                cursor.execute('''
                    SELECT enrollment_fee, miscellaneous_fee, tuition_fee, special_fee
                    FROM tuition_fees
                    WHERE track = %s AND strand IS NULL
                ''', (track,))
            else:
                cursor.execute('''
                    SELECT enrollment_fee, miscellaneous_fee, tuition_fee, special_fee
                    FROM tuition_fees
                    WHERE track = %s AND strand = %s
                ''', (track, strand))

            result = cursor.fetchone()
            cursor.close()

            if result:
                return {
                    'enrollment_fee': float(result['enrollment_fee']),
                    'miscellaneous_fee': float(result['miscellaneous_fee']),
                    'tuition_fee': float(result['tuition_fee']),
                    'special_fee': float(result['special_fee']),
                    'total': float(result['enrollment_fee'] + result['miscellaneous_fee'] +
                                 result['tuition_fee'] + result['special_fee'])
                }
            else:
                # Fallback default fees
                return {
                    'enrollment_fee': 5000,
                    'miscellaneous_fee': 4500,
                    'tuition_fee': 15000,
                    'special_fee': 2000,
                    'total': 26500
                }
        except Error as e:
            print(f"Error fetching tuition fees: {e}")
            return {
                'enrollment_fee': 5000,
                'miscellaneous_fee': 4500,
                'tuition_fee': 15000,
                'special_fee': 2000,
                'total': 26500
            }

    # ==================== STUDENT OPERATIONS ====================

    def add_student(self, student_data):
        """Add new student to database - USES NEW COLUMN NAMES"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            query = '''
                INSERT INTO students 
                (lrn, firstname, middlename, lastname, gender, birthdate, 
                 email, phone, address, grade_level, track, strand, 
                 guardian_name, guardian_contact, enrollment_status)
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
                student_data['grade'],  # Maps to grade_level in DB
                student_data['track'],
                student_data.get('strand', ''),
                student_data['guardian_name'],
                student_data['guardian_contact'],
                student_data.get('status', 'Pending')  # Maps to enrollment_status in DB
            )

            cursor.execute(query, values)
            conn.commit()
            student_id = cursor.lastrowid
            cursor.close()

            self.log_action(None, 'ADD_STUDENT', f"Added student: {student_data['lrn']}")
            return student_id

        except Error as e:
            conn.rollback()
            if "Duplicate entry" in str(e):
                raise Exception(f"Student with LRN {student_data['lrn']} already exists")
            raise Exception(f"Error adding student: {e}")

    def get_student_by_lrn(self, lrn):
        """Get student by LRN - RETURNS WITH UI-FRIENDLY ALIASES"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute('''
                SELECT 
                    id, lrn, firstname, middlename, lastname, gender, birthdate,
                    email, phone, address, 
                    grade_level AS grade,
                    track, strand,
                    guardian_name, guardian_contact, 
                    enrollment_status AS status,
                    created_at, updated_at
                FROM students 
                WHERE lrn = %s
            ''', (lrn,))

            result = cursor.fetchone()
            cursor.close()
            return result

        except Error as e:
            print(f"Error retrieving student: {e}")
            return None

    def get_all_students(self):
        """Get all students - RETURNS WITH UI-FRIENDLY ALIASES"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute('''
                SELECT 
                    id, lrn, firstname, middlename, lastname, gender, birthdate,
                    email, phone, address, 
                    grade_level AS grade,
                    track, strand,
                    guardian_name, guardian_contact, 
                    enrollment_status AS status,
                    created_at, updated_at
                FROM students 
                ORDER BY created_at DESC
            ''')

            results = cursor.fetchall()
            cursor.close()
            return results

        except Error as e:
            print(f"Error retrieving students: {e}")
            return []

    def update_student(self, lrn, student_data):
        """Update student information - USES NEW COLUMN NAMES"""
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
                    grade_level = %s,
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
        """Delete student and related payments"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # Get student_id first
            cursor.execute('SELECT id FROM students WHERE lrn = %s', (lrn,))
            result = cursor.fetchone()

            if result:
                student_id = result[0]
                # Delete payments (CASCADE should handle this, but being explicit)
                cursor.execute('DELETE FROM payments WHERE student_id = %s', (student_id,))
                # Delete student
                cursor.execute('DELETE FROM students WHERE lrn = %s', (lrn,))
                conn.commit()

                self.log_action(None, 'DELETE_STUDENT', f"Deleted student: {lrn}")
                cursor.close()
                return True

            cursor.close()
            return False

        except Error as e:
            conn.rollback()
            raise Exception(f"Error deleting student: {e}")

    def update_enrollment_status(self, lrn, status):
        """Update student enrollment status - USES NEW COLUMN NAME"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                UPDATE students SET 
                    enrollment_status = %s
                WHERE lrn = %s
            ''', (status, lrn))

            conn.commit()
            cursor.close()
            self.log_action(None, 'UPDATE_STATUS', f"Changed status for {lrn} to {status}")

        except Error as e:
            conn.rollback()
            raise Exception(f"Error updating enrollment status: {e}")

    # ==================== PAYMENT OPERATIONS ====================

    def add_payment(self, payment_data):
        """Record payment"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # Get student ID
            cursor.execute('SELECT id FROM students WHERE lrn = %s',
                         (payment_data['student_data']['lrn'],))
            result = cursor.fetchone()

            if not result:
                cursor.close()
                raise Exception("Student not found")

            student_id = result[0]

            # Insert payment
            cursor.execute('''
                INSERT INTO payments 
                (student_id, lrn, amount, payment_method)
                VALUES (%s, %s, %s, %s)
            ''', (
                student_id,
                payment_data['student_data']['lrn'],
                payment_data['amount'],
                payment_data['payment_method']
            ))

            # Update enrollment status to Enrolled
            cursor.execute('''
                UPDATE students SET enrollment_status = 'Enrolled'
                WHERE lrn = %s
            ''', (payment_data['student_data']['lrn'],))

            conn.commit()
            payment_id = cursor.lastrowid
            cursor.close()

            self.log_action(None, 'ADD_PAYMENT',
                          f"Payment received for LRN: {payment_data['student_data']['lrn']}")
            return payment_id

        except Error as e:
            conn.rollback()
            raise Exception(f"Error adding payment: {e}")

    def get_payments_by_lrn(self, lrn):
        """Get all payments for a student"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute('''
                SELECT * FROM payments 
                WHERE lrn = %s 
                ORDER BY payment_date DESC
            ''', (lrn,))

            results = cursor.fetchall()
            cursor.close()
            return results

        except Error as e:
            print(f"Error retrieving payments: {e}")
            return []

    # ==================== USER OPERATIONS ====================

    def authenticate_user(self, email, password):
        """Authenticate user login - FIXED"""
        try:
            from auth_utils import verify_password

            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)

            # Get user with password_hash
            cursor.execute('''
                           SELECT id, email, role, full_name, password_hash
                           FROM users
                           WHERE email = %s
                             AND is_active = TRUE
                           ''', (email,))

            result = cursor.fetchone()
            cursor.close()

            if result:
                # Verify password
                if verify_password(password, result['password_hash']):
                    # Remove hash from result
                    user_data = {
                        'id': result['id'],
                        'email': result['email'],
                        'role': result['role'],
                        'full_name': result['full_name']
                    }

                    # Update last login
                    try:
                        conn2 = self.get_connection()
                        cursor2 = conn2.cursor()
                        cursor2.execute('''
                                        UPDATE users
                                        SET last_login = CURRENT_TIMESTAMP
                                        WHERE id = %s
                                        ''', (result['id'],))
                        conn2.commit()
                        cursor2.close()
                    except:
                        pass

                    # ✅ FIXED: Removed extra parameter from log_action
                    self.log_action(email, 'LOGIN', f"{result['role']} logged in")
                    return user_data
                else:
                    # ✅ FIXED: Removed extra parameter
                    self.log_action(email, 'LOGIN_FAILED', 'Invalid password')
                    return None
            else:
                # ✅ FIXED: Removed extra parameter
                self.log_action(email, 'LOGIN_FAILED', 'User not found')
                return None

        except Exception as e:
            print(f"Error authenticating user: {e}")
            import traceback
            traceback.print_exc()
            return None

    def add_user(self, email, password, role, full_name):
        """Add new user - WITH PASSWORD HASHING"""
        try:
            from auth_utils import hash_password

            conn = self.get_connection()
            cursor = conn.cursor()

            # Hash the password
            password_hash = hash_password(password)

            cursor.execute('''
                           INSERT INTO users (email, password_hash, role, full_name)
                           VALUES (%s, %s, %s, %s)
                           ''', (email, password_hash, role, full_name))

            conn.commit()
            user_id = cursor.lastrowid
            cursor.close()

            self.log_action(None, 'ADD_USER', 'CREATE', f"Added user: {email}")
            return user_id

        except Error as e:
            conn.rollback()
            if "Duplicate entry" in str(e):
                raise Exception(f"User with email {email} already exists")
            raise Exception(f"Error adding user: {e}")

    # ==================== ANALYTICS & STATISTICS ====================

    def get_statistics(self):
        """Get key system statistics - USES NEW COLUMN NAMES"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # Total students
            cursor.execute('SELECT COUNT(*) FROM students')
            total_students = cursor.fetchone()[0]

            # Enrolled students
            cursor.execute("SELECT COUNT(*) FROM students WHERE enrollment_status = 'Enrolled'")
            enrolled = cursor.fetchone()[0]

            # Pending students
            cursor.execute("SELECT COUNT(*) FROM students WHERE enrollment_status = 'Pending'")
            pending = cursor.fetchone()[0]

            # Total revenue
            cursor.execute('SELECT SUM(amount) FROM payments')
            total_revenue = cursor.fetchone()[0] or 0.0

            cursor.close()

            return {
                'total_students': total_students,
                'enrolled': enrolled,
                'pending': pending,
                'total_revenue': float(total_revenue)
            }

        except Error as e:
            print(f"Error retrieving statistics: {e}")
            return {
                'total_students': 0,
                'enrolled': 0,
                'pending': 0,
                'total_revenue': 0.0
            }

    def get_gender_distribution(self):
        """Return list of (gender, count)"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                SELECT gender, COUNT(*) 
                FROM students 
                WHERE gender IS NOT NULL AND TRIM(gender) != ''
                GROUP BY gender
            ''')

            results = cursor.fetchall()
            cursor.close()
            return [(row[0], row[1]) for row in results]

        except Error as e:
            print(f"Error getting gender distribution: {e}")
            return []

    def count_by_track(self):
        """Return dict {track: count}"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('SELECT track, COUNT(*) FROM students GROUP BY track')
            result = dict(cursor.fetchall())
            cursor.close()
            return result

        except Error as e:
            print(f"Error counting by track: {e}")
            return {}

    def count_by_grade(self):
        """Return dict {grade: count} - USES NEW COLUMN NAME"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                SELECT grade_level, COUNT(*) 
                FROM students 
                GROUP BY grade_level
                ORDER BY grade_level
            ''')

            result = dict(cursor.fetchall())
            cursor.close()
            return result

        except Error as e:
            print(f"Error counting by grade: {e}")
            return {}

    def count_by_strand(self, top_n=None):
        """Return dict {strand: count}"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            query = '''
                SELECT strand, COUNT(*) as c 
                FROM students 
                WHERE strand IS NOT NULL AND strand != ''
                GROUP BY strand 
                ORDER BY c DESC
            '''

            if top_n:
                query += f' LIMIT {int(top_n)}'

            cursor.execute(query)
            result = dict(cursor.fetchall())
            cursor.close()
            return result or {"Unspecified": 0}

        except Error as e:
            print(f"Error counting by strand: {e}")
            return {"Unspecified": 0}

    def count_enrollment_status(self):
        """Return dict {status: count} - USES NEW COLUMN NAME"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                SELECT enrollment_status, COUNT(*) 
                FROM students
                GROUP BY enrollment_status
            ''')

            result = dict(cursor.fetchall())
            cursor.close()
            return result

        except Error as e:
            print(f"Error counting enrollment status: {e}")
            return {}

    def get_grade_distribution(self):
        """Return list of (grade_level, count) - USES NEW COLUMN NAME"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                SELECT grade_level, COUNT(*) 
                FROM students 
                GROUP BY grade_level
                ORDER BY grade_level
            ''')

            results = cursor.fetchall()
            cursor.close()
            return [(row[0], row[1]) for row in results]

        except Error as e:
            print(f"Error getting grade distribution: {e}")
            return []

    def get_enrollment_status_distribution(self):
        """Return list of (status, count) - USES NEW COLUMN NAME"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                SELECT enrollment_status, COUNT(*) 
                FROM students 
                GROUP BY enrollment_status
            ''')

            results = cursor.fetchall()
            cursor.close()
            return [(row[0], row[1]) for row in results]

        except Error as e:
            print(f"Error getting enrollment status distribution: {e}")
            return []

    # ==================== AUDIT LOG ====================

    # If your audit_log table uses 'user_email' instead of 'user',
    # replace the log_action method in database_manager_mysql.py with this:

    def log_action(self, user_email, action, details):
        """
        Log system action - Uses user_email column
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                           INSERT INTO audit_log (user_email, action, details)
                           VALUES (%s, %s, %s)
                           ''', (user_email, action, details))

            conn.commit()
            cursor.close()

        except Error as e:
            print(f"Error logging action: {e}")

    def get_audit_log(self, limit=100):
        """Get audit log entries - Uses user_email column"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute('''
                           SELECT id, user_email AS user, action, details, timestamp
                           FROM audit_log
                           ORDER BY timestamp DESC
                               LIMIT %s
                           ''', (limit,))

            results = cursor.fetchall()
            cursor.close()
            return results

        except Error as e:
            print(f"Error retrieving audit log: {e}")
            return []
    # ==================== SEARCH & FILTER ====================

    def search_students(self, query):
        """Search students by name or LRN - USES NEW COLUMN NAMES"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)

            search_query = f"%{query}%"
            cursor.execute('''
                SELECT 
                    id, lrn, firstname, middlename, lastname, gender, birthdate,
                    email, phone, address, 
                    grade_level AS grade,
                    track, strand,
                    guardian_name, guardian_contact, 
                    enrollment_status AS status,
                    created_at, updated_at
                FROM students 
                WHERE lrn LIKE %s OR firstname LIKE %s OR lastname LIKE %s
                ORDER BY created_at DESC
            ''', (search_query, search_query, search_query))

            results = cursor.fetchall()
            cursor.close()
            return results

        except Error as e:
            print(f"Error searching students: {e}")
            return []

    def filter_students(self, grade=None, track=None, status=None):
        """Filter students by criteria - USES NEW COLUMN NAMES"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)

            query = '''
                SELECT 
                    id, lrn, firstname, middlename, lastname, gender, birthdate,
                    email, phone, address, 
                    grade_level AS grade,
                    track, strand,
                    guardian_name, guardian_contact, 
                    enrollment_status AS status,
                    created_at, updated_at
                FROM students 
                WHERE 1=1
            '''
            params = []

            if grade:
                query += ' AND grade_level = %s'
                params.append(grade)

            if track:
                query += ' AND track = %s'
                params.append(track)

            if status:
                query += ' AND enrollment_status = %s'
                params.append(status)

            query += ' ORDER BY created_at DESC'

            cursor.execute(query, params)
            results = cursor.fetchall()
            cursor.close()
            return results

        except Error as e:
            print(f"Error filtering students: {e}")
            return []

def add_payment_with_receipt(self, payment_data, receipt_number):
    """Record payment with receipt number"""
    try:
        conn = self.get_connection()
        cursor = conn.cursor()

        # Get student ID
        cursor.execute('SELECT id FROM students WHERE lrn = %s',
                       (payment_data['student_data']['lrn'],))
        result = cursor.fetchone()

        if not result:
            cursor.close()
            raise Exception("Student not found")

        student_id = result[0]

        # Check if receipt_number column exists, if not add it
        try:
            cursor.execute('''
                           ALTER TABLE payments
                               ADD COLUMN receipt_number VARCHAR(50) NULL AFTER payment_method
                           ''')
            conn.commit()
            print("✅ Added receipt_number column to payments table")
        except:
            pass  # Column already exists

        # Insert payment with receipt number
        cursor.execute('''
                       INSERT INTO payments
                           (student_id, lrn, amount, payment_method, receipt_number)
                       VALUES (%s, %s, %s, %s, %s)
                       ''', (
                           student_id,
                           payment_data['student_data']['lrn'],
                           payment_data['amount'],
                           payment_data['payment_method'],
                           receipt_number
                       ))

        # Update enrollment status to Enrolled
        cursor.execute('''
                       UPDATE students
                       SET enrollment_status = 'Enrolled'
                       WHERE lrn = %s
                       ''', (payment_data['student_data']['lrn'],))

        conn.commit()
        payment_id = cursor.lastrowid
        cursor.close()

        self.log_action(None, 'ADD_PAYMENT',
                        f"Payment received for LRN: {payment_data['student_data']['lrn']}, Receipt: {receipt_number}")
        return payment_id

    except Exception as e:
        conn.rollback()
        raise Exception(f"Error adding payment: {e}")


def get_receipt_by_number(self, receipt_number):
    """Get payment details by receipt number"""
    try:
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute('''
                       SELECT p.*,
                              s.firstname,
                              s.middlename,
                              s.lastname,
                              s.lrn,
                              s.grade_level AS grade,
                              s.track,
                              s.strand,
                              s.email,
                              s.phone
                       FROM payments p
                                JOIN students s ON p.student_id = s.id
                       WHERE p.receipt_number = %s
                       ''', (receipt_number,))

        result = cursor.fetchone()
        cursor.close()
        return result

    except Exception as e:
        print(f"Error retrieving receipt: {e}")
        return None


def get_all_receipts(self, limit=100):
    """Get all payment receipts"""
    try:
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute('''
                       SELECT p.receipt_number,
                              p.amount,
                              p.payment_method,
                              p.payment_date,
                              s.firstname,
                              s.lastname,
                              s.lrn
                       FROM payments p
                                JOIN students s ON p.student_id = s.id
                       WHERE p.receipt_number IS NOT NULL
                       ORDER BY p.payment_date DESC
                           LIMIT %s
                       ''', (limit,))

        results = cursor.fetchall()
        cursor.close()
        return results

    except Exception as e:
        print(f"Error retrieving receipts: {e}")
        return []


def search_receipt(self, search_query):
    """Search receipts by receipt number, LRN, or student name"""
    try:
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)

        search_pattern = f"%{search_query}%"

        cursor.execute('''
                       SELECT p.receipt_number,
                              p.amount,
                              p.payment_method,
                              p.payment_date,
                              s.firstname,
                              s.lastname,
                              s.lrn,
                              s.grade_level AS grade,
                              s.track
                       FROM payments p
                                JOIN students s ON p.student_id = s.id
                       WHERE p.receipt_number LIKE %s
                          OR s.lrn LIKE %s
                          OR s.firstname LIKE %s
                          OR s.lastname LIKE %s
                       ORDER BY p.payment_date DESC LIMIT 50
                       ''', (search_pattern, search_pattern, search_pattern, search_pattern))

        results = cursor.fetchall()
        cursor.close()
        return results

    except Exception as e:
        print(f"Error searching receipts: {e}")
        return []

# ==================== SINGLETON INSTANCE ====================

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


# ============================================
# ADD THESE METHODS TO database_manager_mysql.py
# Paste at the end of the DatabaseManager class
# ============================================

# ==================== STAFF ASSIGNMENT METHODS ====================

def get_students_by_staff(self, staff_id):
    """Get all students assigned to a specific staff member"""
    try:
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute('''
                       SELECT id,
                              lrn,
                              firstname,
                              middlename,
                              lastname,
                              gender,
                              birthdate,
                              email,
                              phone,
                              address,
                              grade_level       AS grade,
                              track,
                              strand,
                              guardian_name,
                              guardian_contact,
                              enrollment_status AS status,
                              assigned_staff_id,
                              assigned_staff_email,
                              created_at,
                              updated_at
                       FROM students
                       WHERE assigned_staff_id = %s
                       ORDER BY created_at DESC
                       ''', (staff_id,))

        results = cursor.fetchall()
        cursor.close()
        return results

    except Exception as e:
        print(f"Error getting students by staff: {e}")
        return []


def assign_student_to_staff(self, student_lrn, staff_id, staff_email):
    """Assign a student to a staff member"""
    try:
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
                       UPDATE students
                       SET assigned_staff_id    = %s,
                           assigned_staff_email = %s
                       WHERE lrn = %s
                       ''', (staff_id, staff_email, student_lrn))

        conn.commit()
        cursor.close()

        self.log_action(
            staff_email,
            'ASSIGN_STUDENT',
            f"Assigned student {student_lrn} to staff {staff_email}"
        )
        return True

    except Exception as e:
        conn.rollback()
        print(f"Error assigning student: {e}")
        return False


def unassign_student_from_staff(self, student_lrn):
    """Remove staff assignment from a student"""
    try:
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
                       UPDATE students
                       SET assigned_staff_id    = NULL,
                           assigned_staff_email = NULL
                       WHERE lrn = %s
                       ''', (student_lrn,))

        conn.commit()
        cursor.close()

        self.log_action(None, 'UNASSIGN_STUDENT', f"Removed staff assignment for {student_lrn}")
        return True

    except Exception as e:
        conn.rollback()
        print(f"Error unassigning student: {e}")
        return False


def get_unassigned_students(self):
    """Get all students not assigned to any staff"""
    try:
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute('''
                       SELECT id,
                              lrn,
                              firstname,
                              middlename,
                              lastname,
                              gender,
                              birthdate,
                              email,
                              phone,
                              address,
                              grade_level       AS grade,
                              track,
                              strand,
                              guardian_name,
                              guardian_contact,
                              enrollment_status AS status,
                              created_at,
                              updated_at
                       FROM students
                       WHERE assigned_staff_id IS NULL
                       ORDER BY created_at DESC
                       ''')

        results = cursor.fetchall()
        cursor.close()
        return results

    except Exception as e:
        print(f"Error getting unassigned students: {e}")
        return []


def get_all_staff_users(self):
    """Get all staff users"""
    try:
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute('''
                       SELECT id, email, full_name, role, is_active, created_at
                       FROM users
                       WHERE role = 'STAFF'
                         AND is_active = 1
                       ORDER BY full_name
                       ''')

        results = cursor.fetchall()
        cursor.close()
        return results

    except Exception as e:
        print(f"Error getting staff users: {e}")
        return []


def get_staff_student_count(self, staff_id):
    """Get count of students assigned to a staff member"""
    try:
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
                       SELECT COUNT(*)
                       FROM students
                       WHERE assigned_staff_id = %s
                       ''', (staff_id,))

        count = cursor.fetchone()[0]
        cursor.close()
        return count

    except Exception as e:
        print(f"Error counting staff students: {e}")
        return 0


# ==================== STAFF SUBJECTS METHODS ====================

def add_staff_subject(self, staff_id, staff_email, subject_name, grade_level=None, track=None):
    """Add a subject that a staff member teaches"""
    try:
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
                       INSERT INTO staff_subjects (staff_id, staff_email, subject_name, grade_level, track)
                       VALUES (%s, %s, %s, %s, %s)
                       ''', (staff_id, staff_email, subject_name, grade_level, track))

        conn.commit()
        subject_id = cursor.lastrowid
        cursor.close()
        return subject_id

    except Exception as e:
        conn.rollback()
        print(f"Error adding staff subject: {e}")
        return None


def get_staff_subjects(self, staff_id):
    """Get all subjects a staff member teaches"""
    try:
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute('''
                       SELECT *
                       FROM staff_subjects
                       WHERE staff_id = %s
                       ORDER BY subject_name
                       ''', (staff_id,))

        results = cursor.fetchall()
        cursor.close()
        return results

    except Exception as e:
        print(f"Error getting staff subjects: {e}")
        return []


def delete_staff_subject(self, subject_id):
    """Delete a staff subject"""
    try:
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('DELETE FROM staff_subjects WHERE id = %s', (subject_id,))
        conn.commit()
        cursor.close()
        return True

    except Exception as e:
        conn.rollback()
        print(f"Error deleting staff subject: {e}")
        return False