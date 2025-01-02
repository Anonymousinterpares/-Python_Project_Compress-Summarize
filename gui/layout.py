import logging
from PyQt5.QtWidgets import (
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
    QSlider,
    QComboBox,
    QToolTip,
    QTreeView,
    QSizePolicy,
    QFileSystemModel,
    QButtonGroup
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QDir, QItemSelectionModel

from gui.utils import apply_stylesheet
from settings.settings_manager import load_app_settings
from utils.file_utils import get_base_dir
from gui.dialogs import show_api_settings  # Import the show_api_settings function

def init_project_manager_ui(main_window):
    """Initialize the user interface components and layout for ProjectManagerGUI."""

    apply_stylesheet(main_window)
    main_window.setWindowTitle('Project Manager')

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
    select_project_button.setIcon(QIcon(main_window.icons_dir + "/folder.png"))
    select_project_button.setMinimumWidth(150)
    reset_project_button = QPushButton('Reset')
    reset_project_button.setIcon(QIcon(main_window.icons_dir + "/reset.png"))
    reset_project_button.setMinimumWidth(150)
    project_layout.addWidget(select_project_button)
    project_layout.addWidget(reset_project_button)
    project_group.setLayout(project_layout)
    layout.addWidget(project_group, 0, 0, 1, 2)

    # --- Row 1: Project Explorer ---
    explorer_group = QGroupBox("Project Explorer")
    explorer_layout = QVBoxLayout()
    main_window.project_tree_view = QTreeView()
    main_window.project_tree_view.setSelectionMode(QTreeView.MultiSelection)
    main_window.project_tree_view.setAlternatingRowColors(True)
    main_window.project_tree_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    explorer_layout.addWidget(main_window.project_tree_view)
    explorer_group.setLayout(explorer_layout)
    layout.addWidget(explorer_group, 1, 0, 1, 2)

    # --- Row 2: Documentation Selection ---
    doc_group = QGroupBox("Documentation Selection")
    doc_layout = QHBoxLayout()
    select_doc_button = QPushButton('Select Documentation File')
    select_doc_button.setIcon(QIcon(main_window.icons_dir + "/file.png"))
    select_doc_button.setMinimumWidth(150)
    reset_doc_button = QPushButton('Reset')
    reset_doc_button.setIcon(QIcon(main_window.icons_dir + "/reset.png"))
    reset_doc_button.setMinimumWidth(150)
    doc_layout.addWidget(select_doc_button)
    doc_layout.addWidget(reset_doc_button)
    doc_group.setLayout(doc_layout)
    layout.addWidget(doc_group, 2, 0, 1, 2)

    # --- Row 3: File Format ---
    format_group = QGroupBox("File Format")
    format_layout = QVBoxLayout()
    docx_radio = QRadioButton("DOCX Format")
    txt_radio = QRadioButton("TXT Format")
    txt_radio.setChecked(True)
    format_layout.addWidget(docx_radio)
    format_layout.addWidget(txt_radio)
    format_group.setLayout(format_layout)
    layout.addWidget(format_group, 3, 0)

    # --- Row 3: Action ---
    action_group = QGroupBox("Action")
    action_layout = QVBoxLayout()
    compress_radio = QRadioButton("Compress Project")
    reconstruct_radio = QRadioButton("Reconstruct Project")
    compress_radio.setChecked(True)
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

    main_window.llm_type_group = QButtonGroup()
    main_window.llm_type_group.addButton(none_radio)
    main_window.llm_type_group.addButton(openai_radio)
    main_window.llm_type_group.addButton(google_radio)

    QToolTip.setFont(main_window.font())
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

    main_window.overview_type_group = QButtonGroup()
    main_window.overview_type_group.addButton(general_radio)
    main_window.overview_type_group.addButton(detailed_radio)

    llm_info_button = QPushButton("LLM Info...")
    llm_info_button.setIcon(QIcon(main_window.icons_dir + "/info.png"))
    llm_info_button.setMinimumWidth(150)
    llm_layout.addWidget(llm_info_button)
    llm_group.setLayout(llm_layout)
    layout.addWidget(llm_group, 4, 0, 1, 2)

    # --- Row 5: Process Button ---
    process_button = QPushButton('Process')
    process_button.setIcon(QIcon(main_window.icons_dir + "/process.png"))
    process_button.setMinimumWidth(150)
    layout.addWidget(process_button, 5, 0, 1, 2)

    # --- Row 6: Toggle for QTreeView selection behavior ---
    selection_toggle_group = QGroupBox("Tree View Selection")
    selection_toggle_layout = QVBoxLayout()
    main_window.recursive_selection_check = QCheckBox("Recursive Selection")
    main_window.recursive_selection_check.setChecked(True)
    selection_toggle_layout.addWidget(main_window.recursive_selection_check)
    selection_toggle_group.setLayout(selection_toggle_layout)
    layout.addWidget(selection_toggle_group, 6, 0, 1, 2)

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

    # Load application settings
    app_settings = load_app_settings(get_base_dir())
    main_window.recursive_selection_check.setChecked(app_settings.get("recursive_selection", True))

    return main_window

def _init_menu(main_window):
    """Initializes the menu bar."""
    menubar = main_window.menuBar()
    file_menu = menubar.addMenu('&File')
    settings_menu = menubar.addMenu('&Settings')

    main_window.exit_action = QAction('Exit')
    main_window.exit_action.setShortcut('Ctrl+Q')
    file_menu.addAction(main_window.exit_action)

    main_window.api_settings_action = QAction('API Settings')
    main_window.api_settings_action.triggered.connect(lambda: show_api_settings(main_window, main_window.api_settings))  # Connect the action
    settings_menu.addAction(main_window.api_settings_action)

    main_window.set_menu_action_icon(main_window.api_settings_action, "settings.png")
    main_window.set_menu_action_icon(main_window.exit_action, "exit.png")

def _init_buttons(main_window):
    """Initializes the buttons and sets their icons."""
    main_window.set_button_icon(main_window.select_project_button, "folder.png")
    main_window.set_button_icon(main_window.reset_project_button, "reset.png")
    main_window.set_button_icon(main_window.select_doc_button, "file.png")
    main_window.set_button_icon(main_window.reset_doc_button, "reset.png")
    main_window.set_button_icon(main_window.llm_info_button, "info.png")
    main_window.set_button_icon(main_window.process_button, "process.png")

def _init_connections(main_window):
    """Initializes the connections between signals and slots."""
    main_window.select_project_button.clicked.connect(main_window.select_folder)
    main_window.reset_project_button.clicked.connect(main_window.reset_project_selection)
    main_window.select_doc_button.clicked.connect(main_window.select_file)
    main_window.reset_doc_button.clicked.connect(main_window.reset_doc_selection)
    main_window.docx_radio.toggled.connect(main_window.update_action_state)
    main_window.txt_radio.toggled.connect(main_window.update_action_state)
    main_window.llm_info_button.clicked.connect(main_window.show_llm_info_dialog)
    main_window.process_button.clicked.connect(main_window.process_project)
    main_window.update_action_state()
    main_window.use_llm_check.stateChanged.connect(main_window.update_llm_options_state)
    main_window.update_llm_options_state(main_window.use_llm_check.checkState())
    main_window.project_tree_view.selectionModel().selectionChanged.connect(
        main_window.on_tree_selection_changed
    )

def update_llm_options_state(main_window, state):
    """Enables or disables LLM options based on the checkbox state."""
    enabled = state == Qt.Checked
    main_window.none_radio.setEnabled(enabled)
    main_window.openai_radio.setEnabled(enabled)
    main_window.google_radio.setEnabled(enabled)
    main_window.general_radio.setEnabled(enabled)
    main_window.detailed_radio.setEnabled(enabled)
    main_window.llm_info_button.setEnabled(enabled)
