import os
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtCore import QDir, QItemSelectionModel
from utils.file_utils import get_base_dir

def select_folder(main_window):
    """Handle project folder selection, remembering the last location and selecting contents."""
    folder_path = QFileDialog.getExistingDirectory(
        main_window, "Select Project Folder", main_window.recent_project_path
    )
    if folder_path:
        main_window.project_path = folder_path
        main_window.recent_project_path = folder_path  # Update recent path
        main_window.file_system_model.setRootPath(folder_path)
        root_index = main_window.file_system_model.index(folder_path)
        main_window.project_tree_view.setRootIndex(root_index)
        main_window.project_tree_view.expandToDepth(0)

        # Recursively select all items in the selected folder, only if enabled
        if main_window.recursive_selection_check.isChecked():
            select_all_in_folder(main_window, root_index, True)

def select_all_in_folder(main_window, folder_index, select):
    """Recursively select or deselect all items within a folder in the tree view."""
    if not folder_index.isValid():
        return

    current_selection_model = main_window.project_tree_view.selectionModel()
    if select and not current_selection_model.isSelected(folder_index):
        current_selection_model.select(folder_index, QItemSelectionModel.Select)
    elif not select and current_selection_model.isSelected(folder_index):
        current_selection_model.select(folder_index, QItemSelectionModel.Deselect)
    
    for row in range(main_window.file_system_model.rowCount(folder_index)):
        child_index = main_window.file_system_model.index(row, 0, folder_index)
        if child_index.isValid():
            if main_window.file_system_model.isDir(child_index):
                select_all_in_folder(main_window, child_index, select)
            else:
                if select and not current_selection_model.isSelected(child_index):
                    current_selection_model.select(child_index, QItemSelectionModel.Select)
                elif not select and current_selection_model.isSelected(child_index):
                    current_selection_model.select(child_index, QItemSelectionModel.Deselect)

def on_tree_selection_changed(main_window, selected, deselected):
    """Handle changes in tree view selection, including recursive selection/deselection."""
    if not main_window.recursive_selection_check.isChecked():
        return

    for index in selected.indexes():
        if main_window.file_system_model.isDir(index):
            select_all_in_folder(main_window, index, True)

    for index in deselected.indexes():
        if main_window.file_system_model.isDir(index):
            select_all_in_folder(main_window, index, False)

def reset_project_selection(main_window):
    """Resets the project folder selection."""
    main_window.project_path = None
    main_window.recent_project_path = ""
    QMessageBox.information(main_window, "Reset", "Project folder selection has been reset.")

def get_project_structure(directory):
    """Creates a string representation of the project directory structure."""
    structure = []
    base_path = os.path.basename(directory)
    structure.append(f"{base_path}/")

    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d != "__pycache__" and not d.startswith(".")]
        level = os.path.relpath(root, directory).count(os.sep) + 1
        if level > 1:
            indent = "  " * (level - 1) + "+-- "
        else:
            indent = ""

        for dir_name in sorted(dirs):
            structure.append(f"{indent}{dir_name}/")

        sub_indent = "  " * level + "+-- "
        for file in sorted(files):
            if not file.startswith("."):
                structure.append(f"{sub_indent}{file}")

    return "\n".join(structure)
