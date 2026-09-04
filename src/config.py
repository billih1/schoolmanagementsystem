"""
Configuration module for School Management System
"""

import os
import sys
from pathlib import Path


class Config:
    """Application configuration and constants"""

    # Application info
    APP_NAME = "School Management System"
    APP_VERSION = "1.0.0"
    APP_AUTHOR = "School Administration"

    # Database settings
    DB_FILENAME = "school.db"

    # File paths
    @staticmethod
    def get_app_data_dir():
        """Get application data directory"""
        if os.name == 'nt':  # Windows
            return Path(os.getenv('LOCALAPPDATA', '')) / 'SchoolManagementSystem'
        else:
            return Path.home() / '.SchoolManagementSystem'

    @staticmethod
    def get_db_path():
        """Get database file path"""
        return Config.get_app_data_dir() / 'data' / Config.DB_FILENAME

    @staticmethod
    def get_backup_dir():
        """Get backup directory"""
        return Config.get_app_data_dir() / 'backups'

    @staticmethod
    def get_reports_dir():
        """Get reports export directory"""
        docs = Path(os.getenv('USERPROFILE', '')) / 'Documents'
        reports = docs / 'School_Reports'
        reports.mkdir(parents=True, exist_ok=True)
        return reports

    @staticmethod
    def get_log_dir():
        """Get log directory"""
        return Config.get_app_data_dir() / 'logs'

    # UI settings
    WINDOW_MIN_WIDTH = 1200
    WINDOW_MIN_HEIGHT = 700
    DEFAULT_THEME = "light"

    # Pagination
    DEFAULT_PAGE_SIZE = 50

    # Date formats
    DATE_FORMAT = "yyyy-MM-dd"
    DISPLAY_DATE_FORMAT = "dd MMMM yyyy"

    # Grading scales
    DEFAULT_GRADING_SCALE = {
        "A+": (90, 100, 4.0),
        "A": (85, 89, 4.0),
        "A-": (80, 84, 3.7),
        "B+": (75, 79, 3.3),
        "B": (70, 74, 3.0),
        "B-": (65, 69, 2.7),
        "C+": (60, 64, 2.3),
        "C": (55, 59, 2.0),
        "C-": (50, 54, 1.7),
        "D": (40, 49, 1.0),
        "F": (0, 39, 0.0)
    }

    # Attendance thresholds
    MIN_ATTENDANCE_PERCENTAGE = 75

    # Fee settings
    DEFAULT_DUE_DAYS = 15

    # User roles
    ROLES = {
        "admin": "Administrator",
        "accountant": "Accountant",
        "teacher": "Teacher",
        "clerk": "Clerk"
    }

    ROLE_PERMISSIONS = {
        "admin": ["*"],
        "accountant": ["fee", "reports", "students_view"],
        "teacher": ["marks", "questions", "attendance", "students_view", "reports"],
        "clerk": ["students", "attendance", "students_view"]
    }

    # Blood groups
    BLOOD_GROUPS = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]

    # Gender options
    GENDER_OPTIONS = ["M", "F", "Other"]

    # Enrollment statuses
    ENROLLMENT_STATUSES = ["Enrolled", "Suspended", "Struck Off", "Graduated", "Alumni"]

    # Staff designations
    STAFF_DESIGNATIONS = [
        "Principal",
        "Vice Principal",
        "Subject Specialist",
        "Senior Teacher",
        "Teacher",
        "Clerk",
        "Accountant",
        "Librarian",
        "Lab Assistant",
        "Support Staff"
    ]

    # Attendance statuses
    ATTENDANCE_STATUSES = ["Present", "Absent", "Late", "Leave"]

    # Week days
    WEEK_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

    # Question types
    QUESTION_TYPES = ["MCQ", "Short", "Long", "Numerical"]

    # Cognitive levels
    COGNITIVE_LEVELS = ["Knowledge", "Understanding", "Application"]

    # Difficulty levels
    DIFFICULTY_LEVELS = ["Easy", "Medium", "Hard"]

    # Payment statuses
    PAYMENT_STATUSES = ["Pending", "Partial", "Paid"]

    # Employment statuses
    EMPLOYMENT_STATUSES = ["Active", "On Leave", "Resigned"]


def ensure_directories():
    """Ensure all required directories exist"""
    dirs = [
        Config.get_app_data_dir(),
        Config.get_app_data_dir() / 'data',
        Config.get_backup_dir(),
        Config.get_reports_dir(),
        Config.get_log_dir()
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)