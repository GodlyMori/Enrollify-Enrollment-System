"""
Authentication utilities with bcrypt password hashing
Place this file in your project root directory
"""
import bcrypt


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt

    Args:
        password: Plain text password

    Returns:
        Bcrypt hashed password string
    """
    if not password:
        raise ValueError("Password cannot be empty")

    # Generate salt and hash
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed.decode('utf-8')


def verify_password(password: str, password_hash: str) -> bool:
    """
    Verify a password against a bcrypt hash

    Args:
        password: Plain text password to verify
        password_hash: Bcrypt hash to compare against

    Returns:
        True if password matches, False otherwise
    """
    try:
        if not password or not password_hash:
            return False

        return bcrypt.checkpw(
            password.encode('utf-8'),
            password_hash.encode('utf-8')
        )
    except Exception as e:
        print(f"Password verification error: {e}")
        return False


def validate_password_strength(password: str) -> tuple[bool, str]:
    """
    Validate password meets minimum security requirements

    Args:
        password: Password to validate

    Returns:
        Tuple of (is_valid, message)
    """
    if not password:
        return False, "Password is required"

    if len(password) < 6:
        return False, "Password must be at least 6 characters long"

    if len(password) > 128:
        return False, "Password is too long (max 128 characters)"

    # Optional: Add more strength checks
    # has_upper = any(c.isupper() for c in password)
    # has_lower = any(c.islower() for c in password)
    # has_digit = any(c.isdigit() for c in password)

    return True, "Password is valid"


# Example usage and testing
if __name__ == '__main__':
    print("=== Bcrypt Password Hashing Demo ===\n")

    # Test password
    test_password = "admin123"

    # Hash the password
    print(f"Original password: {test_password}")
    hashed = hash_password(test_password)
    print(f"Hashed password: {hashed}\n")

    # Verify correct password
    is_valid = verify_password(test_password, hashed)
    print(f"Verify correct password: {is_valid}")

    # Verify incorrect password
    is_valid = verify_password("wrongpassword", hashed)
    print(f"Verify wrong password: {is_valid}\n")

    # Validate password strength
    valid, message = validate_password_strength("12345")
    print(f"Validate '12345': {valid} - {message}")

    valid, message = validate_password_strength("admin123")
    print(f"Validate 'admin123': {valid} - {message}")