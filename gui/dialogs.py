import logging
from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QGroupBox,
    QLabel,
    QComboBox,
    QLineEdit,
    QSlider,
    QHBoxLayout,
    QPushButton,
    QMessageBox,
    QTextBrowser
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import json
import os

from gui.utils import apply_stylesheet
from utils.file_utils import get_base_dir

class APISettingsDialog(QDialog):
    """Dialog for editing API settings."""
    def __init__(self, settings, parent=None):
        """Initialize the API settings dialog.

        Args:
            settings (dict): The current API settings.
            parent (QWidget, optional): The parent widget. Defaults to None.
        """
        super().__init__(parent)
        self.api_settings = settings  # Use the passed settings
        apply_stylesheet(self)
        self.setWindowTitle('API Settings')
        self.setGeometry(200, 200, 400, 300)

        main_layout = QVBoxLayout()

        provider_group = QGroupBox("Provider Settings")
        provider_layout = QVBoxLayout()

        # Provider Selection
        provider_label = QLabel("Provider:")
        self.provider_combobox = QComboBox()
        self.provider_combobox.addItems(["OpenAI", "Google"])
        self.provider_combobox.currentTextChanged.connect(self.update_api_fields)
        provider_layout.addWidget(provider_label)
        provider_layout.addWidget(self.provider_combobox)
        provider_group.setLayout(provider_layout)
        main_layout.addWidget(provider_group)

        # API Key
        api_group = QGroupBox("API Key")
        api_layout = QVBoxLayout()
        self.api_key_label = QLabel("API Key:")
        self.api_key_edit = QLineEdit()
        api_layout.addWidget(self.api_key_label)
        api_layout.addWidget(self.api_key_edit)
        api_group.setLayout(api_layout)
        main_layout.addWidget(api_group)

        # Model Selection
        model_group = QGroupBox("Model Selection")
        model_layout = QVBoxLayout()
        model_label = QLabel("Model:")
        self.model_combobox = QComboBox()
        model_layout.addWidget(model_label)
        model_layout.addWidget(self.model_combobox)
        model_group.setLayout(model_layout)
        main_layout.addWidget(model_group)

        # Temperature
        temp_group = QGroupBox("Temperature")
        temp_layout = QVBoxLayout()
        temperature_label = QLabel("Temperature (0.0 - 1.0):")
        self.temperature_slider = QSlider(Qt.Horizontal)
        self.temperature_slider.setMinimum(0)
        self.temperature_slider.setMaximum(100)
        self.temperature_slider.setValue(70)  # Default value
        self.temperature_slider.valueChanged.connect(self.update_temperature_display)
        self.temperature_display_label = QLabel(f"{self.temperature_slider.value() / 100:.2f}")
        temp_layout.addWidget(temperature_label)
        temp_hbox = QHBoxLayout()
        temp_hbox.addWidget(self.temperature_slider)
        temp_hbox.addWidget(self.temperature_display_label)
        temp_layout.addLayout(temp_hbox)
        temp_group.setLayout(temp_layout)
        main_layout.addWidget(temp_group)

        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.setIcon(QIcon("icons/save.png"))
        save_button.clicked.connect(self.save_settings)
        reset_button = QPushButton("Reset")
        reset_button.setIcon(QIcon("icons/reset.png"))
        reset_button.clicked.connect(self.reset_settings)
        cancel_button = QPushButton("Cancel")
        cancel_button.setIcon(QIcon("icons/cancel.png"))
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(save_button)
        button_layout.addWidget(reset_button)
        button_layout.addWidget(cancel_button)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
        # Load settings for the default provider
        self.provider_combobox.setCurrentText("OpenAI")
        # Force initial update for OpenAI
        self.update_api_fields("OpenAI")
        self.load_settings_for_provider("OpenAI") # Load settings after UI is set up

    def update_temperature_display(self, value):
        """Updates the temperature display label."""
        self.temperature_display_label.setText(f"{value / 100:.2f}")

    def update_api_fields(self, provider_text):
        """Updates the API key label and model choices based on the selected provider."""
        print(f"Updating API fields for provider: {provider_text}")  # Debug print
        self.api_key_label.setText(f"{provider_text} API Key:")
        self.api_key_edit.clear()
        self.model_combobox.clear()
        if provider_text == "OpenAI":
            self.model_combobox.addItems(["gpt-4o", "gpt-4o-mini", "gpt-4", "gpt-3.5-turbo", "gpt-4-turbo"])
        elif provider_text == "Google":
            self.model_combobox.addItems(["gemini-1.5-pro","gemini-exp-1206","gemini-1.5-flash", "gemini-2.0-flash-exp","learnlm-1.5-pro-experimental","",""]) # Add the new Google model
        print(f"Model combobox items: {[self.model_combobox.itemText(i) for i in range(self.model_combobox.count())]}") # Debug print

    def load_settings_for_provider(self, provider):
        """Loads the settings for the specified provider."""
        provider_settings = self.api_settings.get(provider.lower(), {})
        api_key = provider_settings.get("api_key", "")
        if api_key:
            # Mask the API key for display
            self.api_key_edit.setText("*" * len(api_key)) # Changed to mask the entire key for security
        self.temperature_slider.setValue(int(provider_settings.get("temperature", 0.7) * 100))
        self.model_combobox.setCurrentText(provider_settings.get("model", ""))

    def save_settings(self):
        """Save the API settings."""
        provider = self.provider_combobox.currentText().lower()
        api_key = self.api_key_edit.text()
        temperature = self.temperature_slider.value() / 100
        model = self.model_combobox.currentText()

        # Update the settings for the current provider
        self.api_settings[provider] = {
            "api_key": api_key,
            "temperature": temperature,
            "model": model
        }

        try:
            settings_path = os.path.join(get_base_dir(), "settings.json")
            with open(settings_path, "w") as f:
                json.dump(self.api_settings, f, indent=4)
            QMessageBox.information(self, "Settings Saved", "API settings saved successfully.")
            self.accept()  # Close the dialog
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error saving settings: {e}")

    def reset_settings(self):
        """Resets the API settings for the current provider."""
        provider = self.provider_combobox.currentText().lower()
        if provider in self.api_settings:
            del self.api_settings[provider]
            self.load_settings_for_provider(provider)
            self.api_key_edit.clear()
            self.temperature_slider.setValue(70)
            self.model_combobox.setCurrentIndex(-1)
            QMessageBox.information(self, "Settings Reset", f"{provider.capitalize()} API settings have been reset.")
        else:
            QMessageBox.information(self, "No Settings", f"No settings found for {provider}.")

def show_llm_info_dialog(parent):
    """Displays a dialog with detailed information about LLMs."""
    dialog = QDialog(parent)
    dialog.setWindowTitle("LLM Information")
    dialog.setGeometry(200, 200, 500, 400)
    layout = QVBoxLayout(dialog)

    text_browser = QTextBrowser()
    text_browser.setOpenExternalLinks(True)

    info_text = """
    <h2>Understanding Language Models (LLMs)</h2>
    <p>Large Language Models can be used to generate documentation for your project, providing a high-level overview of its functionality and structure.</p>

    <h3>OpenAI Models</h3>
    <p>OpenAI offers powerful models like GPT-4o, GPT-4, and GPT-3.5-turbo. These models are excellent for understanding code and generating human-readable text.</p>
    <ul>
        <li><b>gpt-4o:</b> OpenAI's newest flagship model, designed for enhanced performance across text, vision, and audio.</li>
        <li><b>gpt-4o-mini:</b> A smaller, faster variant of gpt-4o, suitable for applications requiring quick responses.</li>
        <li><b>gpt-4:</b> A very capable model with a good balance of performance and cost. Ideal for complex projects.</li>
        <li><b>gpt-3.5-turbo:</b> A faster and more cost-effective model, suitable for smaller to medium-sized projects.</li>
        <li><b>gpt-4-turbo:</b> An optimized version of GPT-4, offering faster processing speeds and improved efficiency.</li>
    </ul>
    <p><b>Note:</b> OpenAI models have context window limits. For very large projects, you might need to consider the amount of code being processed at once.</p>

    <h3>Google Models</h3>
    <p>Google's Gemini models are designed for various generative tasks, including code understanding and documentation.</p>
    <ul>
        <li><b>gemini-1.5-pro:</b> A robust model capable of handling a wide range of tasks with high accuracy.</li>
        <li><b>gemini-exp-1206:</b> An experimental model designed for specific applications, offering unique capabilities.</li>
        <li><b>gemini-1.5-flash:</b> A faster variant of gemini-1.5-pro, optimized for speed.</li>
        <li><b>gemini-2.0-flash-exp:</b> An advanced experimental model with enhanced features and performance.</li>
        <li><b>learnlm-1.5-pro-experimental:</b> An experimental model focused on learning and adapting to new tasks efficiently.</li>
    </ul>
    <p><b>Key Advantage:</b> Google models generally offer larger context windows, making them well-suited for processing extensive codebases without losing context.</p>

    <h3>Choosing the Right Model</h3>
    <ul>
        <li>For <b>smaller projects</b> or when cost is a primary concern, <b>GPT-3.5-turbo</b> might be a good choice.</li>
        <li>For <b>complex projects</b> requiring high accuracy and detailed understanding, <b>GPT-4o</b> or <b>GPT-4</b> are recommended.</li>
        <li>For <b>large projects</b> with extensive code, <b>Google's Gemini models</b> are advantageous due to their larger context windows.</li>
    </ul>

    <p>You can configure the API keys and model settings in the "Settings" menu under "API Settings". Make sure to enter your API key for the selected provider.</p>
    """
    text_browser.setHtml(info_text)
    layout.addWidget(text_browser)

    close_button = QPushButton("Close", dialog)
    close_button.clicked.connect(dialog.accept)
    layout.addWidget(close_button)

    dialog.setLayout(layout)
    dialog.exec_()

def show_api_settings(parent, settings):
    """Display the API settings dialog."""
    dialog = APISettingsDialog(settings.copy(), parent=parent)
    dialog.load_settings_for_provider(dialog.provider_combobox.currentText())
    if dialog.exec_() == QDialog.Accepted:
        parent.api_settings = dialog.api_settings
        try:
            settings_path = os.path.join(get_base_dir(), "settings.json")
            with open(settings_path, "w") as f:
                json.dump(parent.api_settings, f, indent=4)
        except Exception as e:
            logging.error(f"Error saving API settings after dialog: {e}")
            QMessageBox.critical(parent, "Settings Error", f"Failed to save API settings: {e}")
