import sys
import os
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileSystemModel
)
from PyQt5.QtGui import QIcon  # Import QIcon
from PyQt5.QtCore import QDir
from gui.layout import (
    init_project_manager_ui,
    _init_menu,
    _init_buttons,
    _init_connections,
    update_llm_options_state
)
from gui.dialogs import (
    show_llm_info_dialog,
    show_api_settings,
)
from core.project import (
    select_folder,
    select_all_in_folder,
    on_tree_selection_changed,
    reset_project_selection,
    get_project_structure
)
from core.document import (
    select_file,
    reset_doc_selection,
    convert_project_to_text,
    create_project_documentation,
    convert_docx_to_txt
)
from core.reconstructor import (
    recreate_project_from_text,
    recreate_project_from_docx
)
from core.processor import (
    process_project,
    update_action_state,
    _process_single_file,
    get_project_content_for_llm
)
from core.utils import (
    _read_file_content,
    has_extension,
    has_any_extension
)
from llm.llm_manager import (
    generate_llm_documentation,
    call_openai_api,
    call_google_api
)
from settings.settings_manager import (
    load_api_settings,
    load_app_settings,
    save_settings
)
from utils.file_utils import get_base_dir
from utils.log_utils import setup_logging
from gui.utils import set_menu_action_icon, set_button_icon  # Import the missing functions

class ProjectManagerGUI(QMainWindow):
    """Main application window for the Project Manager."""

    def __init__(self):
        """Initialize the main application window and load API settings."""
        super().__init__()

        self.base_dir = get_base_dir()
        self.icons_dir = os.path.join(self.base_dir, "icons")
        self.api_settings = load_api_settings(self.base_dir)
        self.app_settings = load_app_settings(self.base_dir)
        self.recent_project_path = self.api_settings.get("recent_paths", {}).get("project", "")
        self.recent_doc_path = self.api_settings.get("recent_paths", {}).get("doc", "")
        self.project_path = None
        self.doc_file_path = None
        self.google_model = None

        self.file_system_model = QFileSystemModel()
        self.file_system_model.setRootPath(QDir.homePath())
        self.file_system_model.setFilter(QDir.AllEntries | QDir.NoDotAndDotDot)

        init_project_manager_ui(self)

        self.project_tree_view.setModel(self.file_system_model)
        self.project_tree_view.setRootIndex(self.file_system_model.index(QDir.homePath()))
        self.project_tree_view.setColumnHidden(1, True)
        self.project_tree_view.setColumnHidden(2, True)
        self.project_tree_view.setColumnHidden(3, True)

        self.selected_files_for_compression = []

        _init_menu(self)
        _init_buttons(self)
        _init_connections(self)

        # Ensure the icons directory exists
        if not os.path.exists(self.icons_dir):
            os.makedirs(self.icons_dir)
            print(f"Created icons directory at: {self.icons_dir}")

        self.setWindowIcon(QIcon(os.path.join(self.icons_dir, "app_icon.png")))

        self.showMaximized()

    # Add the missing methods
    def set_menu_action_icon(self, action, icon_name):
        """Helper function to set icon for a menu action."""
        set_menu_action_icon(action, icon_name, self.base_dir)

    def set_button_icon(self, button, icon_name):
        """Helper function to set icon for a button."""
        set_button_icon(button, icon_name, self.base_dir)

    def closeEvent(self, event):
        """Save settings before closing the application."""
        save_settings(self)
        event.accept()

    # Expose core functionality methods to the GUI
    select_folder = select_folder
    select_all_in_folder = select_all_in_folder
    on_tree_selection_changed = on_tree_selection_changed
    reset_project_selection = reset_project_selection
    get_project_structure = get_project_structure
    select_file = select_file
    reset_doc_selection = reset_doc_selection
    convert_project_to_text = convert_project_to_text
    create_project_documentation = create_project_documentation
    convert_docx_to_txt = convert_docx_to_txt
    recreate_project_from_text = recreate_project_from_text
    recreate_project_from_docx = recreate_project_from_docx
    process_project = process_project
    update_action_state = update_action_state
    _process_single_file = _process_single_file
    get_project_content_for_llm = get_project_content_for_llm
    generate_llm_documentation = generate_llm_documentation
    call_openai_api = call_openai_api
    call_google_api = call_google_api
    show_llm_info_dialog = show_llm_info_dialog
    show_api_settings = show_api_settings
    update_llm_options_state = update_llm_options_state
    _read_file_content = _read_file_content

if __name__ == "__main__":
    setup_logging()
    app = QApplication(sys.argv)
    ex = ProjectManagerGUI()
    sys.exit(app.exec_())
