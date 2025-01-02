import logging
from PyQt5.QtWidgets import (
    QToolTip
)
from PyQt5.QtGui import QIcon
import os

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

def set_button_icon(button, icon_name, base_dir):
    """Helper function to set icon for a button."""
    icons_dir = os.path.join(base_dir, "icons")
    icon_path = os.path.join(icons_dir, icon_name)
    if os.path.exists(icon_path):
        icon = QIcon(icon_path)
        button.setIcon(icon)
        logging.debug(f"Icon set for {button.text()}: {icon_path}")
    else:
        logging.warning(f"Icon file not found: {icon_path}")

def set_menu_action_icon(action, icon_name, base_dir):
    """Helper function to set icon for a menu action."""
    icons_dir = os.path.join(base_dir, "icons")
    icon_path = os.path.join(icons_dir, icon_name)
    if os.path.exists(icon_path):
        icon = QIcon(icon_path)
        action.setIcon(icon)
        logging.debug(f"Icon set for action: {icon_path}")
    else:
        logging.warning(f"Icon file not found: {icon_path}")
