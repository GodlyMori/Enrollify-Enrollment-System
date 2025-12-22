"""
Constants for Enrollify System
All constant values in one place for easy modification
"""

# ===== VALID OPTIONS =====

VALID_GRADES = ['Grade 11', 'Grade 12']

VALID_TRACKS = [
    'Academic Track',
    'TVL Track',
    'Sports Track',
    'Arts and Design Track'
]

VALID_GENDERS = ['Male', 'Female']

VALID_STRANDS = [
    # Academic Track
    'STEM',
    'HUMSS',
    'ABM',
    'GAS',
    # TVL Track
    'ICT',
    'Home Economics',
    'Agri-Fishery',
    # Sports & Arts
    'Sports',
    'Arts',
    'Design'
]

# ===== ENROLLMENT STATUS =====

ENROLLMENT_STATUS = {
    'PENDING': 'Pending',
    'ENROLLED': 'Enrolled',
    'CANCELLED': 'Cancelled',
    'DROPPED': 'Dropped'
}

# ===== USER ROLES =====

USER_ROLES = {
    'ADMIN': 'admin',
    'STAFF': 'staff',
    'STUDENT': 'student'
}

# ===== UI COLORS =====

COLORS = {
    'PRIMARY': '#2D9B84',
    'SECONDARY': '#5DBAA3',
    'SUCCESS': '#10B981',
    'WARNING': '#F59E0B',
    'DANGER': '#EF4444',
    'INFO': '#0099FF',
    'BACKGROUND': '#F8F9FA',
    'DARK': '#060C0B',
    'LIGHT': '#FFFFFF',
    'BORDER': '#E5E7EB'
}

# ===== PAYMENT FEES (in PHP) =====

FEES = {
    'ENROLLMENT': 5000,
    'MISCELLANEOUS': 4500,
    'TUITION_STEM': 18000,
    'TUITION_HUMSS': 16000,
    'TUITION_ABM': 17000,
    'TUITION_TVL': 15000,
    'TUITION_GAS': 16000,
    'LABORATORY': 5000,
    'SPORTS': 3000,
    'ARTS': 4000
}

# ===== PAYMENT METHODS =====

PAYMENT_METHODS = [
    'Cash',
    'Credit Card',
    'Debit Card',
    'GCash',
    'PayMaya',
    'Bank Transfer'
]

# ===== ACTION TYPES (for audit logging) =====

ACTION_TYPES = {
    'LOGIN_SUCCESS': 'Login Success',
    'LOGIN_FAILED': 'Login Failed',
    'LOGOUT': 'Logout',
    'USER_CREATED': 'User Created',
    'PASSWORD_CHANGED': 'Password Changed',
    'STUDENT_CREATED': 'Student Created',
    'STUDENT_UPDATED': 'Student Updated',
    'STUDENT_DELETED': 'Student Deleted',
    'STATUS_UPDATED': 'Status Updated',
    'PAYMENT_RECORDED': 'Payment Recorded'
}