"""
Database module for School Management System
Handles SQLite database initialization, connection, and schema creation
"""

import sqlite3
import os
from pathlib import Path
from contextlib import contextmanager
import logging

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages SQLite database for School Management System"""

    def __init__(self):
        """Initialize database manager and ensure data directory exists"""
        self.db_path = self._get_db_path()
        self._ensure_db_directory()

    @staticmethod
    def _get_db_path():
        """Get database path based on OS"""
        if os.name == 'nt':  # Windows
            app_data = os.getenv('LOCALAPPDATA')
            db_dir = Path(app_data) / 'SchoolManagementSystem' / 'data'
        else:
            db_dir = Path.home() / '.SchoolManagementSystem' / 'data'
        return db_dir / 'school.db'

    def _ensure_db_directory(self):
        """Create database directory if it doesn't exist"""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    @contextmanager
    def get_connection(self):
        """Context manager for database connections with WAL mode"""
        conn = sqlite3.connect(str(self.db_path))
        conn.execute('PRAGMA journal_mode=WAL')
        conn.execute('PRAGMA foreign_keys=ON')
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            conn.close()

    def initialize_schema(self):
        """Create all database tables if they don't exist"""
        with self.get_connection() as conn:
            self._create_institution_table(conn)
            self._create_users_table(conn)
            self._create_classes_table(conn)
            self._create_sections_table(conn)
            self._create_students_table(conn)
            self._create_guardians_table(conn)
            self._create_staff_table(conn)
            self._create_attendance_table(conn)
            self._create_fee_structure_table(conn)
            self._create_invoices_table(conn)
            self._create_timetable_table(conn)
            self._create_questions_table(conn)
            self._create_exam_papers_table(conn)
            self._create_exam_results_table(conn)
            self._create_audit_log_table(conn)
            self._create_backup_metadata_table(conn)

    @staticmethod
    def _create_institution_table(conn):
        """Create institution/school configuration table"""
        conn.execute('''
            CREATE TABLE IF NOT EXISTS institution (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                address TEXT,
                contact_phone TEXT,
                contact_email TEXT,
                logo_path TEXT,
                motto TEXT,
                academic_session_start DATE,
                academic_session_end DATE,
                grading_scale TEXT DEFAULT 'standard',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

    @staticmethod
    def _create_users_table(conn):
        """Create user accounts table with RBAC"""
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('admin', 'accountant', 'teacher', 'clerk')),
                email TEXT,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            )
        ''')

    @staticmethod
    def _create_classes_table(conn):
        """Create grade/class table"""
        conn.execute('''
            CREATE TABLE IF NOT EXISTS classes (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                grade_level INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(name, grade_level)
            )
        ''')

    @staticmethod
    def _create_sections_table(conn):
        """Create section table"""
        conn.execute('''
            CREATE TABLE IF NOT EXISTS sections (
                id INTEGER PRIMARY KEY,
                class_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                class_room TEXT,
                capacity INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(class_id) REFERENCES classes(id),
                UNIQUE(class_id, name)
            )
        ''')

    @staticmethod
    def _create_students_table(conn):
        """Create student registry table"""
        conn.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY,
                admission_number TEXT UNIQUE NOT NULL,
                roll_number TEXT,
                full_name TEXT NOT NULL,
                date_of_birth DATE,
                gender TEXT CHECK(gender IN ('M', 'F', 'Other')),
                blood_group TEXT,
                class_id INTEGER NOT NULL,
                section_id INTEGER NOT NULL,
                admission_date DATE NOT NULL,
                enrollment_status TEXT DEFAULT 'Enrolled'
                    CHECK(enrollment_status IN ('Enrolled', 'Suspended', 'Struck Off', 'Graduated', 'Alumni')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(class_id) REFERENCES classes(id),
                FOREIGN KEY(section_id) REFERENCES sections(id)
            )
        ''')

    @staticmethod
    def _create_guardians_table(conn):
        """Create guardian/parent table"""
        conn.execute('''
            CREATE TABLE IF NOT EXISTS guardians (
                id INTEGER PRIMARY KEY,
                student_id INTEGER NOT NULL,
                guardian_type TEXT NOT NULL CHECK(guardian_type IN ('Father', 'Mother', 'Other')),
                full_name TEXT NOT NULL,
                national_id TEXT,
                primary_phone TEXT NOT NULL,
                secondary_phone TEXT,
                email TEXT,
                address TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(student_id) REFERENCES students(id),
                UNIQUE(student_id, guardian_type)
            )
        ''')

    @staticmethod
    def _create_staff_table(conn):
        """Create staff/employee directory table"""
        conn.execute('''
            CREATE TABLE IF NOT EXISTS staff (
                id INTEGER PRIMARY KEY,
                employee_code TEXT UNIQUE NOT NULL,
                full_name TEXT NOT NULL,
                designation TEXT NOT NULL,
                email TEXT,
                primary_phone TEXT,
                secondary_phone TEXT,
                date_of_joining DATE NOT NULL,
                employment_status TEXT DEFAULT 'Active'
                    CHECK(employment_status IN ('Active', 'On Leave', 'Resigned')),
                max_periods_per_week INTEGER DEFAULT 30,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

    @staticmethod
    def _create_attendance_table(conn):
        """Create attendance tracking table"""
        conn.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY,
                student_id INTEGER NOT NULL,
                attendance_date DATE NOT NULL,
                status TEXT NOT NULL CHECK(status IN ('Present', 'Absent', 'Late', 'Leave')),
                remarks TEXT,
                marked_by INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(student_id) REFERENCES students(id),
                FOREIGN KEY(marked_by) REFERENCES users(id),
                UNIQUE(student_id, attendance_date)
            )
        ''')

    @staticmethod
    def _create_fee_structure_table(conn):
        """Create fee structure configuration table"""
        conn.execute('''
            CREATE TABLE IF NOT EXISTS fee_structure (
                id INTEGER PRIMARY KEY,
                class_id INTEGER NOT NULL,
                tuition_fee DECIMAL(10, 2),
                lab_fee DECIMAL(10, 2),
                sports_fund DECIMAL(10, 2),
                admission_fee DECIMAL(10, 2),
                other_fees DECIMAL(10, 2),
                total_monthly DECIMAL(10, 2),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(class_id) REFERENCES classes(id),
                UNIQUE(class_id)
            )
        ''')

    @staticmethod
    def _create_invoices_table(conn):
        """Create fee invoices/billing table"""
        conn.execute('''
            CREATE TABLE IF NOT EXISTS invoices (
                id INTEGER PRIMARY KEY,
                invoice_number TEXT UNIQUE NOT NULL,
                student_id INTEGER NOT NULL,
                billing_month TEXT NOT NULL,
                billing_year INTEGER NOT NULL,
                due_date DATE,
                total_amount DECIMAL(10, 2),
                arrears DECIMAL(10, 2) DEFAULT 0,
                discount DECIMAL(10, 2) DEFAULT 0,
                net_amount DECIMAL(10, 2),
                payment_status TEXT DEFAULT 'Pending'
                    CHECK(payment_status IN ('Pending', 'Partial', 'Paid')),
                amount_paid DECIMAL(10, 2) DEFAULT 0,
                payment_date DATE,
                receipt_number TEXT,
                created_by INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(student_id) REFERENCES students(id),
                FOREIGN KEY(created_by) REFERENCES users(id),
                UNIQUE(student_id, billing_month, billing_year)
            )
        ''')

    @staticmethod
    def _create_timetable_table(conn):
        """Create timetable/schedule table"""
        conn.execute('''
            CREATE TABLE IF NOT EXISTS timetable (
                id INTEGER PRIMARY KEY,
                section_id INTEGER NOT NULL,
                day_of_week TEXT NOT NULL,
                period_number INTEGER NOT NULL,
                period_start_time TIME NOT NULL,
                period_end_time TIME NOT NULL,
                subject TEXT NOT NULL,
                staff_id INTEGER NOT NULL,
                classroom TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(section_id) REFERENCES sections(id),
                FOREIGN KEY(staff_id) REFERENCES staff(id),
                UNIQUE(section_id, day_of_week, period_number)
            )
        ''')

    @staticmethod
    def _create_questions_table(conn):
        """Create question bank table"""
        conn.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY,
                subject TEXT NOT NULL,
                grade_level INTEGER NOT NULL,
                chapter_unit TEXT NOT NULL,
                topic TEXT NOT NULL,
                question_text TEXT NOT NULL,
                question_type TEXT NOT NULL
                    CHECK(question_type IN ('MCQ', 'Short', 'Long', 'Numerical')),
                cognitive_level TEXT CHECK(cognitive_level IN ('Knowledge', 'Understanding', 'Application')),
                difficulty_level TEXT CHECK(difficulty_level IN ('Easy', 'Medium', 'Hard')),
                marks INTEGER,
                expected_time_minutes INTEGER,
                correct_option TEXT,
                explanation_solution TEXT,
                created_by INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(created_by) REFERENCES users(id)
            )
        ''')

    @staticmethod
    def _create_exam_papers_table(conn):
        """Create exam papers table"""
        conn.execute('''
            CREATE TABLE IF NOT EXISTS exam_papers (
                id INTEGER PRIMARY KEY,
                exam_code TEXT UNIQUE NOT NULL,
                subject TEXT NOT NULL,
                grade_level INTEGER NOT NULL,
                class_id INTEGER NOT NULL,
                section_id INTEGER NOT NULL,
                chapters_covered TEXT,
                total_marks INTEGER,
                total_duration_minutes INTEGER,
                paper_variant CHAR(1),
                question_configuration TEXT,
                exam_date DATE,
                created_by INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(class_id) REFERENCES classes(id),
                FOREIGN KEY(section_id) REFERENCES sections(id),
                FOREIGN KEY(created_by) REFERENCES users(id)
            )
        ''')

    @staticmethod
    def _create_exam_results_table(conn):
        """Create examination results/marks table"""
        conn.execute('''
            CREATE TABLE IF NOT EXISTS exam_results (
                id INTEGER PRIMARY KEY,
                student_id INTEGER NOT NULL,
                exam_paper_id INTEGER NOT NULL,
                subject TEXT NOT NULL,
                marks_obtained DECIMAL(5, 2),
                total_marks INTEGER,
                percentage DECIMAL(5, 2),
                grade TEXT,
                gpa DECIMAL(3, 2),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(student_id) REFERENCES students(id),
                FOREIGN KEY(exam_paper_id) REFERENCES exam_papers(id),
                UNIQUE(student_id, exam_paper_id, subject)
            )
        ''')

    @staticmethod
    def _create_audit_log_table(conn):
        """Create audit trail table for critical operations"""
        conn.execute('''
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                action TEXT NOT NULL,
                table_name TEXT,
                record_id INTEGER,
                old_values TEXT,
                new_values TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')

    @staticmethod
    def _create_backup_metadata_table(conn):
        """Create backup metadata table"""
        conn.execute('''
            CREATE TABLE IF NOT EXISTS backup_metadata (
                id INTEGER PRIMARY KEY,
                backup_filename TEXT UNIQUE NOT NULL,
                backup_size INTEGER,
                backup_location TEXT,
                created_by INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                restored_at TIMESTAMP,
                FOREIGN KEY(created_by) REFERENCES users(id)
            )
        ''')


if __name__ == "__main__":
    # Test database initialization
    db = DatabaseManager()
    db.initialize_schema()
    print(f"Database initialized at: {db.db_path}")
