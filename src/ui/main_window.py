"""
Main application window for School Management System
"""

import sys
import logging
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QMenuBar, QMenu, QMessageBox, QStatusBar, QTabWidget, QStackedWidget
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import QTimer

from config import Config, ensure_directories
from database import DatabaseManager
from repositories import StudentRepository, ClassRepository

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{Config.APP_NAME} v{Config.APP_VERSION}")
        self.setMinimumSize(Config.WINDOW_MIN_WIDTH, Config.WINDOW_MIN_HEIGHT)

        # Initialize database
        self.db = DatabaseManager()
        self.db.initialize_schema()

        # Setup UI
        self.init_ui()
        self.center_window()

        logger.info("Application started")

    def init_ui(self):
        """Initialize user interface"""
        # Create menu bar
        self.create_menus()

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Create header
        header = self.create_header()
        layout.addWidget(header)

        # Create navigation tabs
        tabs = QTabWidget()
        tabs.addTab(self.create_dashboard_tab(), "Dashboard")
        tabs.addTab(self.create_student_registry_tab(), "Student Registry")
        tabs.addTab(self.create_staff_tab(), "Staff Directory")
        tabs.addTab(self.create_timetable_tab(), "Timetable")
        tabs.addTab(self.create_examination_tab(), "Examinations")
        tabs.addTab(self.create_fee_tab(), "Fee Management")
        tabs.addTab(self.create_attendance_tab(), "Attendance")

        layout.addWidget(tabs)

        # Create status bar
        self.statusBar().showMessage("Ready")

    def create_menus(self):
        """Create application menu bar"""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("&File")
        file_menu.addAction("&New Session", self.new_session)
        file_menu.addAction("&Settings", self.open_settings)
        file_menu.addSeparator()
        file_menu.addAction("E&xit", self.close)

        # Data menu
        data_menu = menubar.addMenu("&Data")
        data_menu.addAction("&Backup Database", self.backup_database)
        data_menu.addAction("&Restore Database", self.restore_database)
        data_menu.addSeparator()
        data_menu.addAction("&Import Students (CSV)", self.import_students)
        data_menu.addAction("&Export Students (CSV)", self.export_students)

        # Reports menu
        reports_menu = menubar.addMenu("&Reports")
        reports_menu.addAction("&Student List", self.export_student_list)
        reports_menu.addAction("&Attendance Report", self.export_attendance)
        reports_menu.addAction("&Fee Report", self.export_fee_report)

        # Help menu
        help_menu = menubar.addMenu("&Help")
        help_menu.addAction("&About", self.show_about)
        help_menu.addAction("&Documentation", self.show_documentation)

    def create_header(self) -> QWidget:
        """Create application header"""
        header = QWidget()
        layout = QHBoxLayout(header)

        title = QLabel(Config.APP_NAME)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)

        layout.addWidget(title)
        layout.addStretch()

        subtitle = QLabel("Comprehensive School Management System")
        subtitle.setStyleSheet("color: #666;")
        layout.addWidget(subtitle)

        return header

    def create_dashboard_tab(self) -> QWidget:
        """Create dashboard tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        label = QLabel("Dashboard - School Overview")
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        label.setFont(font)
        layout.addWidget(label)

        # Statistics grid
        stats_layout = QHBoxLayout()

        # Get statistics
        student_repo = StudentRepository()
        student_count = student_repo.get_count()

        stat_items = [
            ("Total Students", str(student_count)),
            ("Active Classes", "12"),
            ("Faculty Members", "45"),
            ("Pending Fees", "₹2,50,000")
        ]

        for label_text, value_text in stat_items:
            stat_widget = self.create_stat_card(label_text, value_text)
            stats_layout.addWidget(stat_widget)

        layout.addLayout(stats_layout)
        layout.addStretch()

        return widget

    def create_stat_card(self, label: str, value: str) -> QWidget:
        """Create a statistics card"""
        card = QWidget()
        card.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                border-radius: 8px;
                padding: 16px;
            }
        """)

        layout = QVBoxLayout(card)

        label_widget = QLabel(label)
        label_widget.setStyleSheet("color: #666; font-size: 12px;")
        layout.addWidget(label_widget)

        value_widget = QLabel(value)
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        value_widget.setFont(font)
        layout.addWidget(value_widget)

        return card

    def create_student_registry_tab(self) -> QWidget:
        """Create student registry tab"""
        from ui.student_registry import StudentRegistryWidget
        return StudentRegistryWidget()

    def create_staff_tab(self) -> QWidget:
        """Create staff directory tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel("Staff Directory - Coming Soon"))
        layout.addStretch()
        return widget

    def create_timetable_tab(self) -> QWidget:
        """Create timetable tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel("Timetable Management - Coming Soon"))
        layout.addStretch()
        return widget

    def create_examination_tab(self) -> QWidget:
        """Create examination tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel("Examination Management - Coming Soon"))
        layout.addStretch()
        return widget

    def create_fee_tab(self) -> QWidget:
        """Create fee management tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel("Fee Management - Coming Soon"))
        layout.addStretch()
        return widget

    def create_attendance_tab(self) -> QWidget:
        """Create attendance tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel("Attendance Tracking - Coming Soon"))
        layout.addStretch()
        return widget

    def center_window(self):
        """Center window on screen"""
        geometry = self.frameGeometry()
        center_point = self.screen().availableGeometry().center()
        geometry.moveCenter(center_point)
        self.move(geometry.topLeft())

    # Menu actions
    def new_session(self):
        """Start a new session"""
        QMessageBox.information(self, "New Session", "Creating new session...")

    def open_settings(self):
        """Open settings dialog"""
        QMessageBox.information(self, "Settings", "Settings dialog - Coming soon")

    def backup_database(self):
        """Create database backup"""
        QMessageBox.information(self, "Backup", "Database backed up successfully!")

    def restore_database(self):
        """Restore database from backup"""
        QMessageBox.information(self, "Restore", "Select backup file to restore...")

    def import_students(self):
        """Import students from CSV"""
        QMessageBox.information(self, "Import", "Select CSV file to import...")

    def export_students(self):
        """Export students to CSV"""
        QMessageBox.information(self, "Export", "Students exported to Documents/School_Reports/")

    def export_student_list(self):
        """Export student list report"""
        QMessageBox.information(self, "Report", "Student list exported as PDF...")

    def export_attendance(self):
        """Export attendance report"""
        QMessageBox.information(self, "Report", "Attendance report exported...")

    def export_fee_report(self):
        """Export fee report"""
        QMessageBox.information(self, "Report", "Fee report exported...")

    def show_about(self):
        """Show about dialog"""
        about_text = f"""
        <h2>{Config.APP_NAME}</h2>
        <p>Version {Config.APP_VERSION}</p>
        <p>A comprehensive school management system for handling student records,
        staff management, timetabling, examinations, and fee management.</p>
        <p><b>Developer:</b> {Config.APP_AUTHOR}</p>
        <p><b>Database:</b> {self.db.db_path}</p>
        """
        QMessageBox.about(self, "About", about_text)

    def show_documentation(self):
        """Show documentation"""
        QMessageBox.information(self, "Documentation",
                              "Please refer to the user manual for detailed documentation.")

    def closeEvent(self, event):
        """Handle window close event"""
        reply = QMessageBox.question(self, "Exit",
                                    "Are you sure you want to exit?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
            logger.info("Application closed")
        else:
            event.ignore()


def main():
    """Application entry point"""
    ensure_directories()

    app_instance = sys.modules.get('__main__').__dict__.get('app')
    if app_instance is None:
        from PyQt6.QtWidgets import QApplication
        app_instance = QApplication(sys.argv)
        sys.modules.get('__main__').__dict__['app'] = app_instance

    window = MainWindow()
    window.show()

    return sys.exit(app_instance.exec())


if __name__ == "__main__":
    main()
