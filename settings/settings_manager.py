import json
import os
from PyQt5.QtWidgets import QMessageBox

def load_api_settings(base_dir):
    """Load API settings and other persistent data from settings.json."""
    settings_path = os.path.join(base_dir, "settings.json")
    default_settings = {"recent_paths": {"project": "", "doc": ""}}

    try:
        if not os.path.exists(settings_path):
            print("settings.json not found. Starting with default settings.")
            return default_settings

        with open(settings_path, "r") as f:
            settings = json.load(f)
            # Ensure default structure for recent paths
            if "recent_paths" not in settings:
                settings["recent_paths"] = default_settings["recent_paths"]
            return settings
    except json.JSONDecodeError:
        print("Error decoding settings.json. Please check the file format.")
        QMessageBox.warning(None, "Settings Error", "Error reading settings file. Starting with default settings.")
        return default_settings
    except Exception as e:
        print(f"Unexpected error loading settings: {e}")
        QMessageBox.critical(None, "Settings Error", f"Failed to load settings: {e}")
        return default_settings

def load_app_settings(base_dir):
    """Loads application settings from settings.json, or sets default values."""
    default_settings = {
        "output_format": "txt",
        "llm_temperature": 0.7,
        "recursive_selection": True
    }

    try:
        settings_path = os.path.join(base_dir, "settings.json")
        if not os.path.exists(settings_path):
            # Create a new settings.json file if it doesn't exist
            with open(settings_path, "w") as f:
                json.dump(default_settings, f, indent=4)
            print("New settings.json file created.")

        with open(settings_path, "r") as f:
            app_settings = json.load(f)

        # Ensure default values are present
        for key, value in default_settings.items():
            if key not in app_settings:
                app_settings[key] = value

    except (FileNotFoundError, PermissionError) as e:
        print(f"Error accessing settings.json: {e}")
        QMessageBox.critical(None, "Error", f"Could not access settings file: {e}")
        app_settings = default_settings
    except json.JSONDecodeError:
        print("Error decoding settings.json. Using default settings.")
        app_settings = default_settings
    except Exception as e:
        print(f"Unexpected error loading settings: {e}")
        app_settings = default_settings
    
    print(f"Application settings loaded: {app_settings}")
    return app_settings

def save_settings(main_window):
    """Save settings before closing the application."""
    try:
        # Save recent paths
        main_window.api_settings["recent_paths"] = {
            "project": main_window.recent_project_path,
            "doc": main_window.recent_doc_path
        }

        settings_path = os.path.join(main_window.base_dir, "settings.json")
        with open(settings_path, "w") as f:
            json.dump(main_window.api_settings, f, indent=4)
        print("Settings saved successfully on close.")
    except (FileNotFoundError, PermissionError) as e:
        print(f"Error saving settings on close: {e}")
        QMessageBox.critical(main_window, "Error", f"Could not save settings on close. Check file permissions: {e}")
    except Exception as e:
        print(f"Error saving settings on close: {e}")
        QMessageBox.critical(main_window, "Error", f"Error saving settings: {e}")
