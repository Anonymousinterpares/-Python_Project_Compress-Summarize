import unittest
import os
import sys
from utils.file_utils import get_base_dir
from utils.log_utils import setup_logging

class TestUtils(unittest.TestCase):
    """
    Unit tests for the utils module.
    """

    def test_get_base_dir(self):
        """
        Test the get_base_dir function.
        """
        # Test when running as a script
        base_dir = get_base_dir()
        self.assertEqual(base_dir, os.path.dirname(os.path.abspath(__file__)))

        # Test when running as a frozen executable
        sys.frozen = True
        sys._MEIPASS = "/tmp/test_meipass"
        base_dir = get_base_dir()
        self.assertEqual(base_dir, "/tmp/test_meipass")
        del sys.frozen
        del sys._MEIPASS

    def test_setup_logging(self):
        """
        Test the setup_logging function.
        """
        # Call the setup_logging function
        setup_logging()

        # Check if the log file was created
        log_file = os.path.join(get_base_dir(), "logs", "dev_manager.log")
        self.assertTrue(os.path.exists(log_file))

if __name__ == '__main__':
    unittest.main()
