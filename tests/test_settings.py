import unittest
import os
import json
from settings.settings_manager import load_api_settings, load_app_settings, save_settings
from PyQt5.QtWidgets import QMainWindow
from gui.layout import init_project_manager_ui

class TestSettings(unittest.TestCase):
    """
    Unit tests for the settings module.
    """

    def setUp(self):
        """
        Set up test fixtures (if any).
        """
        self.main_window = QMainWindow()
        self.main_window.icons_dir = os.path.join(os.path.dirname(__file__), "..", "icons")
        init_project_manager_ui(self.main_window)
        self.test_dir = os.path.join(os.path.dirname(__file__), "test_settings")
        self.settings_file = os.path.join(self.test_dir, "settings.json")
        os.makedirs(self.test_dir, exist_ok=True)
        self.main_window.base_dir = self.test_dir

    def tearDown(self):
        """
        Tear down test fixtures (if any).
        """
        if os.path.exists(self.settings_file):
            os.remove(self.settings_file)
        os.rmdir(self.test_dir)
        self.main_window.close()

    def test_load_api_settings(self):
        """
        Test the load_api_settings function.
        """
        # Create a dummy settings file
        test_settings = {
            "openai": {
                "api_key": "test_key",
                "model": "gpt-3.5-turbo",
                "temperature": 0.7
            },
            "recent_paths": {
                "project": "/path/to/project",
                "doc": "/path/to/doc"
            }
        }
        with open(self.settings_file, "w") as f:
            json.dump(test_settings, f)

        # Load the settings
        settings = load_api_settings(self.test_dir)

        # Check if the settings were loaded correctly
        self.assertEqual(settings["openai"]["api_key"], "test_key")
        self.assertEqual(settings["openai"]["model"], "gpt-3.5-turbo")
        self.assertEqual(settings["openai"]["temperature"], 0.7)
        self.assertEqual(settings["recent_paths"]["project"], "/path/to/project")
        self.assertEqual(settings["recent_paths"]["doc"], "/path/to/doc")

    def test_load_app_settings(self):
        """
        Test the load_app_settings function.
        """
        # Create a dummy settings file
        test_settings = {
            "output_format": "docx",
            "llm_temperature": 0.5,
            "recursive_selection": False
        }
        with open(self.settings_file, "w") as f:
            json.dump(test_settings, f)

        # Load the settings
        settings = load_app_settings(self.test_dir)

        # Check if the settings were loaded correctly
        self.assertEqual(settings["output_format"], "docx")
        self.assertEqual(settings["llm_temperature"], 0.5)
        self.assertFalse(settings["recursive_selection"])

    def test_save_settings(self):
        """
        Test the save_settings function.
        """
        # Set some test settings
        self.main_window.recent_project_path = "/path/to/project"
        self.main_window.recent_doc_path = "/path/to/doc"
        self.main_window.api_settings = {
            "openai": {
                "api_key": "test_key",
                "model": "gpt-3.5-turbo",
                "temperature": 0.7
            },
            "recent_paths": {
                "project": "/path/to/project",
                "doc": "/path/to/doc"
            }
        }

        # Save the settings
        save_settings(self.main_window)

        # Check if the settings file was created
        self.assertTrue(os.path.exists(self.settings_file))

        # Check if the settings were saved correctly
        with open(self.settings_file, "r") as f:
            saved_settings = json.load(f)

        self.assertEqual(saved_settings["openai"]["api_key"], "test_key")
        self.assertEqual(saved_settings["openai"]["model"], "gpt-3.5-turbo")
        self.assertEqual(saved_settings["openai"]["temperature"], 0.7)
        self.assertEqual(saved_settings["recent_paths"]["project"], "/path/to/project")
        self.assertEqual(saved_settings["recent_paths"]["doc"], "/path/to/doc")

if __name__ == '__main__':
    unittest.main()
