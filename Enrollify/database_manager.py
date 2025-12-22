import sqlite3
from datetime import datetime
import os

class DatabaseManager:
    """Centralized database management for Enrollify system (SQLite)"""

    def __init__(self, db_name="enrollify.db"):
        self.db_name = db_name
        self.init_database()

    def get_connection(self):
        """Create and return database connection"""
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.db_name) if os.path.dirname(self.db_name) else '.', exist_ok=True)
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row  # Enables dict-like access
        return conn

    def init_database(self):
        """Initialize all required tables"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # ... (your existing tables: students, payments, users, audit_log)

        # ===== NEW: Tracks table =====
        # In init_database():
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS strands
                       (
                           id
                           INTEGER
                           PRIMARY
                           KEY
                           AUTOINCREMENT,
                           name
                           TEXT
                           NOT
                           NULL,
                           track
                           TEXT
                           NOT
                           NULL,
                           FOREIGN
                           KEY
                       (
                           track
                       ) REFERENCES tracks
                       (
                           name
                       ) ON DELETE CASCADE
                           )
                       ''')

        # Insert default strands
        cursor.execute('SELECT COUNT(*) FROM strands')
        if cursor.fetchone()[0] == 0:
            default_strands = [
                ("STEM", "Academic"),
                ("HUMSS", "Academic"),
                ("ABM", "Academic"),
                ("GAS", "Academic"),
                ("Cookery", "TVL"),
                ("Computer Systems Servicing", "TVL"),
                ("Automotive", "TVL"),
                ("Electrical Installation", "TVL")
            ]
            cursor.executemany('INSERT INTO strands (name, track) VALUES (?, ?)', default_strands)

            # In init_database():
            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS tuition_fees
                           (
                               id
                               INTEGER
                               PRIMARY
                               KEY
                               AUTOINCREMENT,
                               track
                               TEXT
                               NOT
                               NULL,
                               strand
                               TEXT,
                               enrollment_fee
                               REAL
                               DEFAULT
                               5000,
                               miscellaneous_fee
                               REAL
                               DEFAULT
                               4500,
                               tuition_fee
                               REAL
                               NOT
                               NULL,
                               special_fee
                               REAL
                               DEFAULT
                               0,
                               created_at
                               TEXT
                               DEFAULT
                               CURRENT_TIMESTAMP,
                               UNIQUE
                           (
                               track,
                               strand
                           )
                               )
                           ''')

            # Insert default fees (run only if table is empty)
            cursor.execute('SELECT COUNT(*) FROM tuition_fees')
            if cursor.fetchone()[0] == 0:
                default_fees = [
                    # Academic Track
                    ("Academic", "STEM", 5000, 4500, 18000, 5000),
                    ("Academic", "HUMSS", 5000, 4500, 15000, 2000),
                    ("Academic", "ABM", 5000, 4500, 15000, 2000),
                    ("Academic", "GAS", 5000, 4500, 15000, 2000),

                    # TVL Track
                    ("TVL", "Cookery", 5000, 4500, 12000, 3000),
                    ("TVL", "CSS", 5000, 4500, 14000, 4000),
                    ("TVL", "Automotive", 5000, 4500, 13000, 3500),

                    # Sports & Arts (no strand)
                    ("Sports", None, 5000, 4500, 10000, 1000),
                    ("Arts & Design", None, 5000, 4500, 12000, 2500),
                ]
                cursor.executemany('''
                                   INSERT INTO tuition_fees (track, strand, enrollment_fee, miscellaneous_fee,
                                                             tuition_fee, special_fee)
                                   VALUES (?, ?, ?, ?, ?, ?)
                                   ''', default_fees)

        conn.commit()
        conn.close()

    def get_tuition_fees(self, track, strand=None):
        """Get tuition fee breakdown for a track/strand"""
        conn = self.get_connection()
        cursor = conn.cursor()

        if strand is None or strand.strip() == "":
            cursor.execute('''
                           SELECT enrollment_fee, miscellaneous_fee, tuition_fee, special_fee
                           FROM tuition_fees
                           WHERE track = ?
                             AND strand IS NULL
                           ''', (track,))
        else:
            cursor.execute('''
                           SELECT enrollment_fee, miscellaneous_fee, tuition_fee, special_fee
                           FROM tuition_fees
                           WHERE track = ?
                             AND strand = ?
                           ''', (track, strand))

        result = cursor.fetchone()
        conn.close()

        if result:
            return {
                'enrollment_fee': result[0],
                'miscellaneous_fee': result[1],
                'tuition_fee': result[2],
                'special_fee': result[3],
                'total': sum(result)
            }
        else:
            # Fallback: default fees
            return {
                'enrollment_fee': 5000,
                'miscellaneous_fee': 4500,
                'tuition_fee': 15000,
                'special_fee': 2000,
                'total': 26500
            }

    def ensure_tuition_fees_table(self):
        """Add tuition_fees table if it doesn't exist (for existing databases)"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Create table if not exists
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS tuition_fees
                       (
                           id
                           INTEGER
                           PRIMARY
                           KEY
                           AUTOINCREMENT,
                           track
                           TEXT
                           NOT
                           NULL,
                           strand
                           TEXT,
                           enrollment_fee
                           REAL
                           DEFAULT
                           5000,
                           miscellaneous_fee
                           REAL
                           DEFAULT
                           4500,
                           tuition_fee
                           REAL
                           NOT
                           NULL,
                           special_fee
                           REAL
                           DEFAULT
                           0,
                           created_at
                           TEXT
                           DEFAULT
                           CURRENT_TIMESTAMP,
                           UNIQUE
                       (
                           track,
                           strand
                       )
                           )
                       ''')

        # Insert default fees only if table is empty
        cursor.execute('SELECT COUNT(*) FROM tuition_fees')
        if cursor.fetchone()[0] == 0:
            default_fees = [
                # Academic Track
                ("Academic", "STEM", 5000, 4500, 18000, 5000),
                ("Academic", "HUMSS", 5000, 4500, 15000, 2000),
                ("Academic", "ABM", 5000, 4500, 15000, 2000),
                ("Academic", "GAS", 5000, 4500, 15000, 2000),

                # TVL Track
                ("TVL", "Cookery", 5000, 4500, 12000, 3000),
                ("TVL", "CSS", 5000, 4500, 14000, 4000),
                ("TVL", "Automotive", 5000, 4500, 13000, 3500),

                # Sports & Arts (no strand)
                ("Sports", None, 5000, 4500, 10000, 1000),
                ("Arts & Design", None, 5000, 4500, 12000, 2500),
            ]
            cursor.executemany('''
                               INSERT INTO tuition_fees (track, strand, enrollment_fee, miscellaneous_fee, tuition_fee,
                                                         special_fee)
                               VALUES (?, ?, ?, ?, ?, ?)
                               ''', default_fees)

        conn.commit()
        conn.close()

    # ==================== TRACK OPERATIONS ====================

    def count_by_track(self):
        """Returns dict like {'Academic': 25, 'TVL': 18}"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT track, COUNT(*) FROM students GROUP BY track')
        result = dict(cursor.fetchall())
        conn.close()
        return result

    def get_strands_by_track(self, track_name):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM strands WHERE track = ? ORDER BY name', (track_name,))
        strands = [row[0] for row in cursor.fetchall()]
        conn.close()
        return strands

    def get_all_tracks(self):
        """Get all available tracks"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM tracks ORDER BY name')
        tracks = [row[0] for row in cursor.fetchall()]
        conn.close()
        return tracks

    def add_track(self, name, description=""):
        """Add new track"""
        if not name.strip():
            raise ValueError("Track name cannot be empty")
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO tracks (name, description) VALUES (?, ?)', (name.strip(), description))
            conn.commit()
            self.log_action(None, 'ADD_TRACK', f"Added track: {name}")
        except sqlite3.IntegrityError:
            conn.rollback()
            raise ValueError(f"Track '{name}' already exists")
        finally:
            conn.close()

    def remove_track(self, name):
        """Remove track (only if no students use it)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            # Check if any student uses this track
            cursor.execute('SELECT COUNT(*) FROM students WHERE track = ?', (name,))
            if cursor.fetchone()[0] > 0:
                raise ValueError("Cannot delete track in use by students")

            cursor.execute('DELETE FROM tracks WHERE name = ?', (name,))
            conn.commit()
            self.log_action(None, 'REMOVE_TRACK', f"Removed track: {name}")
        finally:
            conn.close()

    def is_valid_track(self, track_name):
        """Check if track exists"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT 1 FROM tracks WHERE name = ?', (track_name,))
        exists = cursor.fetchone() is not None
        conn.close()
        return exists

    # ==================== STUDENT OPERATIONS ====================

    def add_student(self, student_data):
        """Add new student to database with track validation"""
        track = student_data['track']
        if not self.is_valid_track(track):
            raise Exception(f"Invalid track: '{track}'. Please select from available tracks.")

        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute('''
                           INSERT INTO students
                           (lrn, firstname, middlename, lastname, gender, birthdate,
                            email, phone, address, grade_level, track, strand,
                            guardian_name, guardian_contact)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                           ''', (
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
                               track,  # Validated
                               student_data.get('strand', ''),
                               student_data['guardian_name'],
                               student_data['guardian_contact']
                           ))

            student_id = cursor.lastrowid
            conn.commit()
            self.log_action(None, 'ADD_STUDENT', f"Added student: {student_data['lrn']}")
            return student_id
        except sqlite3.IntegrityError as e:
            conn.rollback()
            raise Exception(f"Student with LRN {student_data['lrn']} already exists")
        finally:
            conn.close()

    def get_student_by_lrn(self, lrn):
        """Get student by LRN"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM students WHERE lrn = ?', (lrn,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def get_all_students(self):
        """Get all students with UI-friendly aliases"""
        conn = self.get_connection()
        cursor = conn.cursor()
        # Alias grade_level → grade, enrollment_status → status for UI consistency
        cursor.execute('''
            SELECT 
                id, lrn, firstname, middlename, lastname, gender, birthdate,
                email, phone, address, grade_level AS grade, track, strand,
                guardian_name, guardian_contact, enrollment_status AS status,
                created_at, updated_at
            FROM students 
            ORDER BY lastname, firstname
        ''')
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def update_student(self, lrn, student_data):
        """Update student to database with track validation"""
        track = student_data['track']
        if not self.is_valid_track(track):
            raise Exception(f"Invalid track: '{track}'. Please select from available tracks.")

        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                UPDATE students SET
                    firstname = ?,
                    middlename = ?,
                    lastname = ?,
                    gender = ?,
                    birthdate = ?,
                    email = ?,
                    phone = ?,
                    address = ?,
                    grade_level = ?,
                    track = ?,
                    strand = ?,
                    guardian_name = ?,
                    guardian_contact = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE lrn = ?
            ''', (
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
            ))
            conn.commit()
            self.log_action(None, 'UPDATE_STUDENT', f"Updated student: {lrn}")
            return True
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def delete_student(self, lrn):
        """Delete student and related payments"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM students WHERE lrn = ?', (lrn,))
            cursor.execute('DELETE FROM payments WHERE lrn = ?', (lrn,))
            conn.commit()
            self.log_action(None, 'DELETE_STUDENT', f"Deleted student: {lrn}")
            return True
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def update_enrollment_status(self, lrn, status):
        """Update student enrollment status"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE students SET 
                enrollment_status = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE lrn = ?
        ''', (status, lrn))
        conn.commit()
        conn.close()
        self.log_action(None, 'UPDATE_STATUS', f"Changed status for {lrn} to {status}")

    # ==================== PAYMENT OPERATIONS ====================

    def add_payment(self, payment_data):
        """Record payment and auto-enroll student"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            # Get student ID
            cursor.execute('SELECT id FROM students WHERE lrn = ?', (payment_data['student_data']['lrn'],))
            result = cursor.fetchone()
            if not result:
                raise Exception("Student not found")
            student_id = result[0]

            # Insert payment
            cursor.execute('''
                INSERT INTO payments 
                (student_id, lrn, amount, payment_method)
                VALUES (?, ?, ?, ?)
            ''', (
                student_id,
                payment_data['student_data']['lrn'],
                payment_data['amount'],
                payment_data['payment_method']
            ))

            # Enroll student
            cursor.execute('''
                UPDATE students SET enrollment_status = 'Enrolled'
                WHERE lrn = ?
            ''', (payment_data['student_data']['lrn'],))

            payment_id = cursor.lastrowid
            conn.commit()
            self.log_action(None, 'ADD_PAYMENT', f"Payment received for LRN: {payment_data['student_data']['lrn']}")
            return payment_id
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def get_payments_by_lrn(self, lrn):
        """Get all payments for a student"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM payments WHERE lrn = ? ORDER BY payment_date DESC', (lrn,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    # ==================== USER OPERATIONS ====================

    def authenticate_user(self, email, password):
        """Authenticate user login"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, email, role, full_name FROM users WHERE email = ? AND password = ?', (email, password))
        row = cursor.fetchone()
        conn.close()
        if row:
            self.log_action(email, 'LOGIN', f"{row['role']} logged in")
            return dict(row)
        return None

    def add_user(self, email, password, role, full_name):
        """Add new user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO users (email, password, role, full_name) VALUES (?, ?, ?, ?)',
                           (email, password, role, full_name))
            conn.commit()
            self.log_action(None, 'ADD_USER', f"Added user: {email}")
            return True
        except sqlite3.IntegrityError:
            conn.rollback()
            raise Exception(f"User with email {email} already exists")
        finally:
            conn.close()

    # ==================== ANALYTICS & STATISTICS ====================

    def get_statistics(self):
        """Get key system statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*) FROM students')
        total_students = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM students WHERE enrollment_status = 'Enrolled'")
        enrolled = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM students WHERE enrollment_status = 'Pending'")
        pending = cursor.fetchone()[0]

        cursor.execute('SELECT SUM(amount) FROM payments')
        total_revenue = cursor.fetchone()[0] or 0.0

        conn.close()

        return {
            'total_students': total_students,
            'enrolled': enrolled,
            'pending': pending,
            'total_revenue': float(total_revenue)
        }

    def get_gender_distribution(self):
        """Return list of (gender, count) for charts"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT gender, COUNT(*) 
            FROM students 
            WHERE gender IS NOT NULL AND TRIM(gender) != ''
            GROUP BY gender
        ''')
        results = cursor.fetchall()
        conn.close()
        return [(row[0], row[1]) for row in results]

    def get_enrollment_status_distribution(self):
        """Return list of (status, count)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT enrollment_status, COUNT(*) 
            FROM students 
            GROUP BY enrollment_status
        ''')
        results = cursor.fetchall()
        conn.close()
        return [(row[0], row[1]) for row in results]

    def get_grade_distribution(self):
        """Return list of (grade_level, count)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT grade_level, COUNT(*) 
            FROM students 
            GROUP BY grade_level
            ORDER BY grade_level
        ''')
        results = cursor.fetchall()
        conn.close()
        return [(row[0], row[1]) for row in results]

    def get_monthly_enrollments(self):
        """Return list of ('YYYY-MM', count) for trend line chart"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT substr(created_at, 1, 7) as month, COUNT(*)
            FROM students
            GROUP BY month
            ORDER BY month
        ''')
        results = cursor.fetchall()
        conn.close()
        return [(row[0], row[1]) for row in results]

    # ========== BACKWARD COMPATIBILITY (for staff_portal.py) ==========

    def count_by_track(self):
        """Legacy method — returns dict {track: count}"""
        data = self.get_grade_distribution()  # Wait, no — this is grade!
        # Actually, we need track counts:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT track, COUNT(*) FROM students GROUP BY track')
        result = dict(cursor.fetchall())
        conn.close()
        return result

    def count_enrollment_status(self):
        """Legacy method — returns dict {status: count}"""
        data = self.get_enrollment_status_distribution()
        return dict(data)  # Convert list of tuples to dict

    def count_by_grade(self):
        """Legacy method — returns dict {grade: count}"""
        data = self.get_grade_distribution()
        return dict(data)

    def count_by_strand(self, top_n=None):
        """Legacy method — returns dict {strand: count}"""
        conn = self.get_connection()
        cursor = conn.cursor()
        query = 'SELECT strand, COUNT(*) FROM students WHERE strand IS NOT NULL AND strand != "" GROUP BY strand'
        if top_n:
            query += f" ORDER BY COUNT(*) DESC LIMIT {int(top_n)}"
        cursor.execute(query)
        result = dict(cursor.fetchall())
        conn.close()
        return result or {"Unspecified": 0}

    # ==================== AUDIT LOG ====================

    def log_action(self, user_email, action, details):
        """Log system action"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO audit_log (user_email, action, details) VALUES (?, ?, ?)',
                       (user_email, action, details))
        conn.commit()
        conn.close()

    def get_audit_log(self, limit=100):
        """Get audit log entries"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, user_email AS user, action, details, timestamp
            FROM audit_log
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    # ==================== SEARCH & FILTER ====================

    def search_students(self, query):
        """Search students by name or LRN"""
        conn = self.get_connection()
        cursor = conn.cursor()
        search_query = f"%{query}%"
        cursor.execute('''
            SELECT 
                id, lrn, firstname, middlename, lastname, gender, birthdate,
                email, phone, address, grade_level AS grade, track, strand,
                guardian_name, guardian_contact, enrollment_status AS status,
                created_at, updated_at
            FROM students 
            WHERE lrn LIKE ? OR firstname LIKE ? OR lastname LIKE ?
            ORDER BY created_at DESC
        ''', (search_query, search_query, search_query))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def filter_students(self, grade=None, track=None, status=None):
        """Filter students by criteria"""
        conn = self.get_connection()
        cursor = conn.cursor()

        query = '''
            SELECT 
                id, lrn, firstname, middlename, lastname, gender, birthdate,
                email, phone, address, grade_level AS grade, track, strand,
                guardian_name, guardian_contact, enrollment_status AS status,
                created_at, updated_at
            FROM students 
            WHERE 1=1
        '''
        params = []

        if grade:
            query += ' AND grade_level = ?'
            params.append(grade)
        if track:
            query += ' AND track = ?'
            params.append(track)
        if status:
            query += ' AND enrollment_status = ?'
            params.append(status)

        query += ' ORDER BY created_at DESC'

        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]


# Singleton instance
_db_instance = None

def get_database():
    """Get database manager singleton instance"""
    global _db_instance
    if _db_instance is None:
        _db_instance = DatabaseManager()
    return _db_instance