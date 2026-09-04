"""
Student data model for School Management System
"""

from dataclasses import dataclass, field
from datetime import date
from typing import Optional
import re


@dataclass
class Student:
    """Student data model representing a student record"""
    id: Optional[int] = None
    admission_number: str = ""
    roll_number: str = ""
    full_name: str = ""
    date_of_birth: Optional[date] = None
    gender: str = "M"  # M, F, Other
    blood_group: str = ""
    class_id: int = 0
    section_id: int = 0
    admission_date: date = field(default_factory=date.today)
    enrollment_status: str = "Enrolled"  # Enrolled, Suspended, Struck Off, Graduated, Alumni

    # Transient properties (not stored directly)
    class_name: str = ""
    section_name: str = ""

    def validate(self) -> list:
        """Validate student data and return list of errors"""
        errors = []

        if not self.admission_number.strip():
            errors.append("Admission number is required")
        if not self.full_name.strip():
            errors.append("Full name is required")
        if not self.class_id:
            errors.append("Class must be assigned")
        if not self.section_id:
            errors.append("Section must be assigned")
        if self.date_of_birth and self.date_of_birth > date.today():
            errors.append("Date of birth cannot be in the future")
        if self.admission_date > date.today():
            errors.append("Admission date cannot be in the future")

        return errors

    def to_dict(self) -> dict:
        """Convert to dictionary for database operations"""
        return {
            "id": self.id,
            "admission_number": self.admission_number,
            "roll_number": self.roll_number,
            "full_name": self.full_name,
            "date_of_birth": self.date_of_birth.isoformat() if self.date_of_birth else None,
            "gender": self.gender,
            "blood_group": self.blood_group,
            "class_id": self.class_id,
            "section_id": self.section_id,
            "admission_date": self.admission_date.isoformat() if self.admission_date else None,
            "enrollment_status": self.enrollment_status
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Student':
        """Create Student instance from dictionary"""
        dob = None
        if data.get("date_of_birth"):
            try:
                dob = date.fromisoformat(data["date_of_birth"])
            except ValueError:
                pass

        adm_date = None
        if data.get("admission_date"):
            try:
                adm_date = date.fromisoformat(data["admission_date"])
            except ValueError:
                pass

        return cls(
            id=data.get("id"),
            admission_number=data.get("admission_number", ""),
            roll_number=data.get("roll_number", ""),
            full_name=data.get("full_name", ""),
            date_of_birth=dob,
            gender=data.get("gender", "M"),
            blood_group=data.get("blood_group", ""),
            class_id=data.get("class_id", 0),
            section_id=data.get("section_id", 0),
            admission_date=adm_date or date.today(),
            enrollment_status=data.get("enrollment_status", "Enrolled")
        )


@dataclass
class Guardian:
    """Guardian data model representing parent/guardian record"""
    id: Optional[int] = None
    student_id: int = 0
    guardian_type: str = "Father"  # Father, Mother, Other
    full_name: str = ""
    national_id: str = ""
    primary_phone: str = ""
    secondary_phone: str = ""
    email: str = ""
    address: str = ""

    def validate(self) -> list:
        """Validate guardian data and return list of errors"""
        errors = []

        if not self.full_name.strip():
            errors.append("Guardian name is required")
        if not self.primary_phone.strip():
            errors.append("Primary phone is required")

        # Validate phone format (basic)
        if self.primary_phone and not re.match(r'^[\d\s\-+()]{7,20}$', self.primary_phone):
            errors.append("Invalid primary phone format")

        if self.secondary_phone and not re.match(r'^[\d\s\-+()]{7,20}$', self.secondary_phone):
            errors.append("Invalid secondary phone format")

        # Validate email if provided
        if self.email and not re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', self.email):
            errors.append("Invalid email format")

        return errors

    def to_dict(self) -> dict:
        """Convert to dictionary for database operations"""
        return {
            "id": self.id,
            "student_id": self.student_id,
            "guardian_type": self.guardian_type,
            "full_name": self.full_name,
            "national_id": self.national_id,
            "primary_phone": self.primary_phone,
            "secondary_phone": self.secondary_phone,
            "email": self.email,
            "address": self.address
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Guardian':
        """Create Guardian instance from dictionary"""
        return cls(
            id=data.get("id"),
            student_id=data.get("student_id", 0),
            guardian_type=data.get("guardian_type", "Father"),
            full_name=data.get("full_name", ""),
            national_id=data.get("national_id", ""),
            primary_phone=data.get("primary_phone", ""),
            secondary_phone=data.get("secondary_phone", ""),
            email=data.get("email", ""),
            address=data.get("address", "")
        )