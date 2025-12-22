"""
COMPLETE Configuration for Enrollify System
Works with ALL database managers (SQLite, MySQL, Enhanced)
"""

import os
from pathlib import Path


class Config:
    """Application configuration - COMPLETE VERSION"""

    # ===== PATHS =====
    BASE_DIR = Path(__file__).parent
    ASSETS_DIR = BASE_DIR / 'assets'
    LOGS_DIR = BASE_DIR / 'logs'

    # ===== DATABASE =====
    # Works with both SQLite AND MySQL

    # For SQLite (simple, no server needed)
    DB_NAME = "enrollify.db"

    # For MySQL (if you want to use it later)
    DB_HOST = "127.0.0.1"
    DB_USER = "root"
    DB_PASSWORD = ""  # Add your password if you have one
    DB_NAME = "enrollify_db"
    DB_PORT = 3306

    # For database_manager_enhanced.py (MySQL with connection pooling)
    DB_POOL_SIZE = 5  # ← THIS WAS MISSING!

    # ===== APPLICATION =====
    APP_NAME = "Enrollify"
    APP_VERSION = "1.0.0"

    # ===== UI SETTINGS =====
    WINDOW_MIN_WIDTH = 1200
    WINDOW_MIN_HEIGHT = 800

    # ===== SECURITY =====
    PASSWORD_MIN_LENGTH = 6
    SESSION_TIMEOUT = 3600  # seconds
    MAX_LOGIN_ATTEMPTS = 5
    ACCOUNT_LOCK_DURATION = 1800  # seconds

    # ===== PERFORMANCE =====
    PAGE_SIZE = 50
    CACHE_TIMEOUT = 60

    @classmethod
    def ensure_directories(cls):
        """Create necessary directories if they don't exist"""
        cls.LOGS_DIR.mkdir(exist_ok=True)
        cls.ASSETS_DIR.mkdir(exist_ok=True)

    @classmethod
    def get_asset_path(cls, filename):
        """Get full path to asset file"""
        return cls.ASSETS_DIR / filename


# Create directories on import
Config.ensure_directories()

# Print what we're using (for debugging)
if __name__ == '__main__':
    print("=" * 60)
    print("ENROLLIFY CONFIGURATION")
    print("=" * 60)
    print(f"App Name: {Config.APP_NAME}")
    print(f"Version: {Config.APP_VERSION}")
    print(f"Database: {Config.DB_NAME}")
    print(f"MySQL Host: {Config.DB_HOST}")
    print(f"Pool Size: {Config.DB_POOL_SIZE}")
    print("=" * 60)