"""
Logging configuration for Enrollify System
Sets up file and console logging
"""

import logging
import sys
from pathlib import Path
from config import Config


def setup_logging():
    """
    Setup application logging

    Creates:
    - enrollify.log: All logs (INFO and above)
    - errors.log: Error logs only
    - Console output: Warnings and errors

    Returns:
        logging.Logger: Configured root logger
    """

    # Ensure log directory exists
    Config.ensure_directories()

    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    simple_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # File handler for all logs
    all_logs_handler = logging.FileHandler(
        Config.LOGS_DIR / 'enrollify.log',
        encoding='utf-8'
    )
    all_logs_handler.setLevel(logging.INFO)
    all_logs_handler.setFormatter(detailed_formatter)

    # File handler for errors only
    error_handler = logging.FileHandler(
        Config.LOGS_DIR / 'errors.log',
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(detailed_formatter)

    # Console handler for development
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(simple_formatter)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Remove existing handlers (in case of reconfiguration)
    root_logger.handlers.clear()

    # Add handlers
    root_logger.addHandler(all_logs_handler)
    root_logger.addHandler(error_handler)
    root_logger.addHandler(console_handler)

    # Log startup message
    root_logger.info("=" * 60)
    root_logger.info(f"{Config.APP_NAME} v{Config.APP_VERSION} - Logging Started")
    root_logger.info("=" * 60)

    return root_logger


def get_logger(name):
    """
    Get a logger instance for a specific module

    Args:
        name (str): Name of the module (usually __name__)

    Returns:
        logging.Logger: Logger instance

    Example:
        logger = get_logger(__name__)
        logger.info("This is an info message")
    """
    return logging.getLogger(name)