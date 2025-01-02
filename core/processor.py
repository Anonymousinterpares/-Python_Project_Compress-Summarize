import os
from PyQt5.QtWidgets import QMessageBox, QInputDialog, QFileDialog
from core.utils import has_any_extension, _read_file_content  # Import _read_file_content

def process_project(main_window):
    """Handle the main project processing logic."""
    print("Starting project processing")

    if main_window.compress_radio.isChecked():
        print("Compress project option selected")
        # Handle compression (documentation generation)
        if not main_window.project_path:
            QMessageBox.warning(main_window, "Error", "Please select a project folder first.")
            print("No project folder selected for compression")
            return

        # Get selected files for individual compression
        selected_indexes = main_window.project_tree_view.selectionModel().selectedRows()
        main_window.selected_files_for_compression = [main_window.file_system_model.filePath(index) for index in selected_indexes if main_window.file_system_model.fileInfo(index).isFile()]
        print(f"Selected files for individual compression: {main_window.selected_files_for_compression}")

        llm_output = None
        if main_window.use_llm_check.isChecked():
            print("Fetching LLM documentation...")
            project_text_content_for_llm = get_project_content_for_llm(main_window, main_window.project_path)
            if project_text_content_for_llm:
                llm_output = main_window.generate_llm_documentation(project_text_content_for_llm)
                if llm_output:
                    print("LLM documentation fetched successfully.")
                else:
                    print("LLM documentation generation failed.")
            else:
                print("Could not extract project content for LLM.")
        else:
            # Explicitly check the "None" radio button if LLM is not used
            main_window.none_radio.setChecked(True)

        if main_window.txt_radio.isChecked():
            print("TXT format selected")
            main_window.convert_project_to_text(main_window.project_path, llm_overview=llm_output)

        elif main_window.docx_radio.isChecked():
            print("DOCX format selected")
            main_window.create_project_documentation(main_window.project_path, llm_content=llm_output)

    elif main_window.reconstruct_radio.isChecked():
        print("Reconstruct project option selected")
        # Handle reconstruction
        if not main_window.doc_file_path:
            QMessageBox.warning(
                main_window, "Error", "Please select a documentation file first."
            )
            print("No documentation file selected for reconstruction")
            return

        if main_window.doc_file_path.endswith(".txt"):
            print("TXT format selected for reconstruction")
            project_name, ok = QInputDialog.getText(
                main_window, "Project Name", "Enter the name for the reconstructed project:"
            )
            if ok and project_name:
                save_location = QFileDialog.getExistingDirectory(
                    main_window, "Select Save Location"
                )
                if save_location:
                    main_window.recreate_project_from_text(
                        main_window.doc_file_path, project_name, save_location
                    )
        elif main_window.doc_file_path.endswith(".docx"):
            print("DOCX format selected for reconstruction")
            project_name, ok = QInputDialog.getText(
                main_window, "Project Name", "Enter the name for the reconstructed project:"
            )
            if ok and project_name:
                save_location = QFileDialog.getExistingDirectory(
                    main_window, "Select Save Location"
                )
                if save_location:
                    main_window.recreate_project_from_docx(
                        main_window.doc_file_path, project_name, save_location
                    )
        else:
            QMessageBox.warning(
                main_window,
                "Error",
                "Invalid documentation file type for reconstruction. Select a .txt file.",
            )
            print(
                f"Invalid documentation file type selected for reconstruction: {main_window.doc_file_path}"
            )

def update_action_state(main_window):
    """Updates the state of the action radio buttons based on the selected file format."""
    if main_window.docx_radio.isChecked():
        main_window.compress_radio.setChecked(True)
        main_window.compress_radio.setEnabled(False)
        main_window.reconstruct_radio.setEnabled(True)
    elif main_window.txt_radio.isChecked():
        main_window.compress_radio.setEnabled(True)
        main_window.reconstruct_radio.setEnabled(True)

def _process_single_file(main_window, root, file, project_path):
    """Processes a single file and returns its formatted content as a list of lines."""
    file_path = os.path.join(root, file)
    rel_path = os.path.relpath(file_path, project_path)
    print(f"Processing file: {rel_path}")

    file_lines = []

    if has_any_extension(file, [".py", ".json", ".log", ".yaml", ".yml", ".svg", ".lock", ".scss", ".cts", ".cjs", ".js", ".map", ".mts", ".tsx", ".md", ".ts", ".mjs", ".toml", ".txt", ".htm", ".html", ".mdx", ".css", ".markdown", ".node", ".cmd", ".ninja", ".sh", ".cc", ".cs", ".bash", ".fish", ".ps1", ".zsh"]):
        print(f"Matched extension for: {rel_path}")
        file_lines.append(f"### File: {rel_path}\n\n")

        try:
            # Call _read_file_content as a standalone function
            content = _read_file_content(file_path)
            print(f"Content read for {rel_path}:\n{content[:50]}...")

            # Determine the appropriate code block markdown based on file extension
            if file.endswith((".py", ".cts", ".js", ".mjs", ".ts", ".tsx", ".cs")):
                file_lines.append("```python\n")
            elif file.endswith((".json", ".yaml", ".yml", ".toml", ".map", ".node", ".ninja")):
                file_lines.append("```json\n")
            elif file.endswith((".md", ".markdown", ".mdx")):
                file_lines.append("```markdown\n")
            elif file.endswith((".htm", ".html")):
                file_lines.append("```html\n")
            elif file.endswith((".scss", ".css")):
                file_lines.append("```css\n")
            elif file.endswith((".svg",".lock")):
                file_lines.append("```xml\n")
            elif file.endswith((".sh", ".cmd", ".bash", ".fish", ".zsh", ".ps1")):
                file_lines.append("```bash\n")
            elif file.endswith((".cc")):
                file_lines.append("```cpp\n")
            else:
                file_lines.append("```text\n")

            file_lines.append(content)
            file_lines.append("\n```\n\n")
        except Exception as e:
            print(f"Error processing file {rel_path}: {e}")
            file_lines.append(f"Error reading file: {str(e)}\n\n")
    else:
        print(f"Skipping incompatible file: {rel_path}")

    return file_lines

def get_project_content_for_llm(main_window, project_path):
    """
    Extracts content from project files for LLM processing, handling more extensions.

    Args:
        project_path (str): Path to the project directory

    Returns:
        str: Concatenated content of all relevant project files
    """
    project_content_for_llm = ""
    for root, _, files in os.walk(project_path):
        for file in files:
            if has_any_extension(file, [".py", ".json", ".log", ".yaml", ".yml", ".svg", ".lock", ".scss", ".cts", ".cjs", ".js", ".map", ".mts", ".tsx", ".md", ".ts", ".mjs", ".toml", ".txt", ".htm", ".html"]) and not file.startswith("."):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, project_path)
                try:
                    with open(file_path, "r", encoding="utf-8") as sourcefile:
                        content = sourcefile.read()
                        project_content_for_llm += f"File: {rel_path}\n{content}\n\n"
                except UnicodeDecodeError:
                    print(f"Trying alternative encodings for: {file_path}")
                    try:
                        # Use chardet to detect encoding
                        import chardet
                        with open(file_path, "rb") as f:
                            rawdata = f.read()
                            result = chardet.detect(rawdata)
                            encoding = result['encoding']
                        
                        with open(file_path, "r", encoding=encoding) as sourcefile:
                            content = sourcefile.read()
                            project_content_for_llm += f"File (read as {encoding}): {rel_path}\n{content}\n\n"
                            print(f"Successfully read {file_path} using detected encoding: {encoding}")

                    except ImportError:
                        print("chardet library not found. Please install it using 'pip install chardet'")
                        project_content_for_llm += f"File (encoding error): {rel_path}\nCould not read content due to encoding issues. Install 'chardet' for better encoding detection.\n\n"

                    except Exception as e_alt:
                        print(f"Error reading file with detected encoding: {file_path} - {e_alt}")
                        project_content_for_llm += f"File (encoding error): {rel_path}\nCould not read content due to encoding issues.\n\n"

                except Exception as e:
                    print(f"Unexpected error reading file for LLM: {file_path} - {e}")
    return project_content_for_llm
