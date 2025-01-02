import os
import re
from pathlib import Path
from PyQt5.QtWidgets import QMessageBox, QInputDialog, QFileDialog

def recreate_project_from_text(main_window, doc_file, project_name, save_location):
    """
    Recreates a project structure and files from a documentation text file,
    handling files with extensions: .py, .json, .log, .yaml, .md, .ts, .mjs, .toml, .txt, .htm, .html.
    """
    print(
        f"Recreating project from TXT: {doc_file}, Project Name: {project_name}, Save Location: {save_location}"
    )
    project_path = os.path.join(save_location, project_name)

    try:
        with open(doc_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Parse the Markdown content (using regular expressions for simplicity)
        structure_match = re.search(r"## Project Structure\n+```(.*?)```", content, re.DOTALL)
        files_match = re.search(r"## Files Content(.*$)", content, re.DOTALL)

        if not structure_match:
            print("Project Structure section not found in documentation file.")
            QMessageBox.critical(main_window, "Error", "Project Structure section not found in documentation file.")
            return

        structure_section = structure_match.group(1).strip()
        files_section = files_match.group(1).strip() if files_match else ""

        # Recreate project structure
        current_dir_stack = []
        for line in structure_section.split("\n"):
            stripped_line = line.strip()
            if stripped_line.endswith("/"):
                dir_name = stripped_line.rstrip("/").replace("+-- ", "").strip()
                current_dir_stack.append(dir_name)
                dir_path = os.path.join(project_path, *current_dir_stack)
                os.makedirs(dir_path, exist_ok=True)
                print(f"Creating directory: {dir_path}")
            elif stripped_line and not stripped_line.startswith("+--"):
                file_name = stripped_line
                if current_dir_stack:
                    file_path = os.path.join(project_path, *current_dir_stack, file_name)
                else:
                    file_path = os.path.join(project_path, file_name)
                print(f"Creating file: {file_path}")
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                Path(file_path).touch()  # Create empty file

        # Recreate file content
        # Updated regex to handle more extensions and recognize code blocks
        file_blocks = re.findall(r"### File: (.*?)\n+```[a-z]*\n(.*?)\n```", files_section, re.DOTALL)
        for file_name, file_content in file_blocks:
            file_path = os.path.join(project_path, file_name.strip().replace("/", "\\"))
            print(f"Writing content to file: {file_path}")
            try:
                os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Create parent directories if they don't exist
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(file_content.strip())
            except Exception as e:
                print(f"Error writing to file {file_path}: {e}")
                QMessageBox.warning(main_window, "File Error", f"Error writing to file {file_name.strip()}: {e}")

        QMessageBox.information(main_window, "Success", f"Project recreated successfully at: {project_path}")
        print(f"Project recreated successfully at: {project_path}")

    except Exception as e:
        print(f"Error during project recreation: {e}")
        QMessageBox.critical(main_window, "Error", f"An error occurred during project recreation: {e}")

def recreate_project_from_docx(main_window, doc_file_path, project_name, save_location):
        """
        Recreates a project from a .docx documentation file.
        """
        txt_path = convert_docx_to_txt(doc_file_path)
        if txt_path:
            recreate_project_from_text(main_window, txt_path, project_name, save_location)
        else:
            QMessageBox.critical(
                main_window,
                "Error",
                "Failed to convert DOCX to TXT. Project reconstruction aborted."
            )
