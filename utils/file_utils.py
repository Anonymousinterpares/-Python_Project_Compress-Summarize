import sys
import os

def get_base_dir():
    """
    Determine the base directory of the application.

    This function checks if the application is running as a bundled executable
    (e.g., created with PyInstaller) or as a regular Python script. It returns
    the appropriate base directory path.

    Returns:
        str: The base directory path.
    """
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # Running as bundled executable
        return sys._MEIPASS
    else:
        # Running as a script
        return os.path.dirname(os.path.abspath(__file__))
