"""
Staff data model for School Management System
"""

from dataclasses import dataclass, field
from datetime import date
from typing import Optional


@dataclass
class Staff:
    """Staff/Employee data model"""
    id: Optional[int] = None
    employee_code: str = ""
    full_name: str = ""
    designation: str = ""  # Principal, Subject Specialist, Senior Teacher, Clerk, Accountant
    email: str = ""
    primary_phone: str = ""
    secondary_phone: str = ""
    date_of_joining: date = field(default_factory=date.today)
    employment_status: str = "Active"  # Active, On Leave, Resigned
    max_periods_per_week: int = 30

    def validate(self) -> list:
        """Validate staff data and return list of errors"""
        errors = []

        if not self.employee_code.strip():
            errors.append("Employee code is required")
        if not self.full_name.strip():
            errors.append("Full name is required")
        if not self.designation.strip():
            errors.append("Designation is required")
        if not self.primary_phone.strip():
            errors.append("Primary phone is required")
        if self.date_of_joining > date.today():
            errors.append("Date of joining cannot be in the future")
        if self.max_periods_per_week < 0 or self.max_periods_per_week > 60:
            errors.append("Max periods per week must be between 0 and 60")

        return errors

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "employee_code": self.employee_code,
            "full_name": self.full_name,
            "designation": self.designation,
            "email": self.email,
            "primary_phone": self.primary_phone,
            "secondary_phone": self.secondary_phone,
            "date_of_joining": self.date_of_joining.isoformat() if self.date_of_joining else None,
            "employment_status": self.employment_status,
            "max_periods_per_week": self.max_periods_per_week
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Staff':
        """Create Staff instance from dictionary"""
        doj = None
        if data.get("date_of_joining"):
            try:
                doj = date.fromisoformat(data["date_of_joining"])
            except ValueError:
                pass

        return cls(
            id=data.get("id"),
            employee_code=data.get("employee_code", ""),
            full_name=data.get("full_name", ""),
            designation=data.get("designation", ""),
            email=data.get("email", ""),
            primary_phone=data.get("primary_phone", ""),
            secondary_phone=data.get("secondary_phone", ""),
            date_of_joining=doj or date.today(),
            employment_status=data.get("employment_status", "Active"),
            max_periods_per_week=data.get("max_periods_per_week", 30)
        )


@dataclass
class User:
    """User account model for authentication"""
    id: Optional[int] = None
    username: str = ""
    password_hash: str = ""
    full_name: str = ""
    role: str = "clerk"  # admin, accountant, teacher, clerk
    email: str = ""
    is_active: bool = True
    created_at: Optional[date] = None
    last_login: Optional[date] = None

    def validate(self) -> list:
        """Validate user data and return list of errors"""
        errors = []

        if not self.username.strip():
            errors.append("Username is required")
        if not self.password_hash.strip() and not self.id:
            errors.append("Password is required for new users")
        if not self.full_name.strip():
            errors.append("Full name is required")
        if self.role not in ('admin', 'accountant', 'teacher', 'clerk'):
            errors.append("Invalid role specified")

        return errors

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "username": self.username,
            "password_hash": self.password_hash,
            "full_name": self.full_name,
            "role": self.role,
            "email": self.email,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_login": self.last_login.isoformat() if self.last_login else None
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """Create User instance from dictionary"""
        return cls(
            id=data.get("id"),
            username=data.get("username", ""),
            password_hash=data.get("password_hash", ""),
            full_name=data.get("full_name", ""),
            role=data.get("role", "clerk"),
            email=data.get("email", ""),
            is_active=data.get("is_active", True),
            created_at=data.get("created_at"),
            last_login=data.get("last_login")
        )