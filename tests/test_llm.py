import unittest
from PyQt5.QtWidgets import QApplication, QMainWindow
from llm.llm_manager import generate_llm_documentation, call_openai_api, call_google_api
from gui.layout import init_project_manager_ui
import os

class TestLLM(unittest.TestCase):
    """
    Unit tests for the LLM module.
    """
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])

    @classmethod
    def tearDownClass(cls):
        cls.app.quit()

    def setUp(self):
        """
        Set up test fixtures (if any).
        """
        self.main_window = QMainWindow()
        self.main_window.api_settings = {
            "openai": {
                "api_key": "YOUR_OPENAI_API_KEY",  # Replace with your actual API key for testing
                "model": "gpt-3.5-turbo",
                "temperature": 0.7
            },
            "google": {
                "api_key": "YOUR_GOOGLE_API_KEY",  # Replace with your actual API key for testing
                "model": "models/gemini-pro",
                "temperature": 0.7
            }
        }
        self.main_window.openai_radio = None
        self.main_window.google_radio = None
        self.main_window.general_radio = None
        self.main_window.detailed_radio = None
        self.main_window.icons_dir = os.path.join(os.path.dirname(__file__), "..", "icons")
        init_project_manager_ui(self.main_window)
        self.main_window.project_path = os.path.join(os.path.dirname(__file__), "test_project")
        os.makedirs(self.main_window.project_path, exist_ok=True)
        with open(os.path.join(self.main_window.project_path, "test_file.txt"), "w") as f:
            f.write("Test file content")

    def tearDown(self):
        """
        Tear down test fixtures (if any).
        """
        self.main_window.close()

    def test_generate_llm_documentation_openai(self):
        """
        Test the generate_llm_documentation function with OpenAI.
        """
        self.main_window.openai_radio.setChecked(True)
        self.main_window.general_radio.setChecked(True)
        content = "def hello():\n    print('Hello, world!')"
        result = generate_llm_documentation(self.main_window, content)
        self.assertIsNotNone(result)
        self.assertIn("hello", result)

    def test_generate_llm_documentation_google(self):
        """
        Test the generate_llm_documentation function with Google.
        """
        self.main_window.google_radio.setChecked(True)
        self.main_window.general_radio.setChecked(True)
        content = "def hello():\n    print('Hello, world!')"
        result = generate_llm_documentation(self.main_window, content)
        self.assertIsNotNone(result)
        self.assertIn("hello", result)

    def test_call_openai_api(self):
        """
        Test the call_openai_api function.
        """
        content = "def hello():\n    print('Hello, world!')"
        result = call_openai_api(self.main_window, self.main_window.api_settings["openai"]["api_key"], "gpt-3.5-turbo", "You are a helpful assistant.", content, 0.7)
        self.assertIsNotNone(result)
        self.assertIn("hello", result)

    def test_call_google_api(self):
        """
        Test the call_google_api function.
        """
        content = "def hello():\n    print('Hello, world!')"
        result = call_google_api(self.main_window, self.main_window.api_settings["google"]["api_key"], "models/gemini-pro", "You are a helpful assistant.", content, 0.7)
        self.assertIsNotNone(result)
        self.assertIn("hello", result)

if __name__ == '__main__':
    unittest.main()
