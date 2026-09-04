# School Management System

A comprehensive, fully offline desktop application for managing all aspects of school operations including student registry, staff management, timetabling, examinations, fee management, and attendance tracking.

## Project Structure

```
SchoolManagementSystem/
├── src/
│   ├── main.py                 # Application entry point
│   ├── config.py               # Configuration and constants
│   ├── database.py             # SQLite database engine
│   ├── models/
│   │   ├── __init__.py
│   │   ├── student.py          # Student data model
│   │   ├── staff.py            # Staff data model
│   │   ├── timetable.py        # Timetable model
│   │   ├── examination.py      # Exam and question bank
│   │   ├── fee.py              # Fee management
│   │   └── attendance.py       # Attendance tracking
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── main_window.py      # Main application window
│   │   ├── student_registry.py # Student registry UI
│   │   ├── staff_directory.py  # Staff management UI
│   │   ├── timetable_ui.py     # Timetable UI
│   │   ├── exam_ui.py          # Examination UI
│   │   ├── fee_ui.py           # Fee management UI
│   │   └── attendance_ui.py    # Attendance UI
│   ├── services/
│   │   ├── __init__.py
│   │   ├── ranking_service.py  # Ranking calculations
│   │   ├── pdf_service.py      # PDF generation
│   │   ├── backup_service.py   # Backup/restore
│   │   └── validation.py       # Data validation
│   └── utils/
│       ├── __init__.py
│       ├── constants.py
│       └── helpers.py
├── resources/
│   ├── school_logo.png         # School logo (placeholder)
│   └── styles.qss              # Custom PyQt6 styles
├── installer/
│   └── SchoolManagementSystem.iss  # Inno Setup script
├── requirements.txt            # Python dependencies
├── build_installer.py          # Build script for .exe and installer
└── README.md
```

## Technology Stack

- **UI Framework**: PyQt6
- **Database**: SQLite3 with WAL mode
- **PDF Generation**: ReportLab
- **Installer**: Inno Setup
- **Python Version**: 3.10+

## Installation & Setup

### Development Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run application in dev mode
python src/main.py
```

### Building Installer

```bash
# Build executable and installer
python build_installer.py
```

This generates:
- `dist/SchoolManagementSystem.exe` (standalone executable)
- `dist/SchoolManagementSystem_Setup.exe` (installer)

## Key Features

1. **Student Registry** - Complete student lifecycle management
2. **Staff Directory** - Employee profiles and workload tracking
3. **Automated Timetabling** - Conflict resolution and schedule export
4. **Question Bank** - Automated exam paper generation with variants
5. **Examination Management** - Marks entry, ranking, result cards
6. **Fee Management** - Bulk invoicing with arrears tracking
7. **Attendance Tracking** - Daily logs with chronic absenteeism alerts
8. **RBAC** - Role-based access control for Admin, Accountant, Teacher, Clerk
9. **Backup/Restore** - One-click backup with restore capability
10. **PDF Exports** - Professional reports, timetables, vouchers

## Database Location

- **Windows**: `%LOCALAPPDATA%\SchoolManagementSystem\data\school.db`
- **Backup Location**: `%LOCALAPPDATA%\SchoolManagementSystem\backups\`
- **Reports Export**: `%USERPROFILE%\Documents\School_Reports\` (configurable)

## License

Internal Use Only
