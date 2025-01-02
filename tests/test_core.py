import unittest
import os
import shutil
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QDir, Qt
from core.project import select_folder, select_all_in_folder, on_tree_selection_changed, reset_project_selection, get_project_structure
from core.document import select_file, reset_doc_selection, convert_project_to_text, create_project_documentation, convert_docx_to_txt
from core.reconstructor import recreate_project_from_text, recreate_project_from_docx
from core.processor import process_project, update_action_state, _process_single_file, get_project_content_for_llm
from core.utils import _read_file_content, has_extension, has_any_extension
from gui.layout import init_project_manager_ui

class TestCore(unittest.TestCase):
    """
    Unit tests for the core module.
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
        self.main_window.project_path = os.path.join(os.path.dirname(__file__), "test_project")
        self.main_window.doc_file_path = os.path.join(os.path.dirname(__file__), "test_doc.txt")
        self.main_window.recent_project_path = ""
        self.main_window.recent_doc_path = ""
        self.main_window.selected_files_for_compression = []
        self.main_window.api_settings = {}
        self.main_window.llm_type_group = None
        self.main_window.overview_type_group = None
        self.main_window.use_llm_check = None
        self.main_window.txt_radio = None
        self.main_window.docx_radio = None
        self.main_window.compress_radio = None
        self.main_window.reconstruct_radio = None
        self.main_window.project_tree_view = None
        self.main_window.file_system_model = None
        self.main_window.icons_dir = os.path.join(os.path.dirname(__file__), "..", "icons")
        init_project_manager_ui(self.main_window)
        os.makedirs(self.main_window.project_path, exist_ok=True)
        with open(os.path.join(self.main_window.project_path, "test_file.txt"), "w") as f:
            f.write("Test file content")

    def tearDown(self):
        """
        Tear down test fixtures (if any).
        """
        shutil.rmtree(self.main_window.project_path)
        self.main_window.close()

    def test_select_folder(self):
        """
        Test the select_folder function.
        """
        # Simulate selecting a folder
        select_folder(self.main_window)
        self.assertEqual(self.main_window.project_path, os.path.join(os.path.dirname(__file__), "test_project"))

    def test_select_all_in_folder(self):
        """
        Test the select_all_in_folder function.
        """
        # Create a test directory structure
        os.makedirs(os.path.join(self.main_window.project_path, "subdir"), exist_ok=True)
        with open(os.path.join(self.main_window.project_path, "subdir", "test_file2.txt"), "w") as f:
            f.write("Test file 2 content")

        # Select all in the test project folder
        root_index = self.main_window.file_system_model.index(self.main_window.project_path)
        select_all_in_folder(self.main_window, root_index, True)

        # Check if all items are selected
        selected_indexes = self.main_window.project_tree_view.selectionModel().selectedIndexes()
        selected_files = [self.main_window.file_system_model.filePath(index) for index in selected_indexes]
        self.assertIn(os.path.join(self.main_window.project_path, "test_file.txt"), selected_files)
        self.assertIn(os.path.join(self.main_window.project_path, "subdir", "test_file2.txt"), selected_files)

    def test_on_tree_selection_changed(self):
        """
        Test the on_tree_selection_changed function.
        """
        # Create a test directory structure
        os.makedirs(os.path.join(self.main_window.project_path, "subdir"), exist_ok=True)
        with open(os.path.join(self.main_window.project_path, "subdir", "test_file2.txt"), "w") as f:
            f.write("Test file 2 content")

        # Simulate selecting the test project folder
        root_index = self.main_window.file_system_model.index(self.main_window.project_path)
        self.main_window.project_tree_view.selectionModel().select(root_index, QItemSelectionModel.Select)
        on_tree_selection_changed(self.main_window, self.main_window.project_tree_view.selectionModel().selection(), QItemSelectionModel.NoUpdate)

        # Check if all items are selected
        selected_indexes = self.main_window.project_tree_view.selectionModel().selectedIndexes()
        selected_files = [self.main_window.file_system_model.filePath(index) for index in selected_indexes]
        self.assertIn(os.path.join(self.main_window.project_path, "test_file.txt"), selected_files)
        self.assertIn(os.path.join(self.main_window.project_path, "subdir", "test_file2.txt"), selected_files)

    def test_reset_project_selection(self):
        """
        Test the reset_project_selection function.
        """
        # Select a project folder
        select_folder(self.main_window)

        # Reset the project selection
        reset_project_selection(self.main_window)

        # Check if the project path is reset
        self.assertIsNone(self.main_window.project_path)
        self.assertEqual(self.main_window.recent_project_path, "")

    def test_get_project_structure(self):
        """
        Test the get_project_structure function.
        """
        # Create a test directory structure
        os.makedirs(os.path.join(self.main_window.project_path, "subdir"), exist_ok=True)
        with open(os.path.join(self.main_window.project_path, "subdir", "test_file2.txt"), "w") as f:
            f.write("Test file 2 content")

        # Get the project structure
        structure = get_project_structure(self.main_window.project_path)

        # Check if the structure is correct
        expected_structure = f"test_project/\n  +-- subdir/\n    +-- test_file2.txt\n  +-- test_file.txt"
        self.assertEqual(structure, expected_structure)

    def test_select_file(self):
        """
        Test the select_file function.
        """
        # Simulate selecting a file
        select_file(self.main_window)
        self.assertEqual(self.main_window.doc_file_path, os.path.join(os.path.dirname(__file__), "test_doc.txt"))

    def test_reset_doc_selection(self):
        """
        Test the reset_doc_selection function.
        """
        # Select a documentation file
        select_file(self.main_window)

        # Reset the documentation file selection
        reset_doc_selection(self.main_window)

        # Check if the documentation file path is reset
        self.assertIsNone(self.main_window.doc_file_path)
        self.assertEqual(self.main_window.recent_doc_path, "")

    def test_convert_project_to_text(self):
        """
        Test the convert_project_to_text function.
        """
        # Create a test directory structure
        os.makedirs(os.path.join(self.main_window.project_path, "subdir"), exist_ok=True)
        with open(os.path.join(self.main_window.project_path, "subdir", "test_file2.txt"), "w") as f:
            f.write("Test file 2 content")

        # Convert the project to text
        result = convert_project_to_text(self.main_window, self.main_window.project_path)

        # Check if the conversion was successful
        self.assertTrue(result)

        # Check if the output file exists
        output_file = os.path.join(self.main_window.project_path, "project_documentation", "project_documentation.txt")
        self.assertTrue(os.path.exists(output_file))

    def test_create_project_documentation(self):
        """
        Test the create_project_documentation function.
        """
        # Create a test directory structure
        os.makedirs(os.path.join(self.main_window.project_path, "subdir"), exist_ok=True)
        with open(os.path.join(self.main_window.project_path, "subdir", "test_file2.txt"), "w") as f:
            f.write("Test file 2 content")

        # Create project documentation
        create_project_documentation(self.main_window, self.main_window.project_path)

        # Check if the documentation file exists
        output_file = os.path.join(self.main_window.project_path, "project_documentation", "project_documentation.docx")
        self.assertTrue(os.path.exists(output_file))

    def test_convert_docx_to_txt(self):
        """
        Test the convert_docx_to_txt function.
        """
        # Create a dummy .docx file for testing
        docx_file = os.path.join(self.main_window.project_path, "test.docx")
        doc = Document()
        doc.add_paragraph("Test content")
        doc.save(docx_file)

        # Convert the .docx file to .txt
        txt_file = convert_docx_to_txt(docx_file)

        # Check if the .txt file was created
        self.assertTrue(os.path.exists(txt_file))

        # Check if the content is correct
        with open(txt_file, "r") as f:
            content = f.read()
        self.assertEqual(content.strip(), "Test content")

    def test_recreate_project_from_text(self):
        """
        Test the recreate_project_from_text function.
        """
        # Create a dummy .txt file for testing
        txt_file = os.path.join(self.main_window.project_path, "test_doc.txt")
        with open(txt_file, "w") as f:
            f.write("## Project Structure\n```\ntest_project/\n  +-- subdir/\n    +-- test_file2.txt\n  +-- test_file.txt\n```\n")
            f.write("## Files Content\n### File: test_file.txt\n```text\nTest file content\n```\n")
            f.write("### File: subdir/test_file2.txt\n```text\nTest file 2 content\n```\n")

        # Recreate the project from the .txt file
        recreate_project_from_text(self.main_window, txt_file, "recreated_project", self.main_window.project_path)

        # Check if the project was recreated correctly
        self.assertTrue(os.path.exists(os.path.join(self.main_window.project_path, "recreated_project")))
        self.assertTrue(os.path.exists(os.path.join(self.main_window.project_path, "recreated_project", "test_file.txt")))
        self.assertTrue(os.path.exists(os.path.join(self.main_window.project_path, "recreated_project", "subdir", "test_file2.txt")))

        # Check if the file contents are correct
        with open(os.path.join(self.main_window.project_path, "recreated_project", "test_file.txt"), "r") as f:
            content = f.read()
        self.assertEqual(content.strip(), "Test file content")

        with open(os.path.join(self.main_window.project_path, "recreated_project", "subdir", "test_file2.txt"), "r") as f:
            content = f.read()
        self.assertEqual(content.strip(), "Test file 2 content")

    def test_recreate_project_from_docx(self):
        """
        Test the recreate_project_from_docx function.
        """
        # Create a dummy .docx file for testing
        docx_file = os.path.join(self.main_window.project_path, "test.docx")
        doc = Document()
        doc.add_paragraph("## Project Structure")
        doc.add_paragraph("```")
        doc.add_paragraph("test_project/")
        doc.add_paragraph("  +-- subdir/")
        doc.add_paragraph("    +-- test_file2.txt")
        doc.add_paragraph("  +-- test_file.txt")
        doc.add_paragraph("```")
        doc.add_paragraph("## Files Content")
        doc.add_paragraph("### File: test_file.txt")
        doc.add_paragraph("```text")
        doc.add_paragraph("Test file content")
        doc.add_paragraph("```")
        doc.add_paragraph("### File: subdir/test_file2.txt")
        doc.add_paragraph("```text")
        doc.add_paragraph("Test file 2 content")
        doc.add_paragraph("```")
        doc.save(docx_file)

        # Recreate the project from the .docx file
        recreate_project_from_docx(self.main_window, docx_file, "recreated_project", self.main_window.project_path)

        # Check if the project was recreated correctly
        self.assertTrue(os.path.exists(os.path.join(self.main_window.project_path, "recreated_project")))
        self.assertTrue(os.path.exists(os.path.join(self.main_window.project_path, "recreated_project", "test_file.txt")))
        self.assertTrue(os.path.exists(os.path.join(self.main_window.project_path, "recreated_project", "subdir", "test_file2.txt")))

        # Check if the file contents are correct
        with open(os.path.join(self.main_window.project_path, "recreated_project", "test_file.txt"), "r") as f:
            content = f.read()
        self.assertEqual(content.strip(), "Test file content")

        with open(os.path.join(self.main_window.project_path, "recreated_project", "subdir", "test_file2.txt"), "r") as f:
            content = f.read()
        self.assertEqual(content.strip(), "Test file 2 content")

    def test_process_project(self):
        """
        Test process project
        """
        self.main_window.process_project()
        self.main_window.compress_radio.setChecked(True)
        self.main_window.txt_radio.setChecked(True)
        self.main_window.docx_radio.setChecked(False)
        self.main_window.reconstruct_radio.setChecked(False)
        self.main_window.use_llm_check.setChecked(False)
        self.main_window.none_radio.setChecked(True)
        self.main_window.openai_radio.setChecked(False)
        self.main_window.google_radio.setChecked(False)
        self.main_window.general_radio.setChecked(True)
        self.main_window.detailed_radio.setChecked(False)
        self.main_window.project_tree_view.selectionModel().select(self.main_window.file_system_model.index(self.main_window.project_path), QItemSelectionModel.Select)
        self.main_window.project_tree_view.selectionModel().selectionChanged.connect(
            lambda: on_tree_selection_changed(self.main_window, self.main_window.project_tree_view.selectionModel().selection(), QItemSelectionModel.NoUpdate)
        )
        self.main_window.process_project()

    def test_update_action_state(self):
        """
        Test update action state
        """
        self.main_window.docx_radio.setChecked(True)
        update_action_state(self.main_window)
        self.assertTrue(self.main_window.compress_radio.isChecked())
        self.assertFalse(self.main_window.compress_radio.isEnabled())
        self.assertTrue(self.main_window.reconstruct_radio.isEnabled())

        self.main_window.txt_radio.setChecked(True)
        update_action_state(self.main_window)
        self.assertTrue(self.main_window.compress_radio.isEnabled())
        self.assertTrue(self.main_window.reconstruct_radio.isEnabled())

    def test_process_single_file(self):
        """
        Test process single file
        """
        result = _process_single_file(self.main_window, self.main_window.project_path, "test_file.txt", self.main_window.project_path)
        self.assertEqual(result, ["### File: test_file.txt\n\n", "```text\n", "Test file content", "\n```\n\n"])

    def test_get_project_content_for_llm(self):
        """
        Test get project content for llm
        """
        result = get_project_content_for_llm(self.main_window, self.main_window.project_path)
        self.assertEqual(result, "File: test_file.txt\nTest file content\n\n")

    def test_read_file_content(self):
        """
        Test read file content
        """
        result = _read_file_content(os.path.join(self.main_window.project_path, "test_file.txt"))
        self.assertEqual(result, "Test file content")

    def test_has_extension(self):
        """
        Test has extension
        """
        self.assertTrue(has_extension("test_file.txt", ".txt"))
        self.assertFalse(has_extension("test_file.txt", ".docx"))

    def test_has_any_extension(self):
        """
        Test has any extension
        """
        self.assertTrue(has_any_extension("test_file.txt", [".txt", ".docx"]))
        self.assertFalse(has_any_extension("test_file.txt", [".py", ".js"]))

if __name__ == '__main__':
    unittest.main()
