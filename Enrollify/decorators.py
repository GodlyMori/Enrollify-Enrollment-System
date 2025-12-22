"""
Utility decorators for error handling and authentication
Makes code cleaner and more maintainable
"""

import functools
import logging
from PyQt6.QtWidgets import QMessageBox

logger = logging.getLogger(__name__)


def safe_database_operation(operation_name: str):
    """
    Decorator for safe database operations with user feedback

    Catches errors and shows user-friendly messages
    Logs all errors for debugging

    Args:
        operation_name: Description of the operation (e.g., "Load Students")

    Example:
        @safe_database_operation("Load Students")
        def load_students(self):
            # Your code here
            pass
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)

            except ValueError as e:
                # User-friendly errors (like duplicate LRN)
                logger.warning(f"{operation_name} - Validation error: {e}")
                QMessageBox.warning(
                    None,
                    "Validation Error",
                    str(e)
                )
                return None

            except ConnectionError as e:
                # Database connection errors
                logger.error(f"{operation_name} - Connection error: {e}")
                QMessageBox.critical(
                    None,
                    "Connection Error",
                    "Unable to connect to the database.\n"
                    "Please check your connection and try again."
                )
                return None

            except Exception as e:
                # Unexpected errors
                logger.error(
                    f"{operation_name} - Unexpected error: {e}",
                    exc_info=True
                )
                QMessageBox.critical(
                    None,
                    "Error",
                    f"An unexpected error occurred during {operation_name.lower()}.\n"
                    f"Please try again or contact support if the problem persists.\n\n"
                    f"Error details: {str(e)}"
                )
                return None

        return wrapper

    return decorator


def require_authentication(func):
    """
    Decorator to require authentication before executing a function

    Example:
        @require_authentication
        def delete_student(self, student_id):
            # Only runs if user is logged in
            pass
    """

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if not hasattr(self, 'current_user') or self.current_user is None:
            logger.warning(f"Unauthenticated access attempt to {func.__name__}")
            QMessageBox.warning(
                self,
                "Authentication Required",
                "You must be logged in to perform this action."
            )
            return None
        return func(self, *args, **kwargs)

    return wrapper


def require_role(*allowed_roles):
    """
    Decorator to require specific user role(s)

    Args:
        *allowed_roles: One or more roles (e.g., 'admin', 'staff')

    Example:
        @require_role('admin')
        def delete_user(self, user_id):
            # Only admin can delete users
            pass
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if not hasattr(self, 'current_user') or self.current_user is None:
                QMessageBox.warning(
                    self,
                    "Authentication Required",
                    "You must be logged in to perform this action."
                )
                return None

            user_role = self.current_user.get('role', '')
            if user_role not in allowed_roles:
                logger.warning(
                    f"Unauthorized access attempt by {user_role} to {func.__name__}"
                )
                QMessageBox.warning(
                    self,
                    "Access Denied",
                    f"You don't have permission to perform this action.\n"
                    f"Required role: {', '.join(allowed_roles)}"
                )
                return None

            return func(self, *args, **kwargs)

        return wrapper

    return decorator


def log_operation(operation_type: str):
    """
    Decorator to automatically log operations

    Args:
        operation_type: Type of operation for logging

    Example:
        @log_operation("DATA_EXPORT")
        def export_data(self):
            pass
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger.info(f"Starting operation: {operation_type}")
            try:
                result = func(*args, **kwargs)
                logger.info(f"Completed operation: {operation_type}")
                return result
            except Exception as e:
                logger.error(f"Failed operation: {operation_type} - {e}")
                raise

        return wrapper

    return decorator