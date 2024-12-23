# -Python_Project_Compress-Summarize v. 0.9

==================================================
PROJECT GENERAL OVERVIEW:

This project is a Python-based GUI application named "Project Manager," designed to facilitate the documentation and reconstruction of software projects. It allows users to select a project folder, generate documentation (in either TXT or DOCX format), and optionally use Large Language Models (LLMs) from OpenAI or Google to assist in generating project overviews. The application also supports reconstructing a project from a text-based documentation file.

==================================================
Graphical Representation of Project Structure
==================================================

```
+-------------------------------------+
| project_manager_gui_v1(gemini 2.0  |
| flash thinking)_v3.py              |
+-------------------------------------+
        |
        |    +-----------------+
        |--->| gui_layout.py   |
        |    +-----------------+
        |           ^
        |           |
        |           |
        | +--------------------+
        | | PyQt5 library     |
        | +--------------------+
        |
        | +-----------------+
        | | settings.json   |
        | +-----------------+
        |
        |
        |    +------------------+
        |--->|  openai library  |
        |    +------------------+
        |
        |    +---------------------------+
        |--->|  google.generativeai library  |
        |    +---------------------------+
        |
        V
+-------------------------------------+
| User Interface (PyQt5 Application)  |
+-------------------------------------+
```
==================================================
Explanation of the Diagram:
==================================================
*   `project_manager_gui_v1(gemini 2.0 flash thinking)_v3.py`: This is the main script containing the core logic of the application.
*   `gui_layout.py`: This module contains the code for setting up the GUI layout, including applying stylesheets and initializing UI components.
*   `settings.json`: This file stores API settings (API keys, models, temperature) for different LLM providers.
*   `openai Library`: The external library used for interacting with OpenAI's API.
*   `google.generativeai Library`: The external library used for interacting with Google's Gemini API.
*   `PyQt5 Library`: The external library used for creating the GUI.

==================================================
Functions
==================================================

Here's a breakdown of the key functions within the project:

*   **`gui_layout.py`**
    *   `apply_stylesheet(widget)`: Applies a predefined stylesheet to the provided Qt widget.
    *   `init_api_settings_ui(dialog, settings)`: Initializes the UI for the API settings dialog.
    *   `init_project_manager_ui(main_window)`: Initializes the UI of the main project manager window.
*   **`project_manager_gui_v1(gemini 2.0 flash thinking)_v3.py`**
    *   `setup_logging()`: Sets up logging for the application, including file and console output.
    *   `load_api_settings()`: Loads API settings from the `settings.json` file.
    *   `APISettingsDialog.__init__(self, settings)`: Initializes the API settings dialog, allowing the user to configure API keys, models and temperature.
    *   `APISettingsDialog.update_temperature_display(self, value)`: Updates the display label for the temperature slider.
    *   `APISettingsDialog.update_api_fields(self, provider_text)`: Updates the API key label and model combo box when a provider is selected.
    *   `APISettingsDialog.load_settings_for_provider(self, provider)`: Loads settings for specific providers.
    *   `APISettingsDialog.save_settings(self)`: Saves the API settings to `settings.json`.
    *   `APISettingsDialog.reset_settings(self)`: Resets the API settings for the current provider.
        *  `AppSettingsDialog.__init__(self, settings)`: Initializes the application settings dialog, allowing the user to configure output format, temperature and tree view selection.
        *   `AppSettingsDialog.update_temperature_display(self, value)`: Updates the display label for the temperature slider.
        *   `AppSettingsDialog.save_settings(self)`: Saves the application settings to `settings.json`.
    *   `ProjectManagerGUI.__init__(self)`: Initializes the main application window, sets up the UI, loads settings, and connects signals to slots.
    *   `ProjectManagerGUI.show_llm_info_dialog(self)`: Displays a dialog with detailed information about LLMs.
    *   `ProjectManagerGUI.select_folder(self)`: Opens a dialog to select the project folder.
    *   `ProjectManagerGUI.select_file(self)`: Opens a dialog to select a documentation file.
    *   `ProjectManagerGUI.reset_project_selection(self)`: Resets the selected project folder.
    *   `ProjectManagerGUI.reset_doc_selection(self)`: Resets the selected documentation file.
    *   `ProjectManagerGUI.update_action_state(self)`: Updates UI elements based on the selected file format.
    *   `ProjectManagerGUI.process_project(self)`: Orchestrates the main processing logic for project documentation or reconstruction.
    *   `ProjectManagerGUI.get_project_content_for_llm(self, project_path)`: Extracts the content of project files for LLM processing.
    *   `ProjectManagerGUI.generate_llm_documentation(self, project_text)`: Generates documentation using the selected LLM provider.
    *   `ProjectManagerGUI.call_openai_api(self, api_key, model, system_prompt, content, temperature)`: Makes a request to the OpenAI API.
    *   `ProjectManagerGUI.call_google_api(self, api_key, model, system_prompt, content, temperature)`: Makes a request to the Google API.
    *   `ProjectManagerGUI.show_api_settings(self)`: Displays the API settings dialog.
    *   `ProjectManagerGUI.convert_project_to_text(self, project_path, output_file, llm_overview=None)`: Converts the project to a text-based documentation.
    *   `ProjectManagerGUI.recreate_project_from_text(self, doc_file, project_name, save_location)`: Reconstructs a project structure from a text documentation file.
    *   `ProjectManagerGUI.create_project_documentation(self, project_path, output_file, llm_content=None)`: Generates project documentation in DOCX format.
    *   `ProjectManagerGUI.recreate_project_from_docx(self, doc_file, project_name, save_location)`: Recreates a project from a DOCX file.
    *   `ProjectManagerGUI.convert_docx_to_txt(self, docx_path)`: Converts a DOCX file to a TXT file.
    *   `ProjectManagerGUI.closeEvent(self, event)`: Saves settings before closing the application.
    *   `ProjectManagerGUI.show_app_settings_dialog(self)`: Displays the application settings dialog.
    *   `ProjectManagerGUI.set_button_icon(self, button, icon_name)`: Sets an icon for a button.
    *   `ProjectManagerGUI.set_menu_action_icon(self, action, icon_name)`: Sets an icon for a menu action.
    *   `ProjectManagerGUI.on_tree_selection_changed(self, selected, deselected)`: Handles changes in tree view selection.
     *   `ProjectManagerGUI.select_all_in_folder(self, folder_index, select)`: Recursively select or deselect all items within a folder in the tree view.
     *   
==================================================
**Dependencies:**
==================================================
*   **Python Standard Library:** `sys`, `os`, `pathlib`, `datetime`, `json`, `logging`, `unittest`.
*   **PyQt5:** For creating the GUI (`QtWidgets`, `QtGui`, `QtCore`).
*   **python-docx:** For creating and manipulating DOCX files (`docx`, `docx.shared`, `docx.enum.text`, `docx.enum.style`).
*   **openai:** For interacting with the OpenAI API.
*   **google-generativeai:** For interacting with the Google Gemini API.
*   **chardet**: For detecting file encodings.

==================================================
Detailed Explanation:
==================================================

*   **`gui_layout.py`**: This file is responsible for the visual presentation of the application. It contains functions to apply a consistent stylesheet across the application's widgets and to initialize the layouts of both the main window and the API settings dialog. It uses `PyQt5` for the GUI elements.
*   **`project_manager_gui_v1(gemini 2.0 flash thinking)_v3.py`**: This is the core file where the main logic resides. It includes setting up logging, loading API settings from `settings.json`, defining the GUI application window (`ProjectManagerGUI`), handling user interactions, and implementing the project documentation and reconstruction functionality.
    *   The `ProjectManagerGUI` class is the main window of the application. It initializes the UI, including buttons, radio buttons, a file tree view, and connections to the corresponding functions.
    *   The application uses the `QFileSystemModel` to display the project directory structure in a tree view. The `QTreeView` allows the user to select files and folders.
    *   The app supports using LLMs for documentation. The user can select between OpenAI and Google's Gemini models and provide API keys. The `openai` and `google.generativeai` libraries are used for interacting with the respective APIs.
    *   The application provides the functionality to generate documentation in both TXT and DOCX formats. The `docx` library is used to create DOCX files.
    *   The application also provides the functionality to reconstruct a project from a documentation file. It parses the file, recreates the directory structure, and writes file content.
    *   The `settings.json` file stores the API keys and other settings.
    *   The logging module is used for logging all actions, errors, and warnings.
    *   The application also includes a basic application settings dialog for output format, temperature and tree view selection mode.
*   **`settings.json`**: This file contains a JSON object with API keys for OpenAI and Google, along with other settings (temperature, model).
*   **`logs\dev_manager.log`**: Contains logs from the application.
