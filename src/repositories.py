"""
Database repository layer for School Management System
Provides data access layer for all entities
"""

import sqlite3
from typing import List, Optional, Dict, Any
from database import DatabaseManager
from models import Student, Guardian, Staff, User
from datetime import date, datetime
import logging

logger = logging.getLogger(__name__)


class BaseRepository:
    """Base repository with common CRUD operations"""

    def __init__(self):
        self.db = DatabaseManager()

    def execute_query(self, query: str, params: tuple = ()) -> List[sqlite3.Row]:
        """Execute a SELECT query and return results"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()

    def execute_update(self, query: str, params: tuple = ()) -> int:
        """Execute an INSERT/UPDATE/DELETE query and return affected rows"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.rowcount

    def execute_insert(self, query: str, params: tuple = ()) -> int:
        """Execute INSERT and return last row id"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.lastrowid


class StudentRepository(BaseRepository):
    """Repository for student data operations"""

    def create(self, student: Student) -> int:
        """Create a new student record"""
        query = '''
            INSERT INTO students (
                admission_number, roll_number, full_name, date_of_birth,
                gender, blood_group, class_id, section_id, admission_date,
                enrollment_status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        params = (
            student.admission_number,
            student.roll_number,
            student.full_name,
            student.date_of_birth.isoformat() if student.date_of_birth else None,
            student.gender,
            student.blood_group,
            student.class_id,
            student.section_id,
            student.admission_date.isoformat() if student.admission_date else None,
            student.enrollment_status
        )
        return self.execute_insert(query, params)

    def update(self, student: Student) -> bool:
        """Update an existing student record"""
        query = '''
            UPDATE students SET
                admission_number = ?, roll_number = ?, full_name = ?,
                date_of_birth = ?, gender = ?, blood_group = ?,
                class_id = ?, section_id = ?, admission_date = ?,
                enrollment_status = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        '''
        params = (
            student.admission_number,
            student.roll_number,
            student.full_name,
            student.date_of_birth.isoformat() if student.date_of_birth else None,
            student.gender,
            student.blood_group,
            student.class_id,
            student.section_id,
            student.admission_date.isoformat() if student.admission_date else None,
            student.enrollment_status,
            student.id
        )
        return self.execute_update(query, params) > 0

    def delete(self, student_id: int) -> bool:
        """Delete a student record (soft delete via status change)"""
        query = 'UPDATE students SET enrollment_status = ? WHERE id = ?'
        return self.execute_update(query, ('Struck Off', student_id)) > 0

    def get_by_id(self, student_id: int) -> Optional[Student]:
        """Get student by ID"""
        query = 'SELECT * FROM students WHERE id = ?'
        results = self.execute_query(query, (student_id,))
        if results:
            return self._row_to_student(results[0])
        return None

    def get_by_admission_number(self, admission_number: str) -> Optional[Student]:
        """Get student by admission number"""
        query = 'SELECT * FROM students WHERE admission_number = ?'
        results = self.execute_query(query, (admission_number,))
        if results:
            return self._row_to_student(results[0])
        return None

    def get_by_class(self, class_id: int) -> List[Student]:
        """Get all students in a class"""
        query = '''
            SELECT s.*, c.name as class_name, sec.name as section_name
            FROM students s
            JOIN classes c ON s.class_id = c.id
            JOIN sections sec ON s.section_id = sec.id
            WHERE s.class_id = ? AND s.enrollment_status = 'Enrolled'
            ORDER BY s.roll_number
        '''
        results = self.execute_query(query, (class_id,))
        return [self._row_to_student(row) for row in results]

    def get_by_section(self, section_id: int) -> List[Student]:
        """Get all students in a section"""
        query = '''
            SELECT s.*, c.name as class_name, sec.name as section_name
            FROM students s
            JOIN classes c ON s.class_id = c.id
            JOIN sections sec ON s.section_id = sec.id
            WHERE s.section_id = ? AND s.enrollment_status = 'Enrolled'
            ORDER BY s.roll_number
        '''
        results = self.execute_query(query, (section_id,))
        return [self._row_to_student(row) for row in results]

    def get_all(self, limit: int = 100, offset: int = 0) -> List[Student]:
        """Get all students with pagination"""
        query = '''
            SELECT s.*, c.name as class_name, sec.name as section_name
            FROM students s
            JOIN classes c ON s.class_id = c.id
            JOIN sections sec ON s.section_id = sec.id
            WHERE s.enrollment_status = 'Enrolled'
            ORDER BY s.admission_number
            LIMIT ? OFFSET ?
        '''
        results = self.execute_query(query, (limit, offset))
        return [self._row_to_student(row) for row in results]

    def search(self, query_text: str) -> List[Student]:
        """Search students by name, admission number, or roll number"""
        query = '''
            SELECT s.*, c.name as class_name, sec.name as section_name
            FROM students s
            JOIN classes c ON s.class_id = c.id
            JOIN sections sec ON s.section_id = sec.id
            WHERE (s.full_name LIKE ? OR s.admission_number LIKE ? OR s.roll_number LIKE ?)
            AND s.enrollment_status = 'Enrolled'
            ORDER BY s.full_name
            LIMIT 100
        '''
        search_param = f"%{query_text}%"
        results = self.execute_query(query, (search_param, search_param, search_param))
        return [self._row_to_student(row) for row in results]

    def get_count(self) -> int:
        """Get total student count"""
        query = 'SELECT COUNT(*) as count FROM students WHERE enrollment_status = "Enrolled"'
        results = self.execute_query(query)
        return results[0]['count'] if results else 0

    @staticmethod
    def _row_to_student(row: sqlite3.Row) -> Student:
        """Convert database row to Student object"""
        return Student(
            id=row['id'],
            admission_number=row['admission_number'],
            roll_number=row['roll_number'],
            full_name=row['full_name'],
            date_of_birth=date.fromisoformat(row['date_of_birth']) if row['date_of_birth'] else None,
            gender=row['gender'],
            blood_group=row['blood_group'],
            class_id=row['class_id'],
            section_id=row['section_id'],
            admission_date=date.fromisoformat(row['admission_date']) if row['admission_date'] else None,
            enrollment_status=row['enrollment_status'],
            class_name=row.get('class_name', ''),
            section_name=row.get('section_name', '')
        )


class GuardianRepository(BaseRepository):
    """Repository for guardian/parent data operations"""

    def create(self, guardian: Guardian) -> int:
        """Create a new guardian record"""
        query = '''
            INSERT INTO guardians (
                student_id, guardian_type, full_name, national_id,
                primary_phone, secondary_phone, email, address
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        '''
        params = (
            guardian.student_id,
            guardian.guardian_type,
            guardian.full_name,
            guardian.national_id,
            guardian.primary_phone,
            guardian.secondary_phone,
            guardian.email,
            guardian.address
        )
        return self.execute_insert(query, params)

    def update(self, guardian: Guardian) -> bool:
        """Update an existing guardian record"""
        query = '''
            UPDATE guardians SET
                guardian_type = ?, full_name = ?, national_id = ?,
                primary_phone = ?, secondary_phone = ?, email = ?, address = ?
            WHERE id = ?
        '''
        params = (
            guardian.guardian_type,
            guardian.full_name,
            guardian.national_id,
            guardian.primary_phone,
            guardian.secondary_phone,
            guardian.email,
            guardian.address,
            guardian.id
        )
        return self.execute_update(query, params) > 0

    def delete(self, guardian_id: int) -> bool:
        """Delete a guardian record"""
        query = 'DELETE FROM guardians WHERE id = ?'
        return self.execute_update(query, (guardian_id,)) > 0

    def get_by_student(self, student_id: int) -> List[Guardian]:
        """Get all guardians for a student"""
        query = 'SELECT * FROM guardians WHERE student_id = ? ORDER BY guardian_type'
        results = self.execute_query(query, (student_id,))
        return [self._row_to_guardian(row) for row in results]

    @staticmethod
    def _row_to_guardian(row: sqlite3.Row) -> Guardian:
        """Convert database row to Guardian object"""
        return Guardian(
            id=row['id'],
            student_id=row['student_id'],
            guardian_type=row['guardian_type'],
            full_name=row['full_name'],
            national_id=row['national_id'],
            primary_phone=row['primary_phone'],
            secondary_phone=row['secondary_phone'],
            email=row['email'],
            address=row['address']
        )


class StaffRepository(BaseRepository):
    """Repository for staff/employee data operations"""

    def create(self, staff: Staff) -> int:
        """Create a new staff record"""
        query = '''
            INSERT INTO staff (
                employee_code, full_name, designation, email,
                primary_phone, secondary_phone, date_of_joining,
                employment_status, max_periods_per_week
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        params = (
            staff.employee_code,
            staff.full_name,
            staff.designation,
            staff.email,
            staff.primary_phone,
            staff.secondary_phone,
            staff.date_of_joining.isoformat() if staff.date_of_joining else None,
            staff.employment_status,
            staff.max_periods_per_week
        )
        return self.execute_insert(query, params)

    def get_all(self) -> List[Staff]:
        """Get all staff members"""
        query = '''
            SELECT * FROM staff
            WHERE employment_status = 'Active'
            ORDER BY full_name
        '''
        results = self.execute_query(query)
        return [self._row_to_staff(row) for row in results]

    @staticmethod
    def _row_to_staff(row: sqlite3.Row) -> Staff:
        """Convert database row to Staff object"""
        return Staff(
            id=row['id'],
            employee_code=row['employee_code'],
            full_name=row['full_name'],
            designation=row['designation'],
            email=row['email'],
            primary_phone=row['primary_phone'],
            secondary_phone=row['secondary_phone'],
            date_of_joining=date.fromisoformat(row['date_of_joining']) if row['date_of_joining'] else None,
            employment_status=row['employment_status'],
            max_periods_per_week=row['max_periods_per_week']
        )


class ClassRepository(BaseRepository):
    """Repository for class/grade operations"""

    def create(self, name: str, grade_level: int) -> int:
        """Create a new class"""
        query = 'INSERT INTO classes (name, grade_level) VALUES (?, ?)'
        return self.execute_insert(query, (name, grade_level))

    def get_all(self) -> List[Dict[str, Any]]:
        """Get all classes"""
        query = 'SELECT * FROM classes ORDER BY grade_level, name'
        results = self.execute_query(query)
        return [dict(row) for row in results]

    def get_sections(self, class_id: int) -> List[Dict[str, Any]]:
        """Get all sections for a class"""
        query = 'SELECT * FROM sections WHERE class_id = ? ORDER BY name'
        results = self.execute_query(query, (class_id,))
        return [dict(row) for row in results]


if __name__ == "__main__":
    # Test repositories
    print("Repository module loaded successfully")
