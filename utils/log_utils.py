import logging
import os
import tempfile
from utils.file_utils import get_base_dir  # Import the missing function

def setup_logging():
    """Sets up logging configuration for the application.
    Creates a logs directory if it doesn't exist and configures both file and console logging."""
    log_dir = os.path.join(get_base_dir(), "logs")
    try:
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
    except Exception as e:
        print(f"Error creating logs directory: {e}")
        # Fallback to using a temporary directory if creating 'logs' fails
        log_dir = os.path.join(tempfile.gettempdir(), "ProjectManager_logs")
        if not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
        print(f"Using temporary directory for logs: {log_dir}")

    log_file = os.path.join(log_dir, "dev_manager.log")

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    # Add a StreamHandler to output logs to the console as well
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)  # Set the level for console output
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    print(f"Logging setup complete. Log file: {log_file}")
