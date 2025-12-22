import re
from datetime import datetime


class ValidationUtils:
    """Validation utilities for Enrollify system"""

    @staticmethod
    def validate_email(email):
        """Validate email format"""
        if not email:
            return False, "Email is required"

        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            return False, "Invalid email format"

        return True, ""

    @staticmethod
    def validate_phone_philippines(phone):
        """Validate Philippine phone number"""
        if not phone:
            return False, "Phone number is required"

        # Remove spaces, dashes, and parentheses
        cleaned = re.sub(r'[\s\-\(\)]', '', phone)

        # Check formats: +639XXXXXXXXX, 09XXXXXXXXX, 9XXXXXXXXX
        patterns = [
            r'^\+639\d{9}$',  # +639XXXXXXXXX
            r'^09\d{9}$',  # 09XXXXXXXXX
            r'^9\d{9}$'  # 9XXXXXXXXX
        ]

        for pattern in patterns:
            if re.match(pattern, cleaned):
                return True, ""

        return False, "Invalid Philippine phone number format (use +63 XXX XXX XXXX or 09XX XXX XXXX)"

    @staticmethod
    def validate_lrn(lrn):
        """Validate Learner Reference Number (12 digits)"""
        if not lrn:
            return False, "LRN is required"

        if not lrn.isdigit():
            return False, "LRN must contain only numbers"

        if len(lrn) != 12:
            return False, "LRN must be exactly 12 digits"

        return True, ""

    @staticmethod
    def validate_name(name, field_name):
        """Validate name fields"""
        if not name:
            return False, f"{field_name} is required"

        if len(name) < 2:
            return False, f"{field_name} must be at least 2 characters"

        if len(name) > 50:
            return False, f"{field_name} must not exceed 50 characters"

        # Allow letters, spaces, hyphens, and apostrophes
        if not re.match(r"^[a-zA-Z\s\-']+$", name):
            return False, f"{field_name} contains invalid characters"

        return True, ""

    @staticmethod
    def validate_password(password):
        """Validate password strength"""
        if not password:
            return False, "Password is required"

        if len(password) < 6:
            return False, "Password must be at least 6 characters"

        if len(password) > 50:
            return False, "Password must not exceed 50 characters"

        # Check for at least one letter and one number (optional, can be enforced)
        # if not re.search(r'[A-Za-z]', password) or not re.search(r'\d', password):
        #     return False, "Password must contain at least one letter and one number"

        return True, ""

    @staticmethod
    def validate_date(date_string, format_str='%m/%d/%Y'):
        """Validate date format and check if it's reasonable"""
        if not date_string:
            return False, "Date is required"

        try:
            date_obj = datetime.strptime(date_string, format_str)

            # Check if date is not in future
            if date_obj > datetime.now():
                return False, "Date cannot be in the future"

            # Check if date is reasonable (not too old, e.g., not before 1900)
            if date_obj.year < 1900:
                return False, "Invalid date"

            return True, ""
        except ValueError:
            return False, f"Invalid date format (use {format_str})"

    @staticmethod
    def validate_birthdate_for_shs(birthdate_string, format_str='%m/%d/%Y'):
        """Validate birthdate specifically for SHS students (age 15-20 typically)"""
        valid, message = ValidationUtils.validate_date(birthdate_string, format_str)
        if not valid:
            return False, message

        try:
            birthdate = datetime.strptime(birthdate_string, format_str)
            today = datetime.now()
            age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

            if age < 13:
                return False, "Student must be at least 13 years old for Senior High School"

            if age > 25:
                return False, "Please verify the birthdate (student appears to be over 25 years old)"

            return True, ""
        except ValueError:
            return False, "Invalid birthdate"

    @staticmethod
    def validate_address(address):
        """Validate address"""
        if not address:
            return False, "Address is required"

        if len(address) < 10:
            return False, "Please provide a complete address (at least 10 characters)"

        if len(address) > 200:
            return False, "Address is too long (max 200 characters)"

        return True, ""

    @staticmethod
    def sanitize_input(text):
        """Sanitize text input to prevent XSS and other attacks"""
        if not text:
            return ""

        # Remove any HTML tags
        text = re.sub(r'<[^>]+>', '', text)

        # Remove special characters that could be used for injection
        text = re.sub(r'[<>\"\'%;()&+]', '', text)

        return text.strip()

    @staticmethod
    def validate_grade_level(grade):
        """Validate grade level"""
        valid_grades = ['Grade 11', 'Grade 12']
        if grade not in valid_grades:
            return False, "Please select a valid grade level"
        return True, ""

    @staticmethod
    def validate_track(track):
        """Validate track selection"""
        valid_tracks = ['Academic Track', 'TVL Track', 'Sports Track', 'Arts and Design Track']
        if track not in valid_tracks:
            return False, "Please select a valid track"
        return True, ""

    @staticmethod
    def validate_gender(gender):
        """Validate gender selection"""
        valid_genders = ['Male', 'Female']
        if gender not in valid_genders:
            return False, "Please select a valid gender"
        return True, ""

    @staticmethod
    def validate_enrollment_form(form_data):
        """Comprehensive validation for enrollment form"""
        errors = []

        # LRN
        valid, msg = ValidationUtils.validate_lrn(form_data.get('lrn', ''))
        if not valid:
            errors.append(f"LRN: {msg}")

        # Gender
        valid, msg = ValidationUtils.validate_gender(form_data.get('gender', ''))
        if not valid:
            errors.append(f"Gender: {msg}")

        # First Name
        valid, msg = ValidationUtils.validate_name(form_data.get('firstname', ''), "First Name")
        if not valid:
            errors.append(msg)

        # Last Name
        valid, msg = ValidationUtils.validate_name(form_data.get('lastname', ''), "Last Name")
        if not valid:
            errors.append(msg)

        # Middle Name (optional but validate if provided)
        if form_data.get('middlename'):
            valid, msg = ValidationUtils.validate_name(form_data.get('middlename', ''), "Middle Name")
            if not valid:
                errors.append(msg)

        # Birthdate
        valid, msg = ValidationUtils.validate_birthdate_for_shs(form_data.get('birthdate', ''))
        if not valid:
            errors.append(f"Birth Date: {msg}")

        # Email
        valid, msg = ValidationUtils.validate_email(form_data.get('email', ''))
        if not valid:
            errors.append(f"Email: {msg}")

        # Phone
        valid, msg = ValidationUtils.validate_phone_philippines(form_data.get('phone', ''))
        if not valid:
            errors.append(f"Phone: {msg}")

        # Address
        valid, msg = ValidationUtils.validate_address(form_data.get('address', ''))
        if not valid:
            errors.append(f"Address: {msg}")

        # Grade Level
        valid, msg = ValidationUtils.validate_grade_level(form_data.get('grade', ''))
        if not valid:
            errors.append(f"Grade Level: {msg}")

        # Track
        valid, msg = ValidationUtils.validate_track(form_data.get('track', ''))
        if not valid:
            errors.append(f"Track: {msg}")

        # Guardian Name
        valid, msg = ValidationUtils.validate_name(form_data.get('guardian_name', ''), "Guardian Name")
        if not valid:
            errors.append(msg)

        # Guardian Contact
        valid, msg = ValidationUtils.validate_phone_philippines(form_data.get('guardian_contact', ''))
        if not valid:
            errors.append(f"Guardian Contact: {msg}")

        if errors:
            return False, "\n".join(errors)

        return True, "All validations passed"

    @staticmethod
    def format_phone_number(phone):
        """Format phone number to standard Philippine format"""
        # Remove all non-digit characters
        digits = re.sub(r'\D', '', phone)

        # Convert to +63 format
        if digits.startswith('0'):
            digits = '63' + digits[1:]
        elif digits.startswith('9'):
            digits = '63' + digits
        elif not digits.startswith('63'):
            return phone  # Return original if it can't determine format

        # Format as +63 XXX XXX XXXX
        if len(digits) == 12:
            return f"+{digits[:2]} {digits[2:5]} {digits[5:8]} {digits[8:]}"

        return phone


# Utility function for quick access
def validate_form(form_data):
    """Quick validation function"""
    return ValidationUtils.validate_enrollment_form(form_data)