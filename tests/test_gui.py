import unittest
from PyQt5.QtWidgets import QApplication, QMainWindow
from gui.layout import init_project_manager_ui, _init_menu, _init_buttons, _init_connections, update_llm_options_state
from gui.dialogs import APISettingsDialog, show_llm_info_dialog
from gui.utils import apply_stylesheet, set_button_icon, set_menu_action_icon
from PyQt5.QtCore import Qt
import sys
import os

class TestGui(unittest.TestCase):
    """
    Unit tests for the GUI module.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up test fixtures (if any).
        """
        cls.app = QApplication(sys.argv)

    @classmethod
    def tearDownClass(cls):
        """
        Tear down test fixtures (if any).
        """
        cls.app.quit()

    def setUp(self):
        """
        Set up a main window for testing.
        """
        self.main_window = QMainWindow()
        self.main_window.api_settings = {}  # Initialize api_settings
        self.main_window.icons_dir = os.path.join(os.path.dirname(__file__), "..", "icons")
        self.main_window.base_dir = os.path.dirname(__file__)
        init_project_manager_ui(self.main_window)
        _init_menu(self.main_window)
        _init_buttons(self.main_window)
        _init_connections(self.main_window)

    def tearDown(self):
        """
        Close the main window after each test.
        """
        self.main_window.close()

    def test_init_project_manager_ui(self):
        """
        Test the initialization of the main window UI.
        """
        self.assertIsNotNone(self.main_window.centralWidget())

    def test_init_menu(self):
        """
        Test the initialization of the menu bar.
        """
        self.assertIsNotNone(self.main_window.menuBar())
        self.assertEqual(self.main_window.menuBar().actions()[0].text(), "&File")
        self.assertEqual(self.main_window.menuBar().actions()[1].text(), "&Settings")

    def test_init_buttons(self):
        """
        Test the initialization of the buttons.
        """
        self.assertIsNotNone(self.main_window.select_project_button)
        self.assertIsNotNone(self.main_window.reset_project_button)
        self.assertIsNotNone(self.main_window.select_doc_button)
        self.assertIsNotNone(self.main_window.reset_doc_button)
        self.assertIsNotNone(self.main_window.llm_info_button)
        self.assertIsNotNone(self.main_window.process_button)

    def test_update_llm_options_state(self):
        """
        Test the enabling/disabling of LLM options.
        """
        update_llm_options_state(self.main_window, Qt.Checked)
        self.assertTrue(self.main_window.none_radio.isEnabled())
        self.assertTrue(self.main_window.openai_radio.isEnabled())
        self.assertTrue(self.main_window.google_radio.isEnabled())
        self.assertTrue(self.main_window.general_radio.isEnabled())
        self.assertTrue(self.main_window.detailed_radio.isEnabled())
        self.assertTrue(self.main_window.llm_info_button.isEnabled())

        update_llm_options_state(self.main_window, Qt.Unchecked)
        self.assertFalse(self.main_window.none_radio.isEnabled())
        self.assertFalse(self.main_window.openai_radio.isEnabled())
        self.assertFalse(self.main_window.google_radio.isEnabled())
        self.assertFalse(self.main_window.general_radio.isEnabled())
        self.assertFalse(self.main_window.detailed_radio.isEnabled())
        self.assertFalse(self.main_window.llm_info_button.isEnabled())

    def test_api_settings_dialog(self):
        """
        Test the API settings dialog.
        """
        settings = {}
        dialog = APISettingsDialog(settings)
        self.assertIsNotNone(dialog)

    def test_show_llm_info_dialog(self):
        """
        Test the LLM info dialog.
        """
        # Just check if it can be shown without errors
        try:
            show_llm_info_dialog(self.main_window)
        except Exception as e:
            self.fail(f"show_llm_info_dialog raised an exception: {e}")

    def test_apply_stylesheet(self):
        """
        Test the apply_stylesheet function.
        """
        # Just check if it can be applied without errors
        try:
            apply_stylesheet(self.main_window)
        except Exception as e:
            self.fail(f"apply_stylesheet raised an exception: {e}")

    def test_set_button_icon(self):
        """
        Test the set_button_icon function.
        """
        # Create a dummy button for testing
        button = self.main_window.select_project_button
        # Just check if it can be applied without errors
        try:
            set_button_icon(button, "folder.png", self.main_window.base_dir)
        except Exception as e:
            self.fail(f"set_button_icon raised an exception: {e}")

    def test_set_menu_action_icon(self):
        """
        Test the set_menu_action_icon function.
        """
        # Create a dummy action for testing
        action = self.main_window.api_settings_action
        # Just check if it can be applied without errors
        try:
            set_menu_action_icon(action, "settings.png", self.main_window.base_dir)
        except Exception as e:
            self.fail(f"set_menu_action_icon raised an exception: {e}")

if __name__ == '__main__':
    unittest.main()
