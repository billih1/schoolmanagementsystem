"""
Main entry point for School Management System
"""

import sys
import logging
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from config import Config, ensure_directories
from database import DatabaseManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Config.get_log_dir() / 'app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def main():
    """Application entry point"""
    try:
        # Ensure all directories exist
        ensure_directories()

        logger.info(f"Starting {Config.APP_NAME} v{Config.APP_VERSION}")

        # Initialize database
        db = DatabaseManager()
        db.initialize_schema()
        logger.info(f"Database initialized at: {db.db_path}")

        # Import and start PyQt6 application
        from PyQt6.QtWidgets import QApplication
        from ui.main_window import MainWindow

        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()

        logger.info("Application UI initialized")
        sys.exit(app.exec())

    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
