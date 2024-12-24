==================================================
PROJECT GENERAL OVERVIEW:
==================================================

**Project Overview:**

This project is a GUI application built using PyQt5 for managing and documenting software projects. It allows users to select a project folder, choose between compressing the project into a documentation file (TXT or DOCX) or reconstructing a project from an existing documentation file. Additionally, it integrates with LLMs (OpenAI and Google) to generate documentation overviews. Users can configure API settings, select LLM models, and adjust parameters like temperature. The application also includes features for recursive selection of project files in a tree view, handling of different file formats, and logging of operations.

**Graphical Representation of Project Structure:**

```
+-----------------+     +-----------------+     +-----------------+
|    main.py    |---->|   gui_layout.py |---->|   settings.json   |
+-----------------+     +-----------------+     +-----------------+
      ^                                               |
      |                                               |
      +-----------------------------------------------+
      |                                               |
      |                                               V
      |                                   +-----------------+
      |                                   |   logs/         |
      |                                   |   dev_manager.log
      |                                   +-----------------+
      |                                               |
      |                                               V
      |                                   +-----------------+
      |                                   |  docx library   |
      |                                   +-----------------+
      |                                               |
      |                                               V
      |                                   +-----------------+
      |                                   |  openai library |
      |                                   +-----------------+
      |                                               |
      |                                               V
      |                                   +-----------------+
      |                                   | google.         |
      |                                   | generativeai   |
      |                                   | library         |
      |                                   +-----------------+
      |                                               |
      |                                               V
      V                                   +-----------------+
+-----------------+                        |   PyQt5 library |
|   __init__.py   |                        +-----------------+
+-----------------+

```

**Functions:**

*   **`gui_layout.py`**:
    *   `apply_stylesheet(widget)`: Applies a CSS stylesheet to a given PyQt5 widget for consistent styling.
    *   `init_api_settings_ui(dialog, settings)`: Initializes the UI for the API settings dialog, including layout and widgets for provider selection, API key, model selection, and temperature.
    *   `init_project_manager_ui(main_window)`: Sets up the main application window UI, including project and documentation selection, file format and action options, LLM options, and the process button.
*   **`main.py`**:
    *   `get_base_dir()`: Determines the base directory of the application, handling cases where it's run as a bundled executable or a script.
    *   `setup_logging()`: Sets up logging to a file and the console, creating a 'logs' directory if it doesn't exist.
    *   `load_api_settings()`: Loads API settings from `settings.json`, handling cases where the file is missing or contains invalid JSON.
    *   `APISettingsDialog.__init__(self, settings, parent=None)`: Initializes the API settings dialog.
    *   `APISettingsDialog.update_temperature_display(self, value)`: Updates the temperature display label in the API settings dialog.
    *   `APISettingsDialog.update_api_fields(self, provider_text)`: Updates API key and model fields based on the selected provider.
    *   `APISettingsDialog.load_settings_for_provider(self, provider)`: Loads settings for the specified provider.
    *   `APISettingsDialog.save_settings(self)`: Saves the API settings to `settings.json`.
    *   `APISettingsDialog.reset_settings(self)`: Resets API settings for the current provider.
    *   `ProjectManagerGUI.__init__(self)`: Initializes the main application window, loads settings, and sets up the UI.
    *   `ProjectManagerGUI.load_app_settings(self)`: Loads application settings from `settings.json` or sets default values.
    *   `ProjectManagerGUI._init_menu(self)`: Initializes the menu bar.
    *   `ProjectManagerGUI._init_buttons(self)`: Initializes buttons and sets their icons.
    *   `ProjectManagerGUI._init_connections(self)`: Connects signals and slots for UI elements.
    *   `ProjectManagerGUI.update_llm_options_state(self, state)`: Enables/disables LLM options based on checkbox state.
    *   `ProjectManagerGUI.show_app_settings_dialog(self)`: Displays the application settings dialog.
    *   `ProjectManagerGUI.set_button_icon(self, button, icon_name)`: Sets the icon for a button.
    *   `ProjectManagerGUI.set_menu_action_icon(self, action, icon_name)`: Sets the icon for a menu action.
    *   `ProjectManagerGUI.show_llm_info_dialog(self)`: Displays a dialog with information about LLMs.
    *   `ProjectManagerGUI.select_folder(self)`: Opens a dialog to select the project folder.
    *   `ProjectManagerGUI.select_all_in_folder(self, folder_index, select)`: Recursively selects/deselects items in the tree view.
    *   `ProjectManagerGUI.on_tree_selection_changed(self, selected, deselected)`: Handles tree view selection changes.
    *   `ProjectManagerGUI.closeEvent(self, event)`: Saves settings before closing the application.
    *   `ProjectManagerGUI.select_file(self)`: Opens a dialog to select the documentation file.
    *   `ProjectManagerGUI.reset_project_selection(self)`: Resets the project folder selection.
    *   `ProjectManagerGUI.reset_doc_selection(self)`: Resets the documentation file selection.
    *   `ProjectManagerGUI.update_action_state(self)`: Updates the state of action radio buttons based on file format selection.
    *   `ProjectManagerGUI._read_file_content(self, file_path)`: Reads file content with encoding detection.
    *   `ProjectManagerGUI.process_project(self)`: Main logic for processing the project (compression or reconstruction).
    *   `ProjectManagerGUI.get_project_content_for_llm(self, project_path)`: Extracts project content for LLM processing.
    *   `ProjectManagerGUI.generate_llm_documentation(self, project_text)`: Generates documentation using the selected LLM.
    *   `ProjectManagerGUI.call_openai_api(self, api_key, model, system_prompt, content, temperature)`: Calls the OpenAI API.
    *   `ProjectManagerGUI.call_google_api(self, api_key, model, system_prompt, content, temperature)`: Calls the Google Generative AI API.
    *   `ProjectManagerGUI.show_api_settings(self)`: Displays the API settings dialog.
    *   `ProjectManagerGUI.convert_project_to_text(self, project_path, llm_overview=None)`: Converts project files to a text documentation file.
    *   `ProjectManagerGUI.recreate_project_from_text(self, doc_file, project_name, save_location)`: Recreates a project from a text documentation file.
    *   `ProjectManagerGUI.create_project_documentation(self, project_path, llm_content=None)`: Creates project documentation in DOCX format.
    *   `ProjectManagerGUI.recreate_project_from_docx(self, doc_file, project_name, save_location)`: Recreates a project from a DOCX file.
    *   `ProjectManagerGUI.convert_docx_to_txt(self, docx_path)`: Converts a DOCX file to TXT.
    *   `run_tests()`: Runs unit tests.
    *   `TestProjectManager.setUp(self)`: Sets up test fixtures.
    *   `TestProjectManager.tearDown(self)`: Tears down test fixtures.
    *   `TestProjectManager.test_select_folder(self)`: Tests the `select_folder` method.

**Dependencies:**

*   **PyQt5:** `QtWidgets` (various widgets), `QtGui` (`QIcon`), `QtCore` (`Qt`, `QDir`, `QItemSelectionModel`)
*   **docx:** For creating and manipulating DOCX files.
*   **openai:** For interacting with the OpenAI API.
*   **google.generativeai:** For interacting with Google's Generative AI models.
*   **chardet:** For character encoding detection.
*   **unittest:** For unit testing.
*   **json:** For handling JSON files.
*   **logging:** For logging application events.
*   **os:** For interacting with the operating system.
*   **sys:** For system-specific parameters and functions.
*   **pathlib:** For object-oriented filesystem paths.
*   **datetime:** For working with dates and times.
*   **tempfile:** For generating temporary files and directories.
