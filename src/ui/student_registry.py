"""
Student Registry UI Module for School Management System
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit,
    QTableWidget, QTableWidgetItem, QDialog, QFormLayout, QComboBox,
    QDateEdit, QSpinBox, QMessageBox, QHeaderView, QSearchBar
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont, QIcon

from models import Student, Guardian
from repositories import StudentRepository, GuardianRepository, ClassRepository
from datetime import date


class StudentRegistryWidget(QWidget):
    """Main student registry interface"""

    def __init__(self):
        super().__init__()
        self.student_repo = StudentRepository()
        self.guardian_repo = GuardianRepository()
        self.class_repo = ClassRepository()

        self.init_ui()
        self.load_students()

    def init_ui(self):
        """Initialize the student registry interface"""
        layout = QVBoxLayout(self)

        # Header
        header = self.create_header()
        layout.addWidget(header)

        # Search and filter section
        search_section = self.create_search_section()
        layout.addWidget(search_section)

        # Students table
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "ID", "Admission #", "Roll #", "Name", "Class", "Section",
            "DOB", "Status"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)

        # Action buttons
        button_layout = QHBoxLayout()
        self.add_btn = QPushButton("+ Add Student")
        self.add_btn.clicked.connect(self.open_add_dialog)
        button_layout.addWidget(self.add_btn)

        self.edit_btn = QPushButton("✎ Edit")
        self.edit_btn.clicked.connect(self.open_edit_dialog)
        button_layout.addWidget(self.edit_btn)

        self.delete_btn = QPushButton("🗑 Delete")
        self.delete_btn.clicked.connect(self.delete_student)
        button_layout.addWidget(self.delete_btn)

        self.export_btn = QPushButton("📊 Export")
        self.export_btn.clicked.connect(self.export_students)
        button_layout.addWidget(self.export_btn)

        button_layout.addStretch()
        layout.addLayout(button_layout)

    def create_header(self) -> QWidget:
        """Create header section"""
        header = QWidget()
        layout = QHBoxLayout(header)

        title = QLabel("Student Registry")
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        title.setFont(font)

        layout.addWidget(title)
        layout.addStretch()

        count_label = QLabel(f"Total Students: {self.student_repo.get_count()}")
        layout.addWidget(count_label)

        return header

    def create_search_section(self) -> QWidget:
        """Create search and filter section"""
        section = QWidget()
        layout = QHBoxLayout(section)

        layout.addWidget(QLabel("Search:"))
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Name, admission #, or roll #...")
        self.search_box.textChanged.connect(self.search_students)
        layout.addWidget(self.search_box)

        layout.addWidget(QLabel("Class:"))
        self.class_filter = QComboBox()
        self.class_filter.addItem("All Classes")
        classes = self.class_repo.get_all()
        for cls in classes:
            self.class_filter.addItem(cls['name'], cls['id'])
        self.class_filter.currentIndexChanged.connect(self.filter_by_class)
        layout.addWidget(self.class_filter)

        return section

    def load_students(self):
        """Load all students into the table"""
        students = self.student_repo.get_all(limit=100)
        self.populate_table(students)

    def populate_table(self, students):
        """Populate the students table"""
        self.table.setRowCount(len(students))

        for row, student in enumerate(students):
            self.table.setItem(row, 0, QTableWidgetItem(str(student.id or "")))
            self.table.setItem(row, 1, QTableWidgetItem(student.admission_number))
            self.table.setItem(row, 2, QTableWidgetItem(student.roll_number))
            self.table.setItem(row, 3, QTableWidgetItem(student.full_name))
            self.table.setItem(row, 4, QTableWidgetItem(student.class_name))
            self.table.setItem(row, 5, QTableWidgetItem(student.section_name))
            dob = student.date_of_birth.strftime("%Y-%m-%d") if student.date_of_birth else ""
            self.table.setItem(row, 6, QTableWidgetItem(dob))
            self.table.setItem(row, 7, QTableWidgetItem(student.enrollment_status))

    def search_students(self):
        """Search students based on search box input"""
        query = self.search_box.text().strip()
        if query:
            students = self.student_repo.search(query)
            self.populate_table(students)
        else:
            self.load_students()

    def filter_by_class(self):
        """Filter students by selected class"""
        class_id = self.class_filter.currentData()
        if class_id:
            students = self.student_repo.get_by_class(class_id)
            self.populate_table(students)
        else:
            self.load_students()

    def open_add_dialog(self):
        """Open dialog to add a new student"""
        dialog = StudentDialog(self, self.class_repo.get_all())
        if dialog.exec() == QDialog.DialogCode.Accepted:
            student = dialog.get_student()
            errors = student.validate()
            if errors:
                QMessageBox.warning(self, "Validation Error", "\n".join(errors))
                return

            try:
                student_id = self.student_repo.create(student)
                student.id = student_id

                # Add guardians if provided
                guardians = dialog.get_guardians()
                for guardian in guardians:
                    if guardian.full_name:
                        guardian.student_id = student_id
                        self.guardian_repo.create(guardian)

                QMessageBox.information(self, "Success",
                                      f"Student {student.full_name} added successfully!")
                self.load_students()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to add student: {str(e)}")

    def open_edit_dialog(self):
        """Open dialog to edit selected student"""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Selection", "Please select a student to edit")
            return

        student_id = int(self.table.item(current_row, 0).text())
        student = self.student_repo.get_by_id(student_id)

        if not student:
            QMessageBox.warning(self, "Error", "Could not load student data")
            return

        guardians = self.guardian_repo.get_by_student(student_id)
        classes = self.class_repo.get_all()

        dialog = StudentDialog(self, classes, student, guardians)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            updated_student = dialog.get_student()
            errors = updated_student.validate()
            if errors:
                QMessageBox.warning(self, "Validation Error", "\n".join(errors))
                return

            try:
                self.student_repo.update(updated_student)
                QMessageBox.information(self, "Success", "Student updated successfully!")
                self.load_students()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to update student: {str(e)}")

    def delete_student(self):
        """Delete selected student"""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Selection", "Please select a student to delete")
            return

        student_id = int(self.table.item(current_row, 0).text())
        student_name = self.table.item(current_row, 3).text()

        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Mark {student_name} as Struck Off?\nThis is a soft delete (status change).",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.student_repo.delete(student_id)
                QMessageBox.information(self, "Success", "Student marked as Struck Off")
                self.load_students()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete student: {str(e)}")

    def export_students(self):
        """Export students to CSV"""
        try:
            import csv
            from pathlib import Path
            from config import Config

            students = self.student_repo.get_all(limit=1000)
            export_path = Config.get_reports_dir() / "students_export.csv"

            with open(export_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    "ID", "Admission #", "Roll #", "Name", "DOB", "Gender",
                    "Blood Group", "Class", "Section", "Admission Date", "Status"
                ])
                for student in students:
                    writer.writerow([
                        student.id,
                        student.admission_number,
                        student.roll_number,
                        student.full_name,
                        student.date_of_birth or "",
                        student.gender,
                        student.blood_group,
                        student.class_name,
                        student.section_name,
                        student.admission_date,
                        student.enrollment_status
                    ])

            QMessageBox.information(self, "Success",
                                  f"Students exported to:\n{export_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Export failed: {str(e)}")


class StudentDialog(QDialog):
    """Dialog for adding/editing student information"""

    def __init__(self, parent, classes, student=None, guardians=None):
        super().__init__(parent)
        self.setWindowTitle("Student Information")
        self.setMinimumWidth(500)

        self.student = student or Student()
        self.guardians = guardians or []
        self.classes = classes

        self.init_ui()

    def init_ui(self):
        """Initialize dialog UI"""
        layout = QVBoxLayout(self)

        # Student details form
        form_layout = QFormLayout()

        self.admission_edit = QLineEdit()
        self.admission_edit.setText(self.student.admission_number)
        form_layout.addRow("Admission Number:", self.admission_edit)

        self.roll_edit = QLineEdit()
        self.roll_edit.setText(self.student.roll_number)
        form_layout.addRow("Roll Number:", self.roll_edit)

        self.name_edit = QLineEdit()
        self.name_edit.setText(self.student.full_name)
        form_layout.addRow("Full Name:", self.name_edit)

        self.dob_edit = QDateEdit()
        if self.student.date_of_birth:
            self.dob_edit.setDate(QDate(
                self.student.date_of_birth.year,
                self.student.date_of_birth.month,
                self.student.date_of_birth.day
            ))
        form_layout.addRow("Date of Birth:", self.dob_edit)

        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["M", "F", "Other"])
        self.gender_combo.setCurrentText(self.student.gender)
        form_layout.addRow("Gender:", self.gender_combo)

        self.blood_group_combo = QComboBox()
        from config import Config
        self.blood_group_combo.addItems(Config.BLOOD_GROUPS)
        self.blood_group_combo.setCurrentText(self.student.blood_group or "")
        form_layout.addRow("Blood Group:", self.blood_group_combo)

        self.class_combo = QComboBox()
        for cls in self.classes:
            self.class_combo.addItem(cls['name'], cls['id'])
        if self.student.class_id:
            index = self.class_combo.findData(self.student.class_id)
            if index >= 0:
                self.class_combo.setCurrentIndex(index)
        form_layout.addRow("Class:", self.class_combo)

        self.admission_date_edit = QDateEdit()
        if self.student.admission_date:
            self.admission_date_edit.setDate(QDate(
                self.student.admission_date.year,
                self.student.admission_date.month,
                self.student.admission_date.day
            ))
        form_layout.addRow("Admission Date:", self.admission_date_edit)

        layout.addLayout(form_layout)

        # Buttons
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)
        button_layout.addWidget(save_btn)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)

        layout.addLayout(button_layout)

    def get_student(self) -> Student:
        """Get updated student object from form"""
        self.student.admission_number = self.admission_edit.text()
        self.student.roll_number = self.roll_edit.text()
        self.student.full_name = self.name_edit.text()

        dob_qdate = self.dob_edit.date()
        self.student.date_of_birth = date(dob_qdate.year(), dob_qdate.month(), dob_qdate.day())

        self.student.gender = self.gender_combo.currentText()
        self.student.blood_group = self.blood_group_combo.currentText()
        self.student.class_id = self.class_combo.currentData()

        adm_qdate = self.admission_date_edit.date()
        self.student.admission_date = date(adm_qdate.year(), adm_qdate.month(), adm_qdate.day())

        return self.student

    def get_guardians(self) -> list:
        """Get guardians"""
        return self.guardians
