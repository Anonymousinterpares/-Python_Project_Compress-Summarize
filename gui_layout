import logging
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QMainWindow,
    QAction,
    QInputDialog,
    QCheckBox,
    QGroupBox,
    QVBoxLayout,
    QHBoxLayout,
    QRadioButton,
    QLabel,
    QGridLayout,
    QLineEdit,
    QDialog,
    QSlider,
    QComboBox,
    QToolTip,
    QTextBrowser,
    QSizePolicy,
    QFrame,
    QSpacerItem,
    QButtonGroup,
    QTreeView, # Ensure QTreeView is here
    QFileSystemModel
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
def apply_stylesheet(widget):
    """Applies a basic modern stylesheet to the given widget."""
    try:
        widget.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QDialog {
                background-color: #f0f0f0;
            }
            QGroupBox {
                border: 1px solid #c0c0c0;
                border-radius: 5px;
                margin-top: 10px;
                padding: 10px;
                font-size: 14px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 5px;
                background-color: #f0f0f0;
                font-weight: bold;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #003d80;
            }
            QRadioButton, QCheckBox {
                spacing: 5px;
                font-size: 14px;
            }
            QLabel {
                font-size: 14px;
            }
            QLineEdit {
                border: 1px solid #c0c0c0;
                border-radius: 3px;
                padding: 5px;
                font-size: 14px;
            }
            QComboBox {
                border: 1px solid #c0c0c0;
                border-radius: 3px;
                padding: 5px;
                font-size: 14px;
            }
            QTextBrowser {
                border: 1px solid #c0c0c0;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                background-color: white;
            }
            QMenuBar {
                background-color: #e0e0e0;
                font-size: 14px;
            }
            QMenuBar::item {
                background-color: transparent;
            }
            QMenuBar::item:selected {
                background-color: #c0c0c0;
            }
            QMenu {
                background-color: #f0f0f0;
                border: 1px solid #c0c0c0;
                font-size: 14px;
            }
            QMenu::item:selected {
                background-color: #c0c0c0;
            }
        """)
    except Exception as e:
        logging.error(f"Error applying stylesheet: {e}")

def init_api_settings_ui(dialog, settings):
    """Initialize the user interface components and layout for APISettingsDialog."""

    apply_stylesheet(dialog) # Apply the stylesheet
    dialog.setWindowTitle('API Settings')
    dialog.setGeometry(200, 200, 400, 300)

    main_layout = QVBoxLayout()

    provider_group = QGroupBox("Provider Settings")
    provider_layout = QVBoxLayout()

    # Provider Selection
    provider_label = QLabel("Provider:")
    provider_combobox = QComboBox()
    provider_combobox.addItems(["OpenAI", "Google"])
    provider_layout.addWidget(provider_label)
    provider_layout.addWidget(provider_combobox)
    provider_group.setLayout(provider_layout)
    main_layout.addWidget(provider_group)

    # API Key
    api_group = QGroupBox("API Key")
    api_layout = QVBoxLayout()
    api_key_label = QLabel("API Key:")
    api_key_edit = QLineEdit()
    api_layout.addWidget(api_key_label)
    api_layout.addWidget(api_key_edit)
    api_group.setLayout(api_layout)
    main_layout.addWidget(api_group)

    # Model Selection
    model_group = QGroupBox("Model Selection")
    model_layout = QVBoxLayout()
    model_label = QLabel("Model:")
    model_combobox = QComboBox()
    model_layout.addWidget(model_label)
    model_layout.addWidget(model_combobox)
    model_group.setLayout(model_layout)
    main_layout.addWidget(model_group)

    # Temperature
    temp_group = QGroupBox("Temperature")
    temp_layout = QVBoxLayout()
    temperature_label = QLabel("Temperature (0.0 - 1.0):")
    temperature_slider = QSlider(Qt.Horizontal)
    temperature_slider.setMinimum(0)
    temperature_slider.setMaximum(100)
    temperature_slider.setValue(70) # Default value
    temperature_display_label = QLabel(f"{temperature_slider.value() / 100:.2f}")
    temp_layout.addWidget(temperature_label)
    temp_hbox = QHBoxLayout()
    temp_hbox.addWidget(temperature_slider)
    temp_hbox.addWidget(temperature_display_label)
    temp_layout.addLayout(temp_hbox)
    temp_group.setLayout(temp_layout)
    main_layout.addWidget(temp_group)

    # Buttons
    button_layout = QHBoxLayout()
    save_button = QPushButton("Save")
    save_button.setIcon(QIcon("icons/save.png"))
    reset_button = QPushButton("Reset")
    reset_button.setIcon(QIcon("icons/reset.png"))
    cancel_button = QPushButton("Cancel")
    cancel_button.setIcon(QIcon("icons/cancel.png"))
    button_layout.addWidget(save_button)
    button_layout.addWidget(reset_button)
    button_layout.addWidget(cancel_button)
    main_layout.addLayout(button_layout)

    dialog.setLayout(main_layout)

    # Store widgets for later use
    dialog.provider_combobox = provider_combobox
    dialog.api_key_edit = api_key_edit
    dialog.model_combobox = model_combobox
    dialog.temperature_slider = temperature_slider
    dialog.temperature_display_label = temperature_display_label
    dialog.save_button = save_button
    dialog.reset_button = reset_button
    dialog.cancel_button = cancel_button
    dialog.api_key_label = api_key_label

    return dialog


def init_project_manager_ui(main_window):
    """Initialize the user interface components and layout for ProjectManagerGUI."""

    apply_stylesheet(main_window) # Apply the stylesheet
    main_window.setWindowTitle('Project Manager')
    # Remove setGeometry() to allow for full-screen

    # Central Widget
    central_widget = QWidget(main_window)
    main_window.setCentralWidget(central_widget)

    # Main Layout using QGridLayout
    layout = QGridLayout()
    central_widget.setLayout(layout)

    # --- Row 0: Project Selection ---
    project_group = QGroupBox("Project Selection")
    project_layout = QHBoxLayout()
    select_project_button = QPushButton('Select Project Folder')
    select_project_button.setIcon(QIcon("icons/folder.png"))
    select_project_button.setMinimumWidth(150)  # Adjust button size
    reset_project_button = QPushButton('Reset')
    reset_project_button.setIcon(QIcon("icons/reset.png"))
    reset_project_button.setMinimumWidth(150)  # Adjust button size
    project_layout.addWidget(select_project_button)
    project_layout.addWidget(reset_project_button)
    project_group.setLayout(project_layout)
    layout.addWidget(project_group, 0, 0, 1, 2) # Span 2 columns

    # --- Row 1: Project Explorer ---
    explorer_group = QGroupBox("Project Explorer")
    explorer_layout = QVBoxLayout()
    main_window.project_tree_view = QTreeView() # Initialize the tree view
    main_window.project_tree_view.setSelectionMode(QTreeView.MultiSelection) # Enable multiple selection
    main_window.project_tree_view.setAlternatingRowColors(True)
    main_window.project_tree_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    explorer_layout.addWidget(main_window.project_tree_view)
    explorer_group.setLayout(explorer_layout)
    layout.addWidget(explorer_group, 1, 0, 1, 2) # Span 2 columns

    # --- Row 2: Documentation Selection ---
    doc_group = QGroupBox("Documentation Selection")
    doc_layout = QHBoxLayout()
    select_doc_button = QPushButton('Select Documentation File')
    select_doc_button.setIcon(QIcon("icons/file.png"))
    select_doc_button.setMinimumWidth(150)
    reset_doc_button = QPushButton('Reset')
    reset_doc_button.setIcon(QIcon("icons/reset.png"))
    reset_doc_button.setMinimumWidth(150)
    doc_layout.addWidget(select_doc_button)
    doc_layout.addWidget(reset_doc_button)
    doc_group.setLayout(doc_layout)
    layout.addWidget(doc_group, 2, 0, 1, 2) # Span 2 columns

    # --- Row 3: File Format ---
    format_group = QGroupBox("File Format")
    format_layout = QVBoxLayout()
    docx_radio = QRadioButton("DOCX Format")
    txt_radio = QRadioButton("TXT Format")
    txt_radio.setChecked(True)  # Default to TXT
    format_layout.addWidget(docx_radio)
    format_layout.addWidget(txt_radio)
    format_group.setLayout(format_layout)
    layout.addWidget(format_group, 3, 0)

    # --- Row 3: Action ---
    action_group = QGroupBox("Action")
    action_layout = QVBoxLayout()
    compress_radio = QRadioButton("Compress Project")
    reconstruct_radio = QRadioButton("Reconstruct Project")
    compress_radio.setChecked(True)  # Default to Compress
    action_layout.addWidget(compress_radio)
    action_layout.addWidget(reconstruct_radio)
    action_group.setLayout(action_layout)
    layout.addWidget(action_group, 3, 1)

    # --- Row 4: LLM Options ---
    llm_group = QGroupBox("LLM Options")
    llm_layout = QVBoxLayout()
    use_llm_check = QCheckBox("Use LLM for Documentation")
    llm_layout.addWidget(use_llm_check)
    llm_type_label = QLabel("LLM Type:")
    llm_layout.addWidget(llm_type_label)
    none_radio = QRadioButton("None")
    openai_radio = QRadioButton("OpenAI")
    google_radio = QRadioButton("Google")
    none_radio.setChecked(True)

    # Create a button group for LLM type
    main_window.llm_type_group = QButtonGroup() # Store the button group in the main window
    main_window.llm_type_group.addButton(none_radio)
    main_window.llm_type_group.addButton(openai_radio)
    main_window.llm_type_group.addButton(google_radio)
    none_radio.toggled.connect(lambda: logging.info("None radio toggled"))
    openai_radio.toggled.connect(lambda: logging.info("OpenAI radio toggled"))
    google_radio.toggled.connect(lambda: logging.info("Google radio toggled"))

    print(f"LLM Type Group buttons: {main_window.llm_type_group.buttons()}") # Debugging

    # Set tooltips for LLM options
    QToolTip.setFont(main_window.font())  # Ensure tooltips use the application font
    openai_radio.setToolTip(
        "<b>OpenAI Models</b><br>"
        "Utilizes OpenAI's language models for documentation.<br>"
        "Consider context window limits for larger projects."
    )
    google_radio.setToolTip(
        "<b>Google Models</b><br>"
        "Utilizes Google's Gemini models for documentation.<br>"
        "Offers a larger context window suitable for bigger projects."
    )
    hbox_llm = QHBoxLayout()
    hbox_llm.addWidget(none_radio)
    hbox_llm.addWidget(openai_radio)
    hbox_llm.addWidget(google_radio)
    llm_layout.addLayout(hbox_llm)
    overview_label = QLabel("Overview Type:")
    general_radio = QRadioButton("General")
    detailed_radio = QRadioButton("Detailed")
    general_radio.setChecked(True)
    llm_layout.addWidget(overview_label)
    llm_layout.addWidget(general_radio)
    llm_layout.addWidget(detailed_radio)

    # Create a button group for overview type
    main_window.overview_type_group = QButtonGroup() # Store the button group in the main window
    main_window.overview_type_group.addButton(general_radio)
    main_window.overview_type_group.addButton(detailed_radio)
    general_radio.toggled.connect(lambda: logging.info("General radio toggled"))
    detailed_radio.toggled.connect(lambda: logging.info("Detailed radio toggled"))

    print(f"Overview Type Group buttons: {main_window.overview_type_group.buttons()}") # Debugging

    # Button to show detailed LLM info
    llm_info_button = QPushButton("LLM Info...")
    llm_info_button.setIcon(QIcon("icons/info.png"))
    llm_info_button.setMinimumWidth(150)
    llm_layout.addWidget(llm_info_button)
    llm_group.setLayout(llm_layout)
    layout.addWidget(llm_group, 4, 0, 1, 2) # Span 2 columns

    # --- Row 5: Process Button ---
    process_button = QPushButton('Process')
    process_button.setIcon(QIcon("icons/process.png"))
    process_button.setMinimumWidth(150)
    layout.addWidget(process_button, 5, 0, 1, 2) # Span 2 columns

    # --- Row 6: Toggle for QTreeView selection behavior ---
    selection_toggle_group = QGroupBox("Tree View Selection")
    selection_toggle_layout = QVBoxLayout()
    main_window.recursive_selection_check = QCheckBox("Recursive Selection")
    main_window.recursive_selection_check.setChecked(True)  # Default to recursive selection
    selection_toggle_layout.addWidget(main_window.recursive_selection_check)
    selection_toggle_group.setLayout(selection_toggle_layout)
    layout.addWidget(selection_toggle_group, 6, 0, 1, 2)  # Span 2 columns

    # Store widgets for later use
    main_window.select_project_button = select_project_button
    main_window.reset_project_button = reset_project_button
    main_window.select_doc_button = select_doc_button
    main_window.reset_doc_button = reset_doc_button
    main_window.docx_radio = docx_radio
    main_window.txt_radio = txt_radio
    main_window.compress_radio = compress_radio
    main_window.reconstruct_radio = reconstruct_radio
    main_window.use_llm_check = use_llm_check
    main_window.none_radio = none_radio
    main_window.openai_radio = openai_radio
    main_window.google_radio = google_radio
    main_window.general_radio = general_radio
    main_window.detailed_radio = detailed_radio
    main_window.llm_info_button = llm_info_button
    main_window.process_button = process_button

    return main_window
