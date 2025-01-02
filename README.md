# Project Manager Application

![Project Manager Screenshot](images/screenshot.png) <!-- Add a screenshot if available -->

The **Project Manager Application** is a powerful tool designed to help developers manage, document, and compress their projects efficiently. It supports both TXT and DOCX documentation formats and integrates with LLMs (Large Language Models) like OpenAI and Google for advanced project analysis.

---

## Features

- **Project Compression**: Compress your project into a single, well-organized documentation file (TXT or DOCX).
- **Project Reconstruction**: Reconstruct a project from a previously generated documentation file.
- **LLM Integration**: Use OpenAI or Google models to generate detailed project overviews and documentation.
- **File Explorer**: Browse and select files/folders within your project using an intuitive tree view.
- **Customizable Settings**: Configure API keys, LLM models, and other settings for seamless integration.
- **Recursive Selection**: Automatically select all files within a folder for compression.
- **Incompatible File Handling**: Identify and document files that cannot be processed.

---

## Installation

### Prerequisites

- Python 3.8 or higher
- PyQt5
- python-docx
- openai (for OpenAI integration)
- google-generativeai (for Google integration)
- chardet (for encoding detection)

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/project-manager.git
   cd project-manager
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py
   ```

---

## Usage

1. **Select a Project Folder**: Click "Select Project Folder" to choose the project you want to compress or reconstruct.
2. **Choose Documentation Format**: Select either TXT or DOCX format for the output documentation.
3. **Enable LLM (Optional)**: If you want to use an LLM for project analysis, enable the "Use LLM for Documentation" option and select the desired model.
4. **Compress or Reconstruct**:
   - **Compress**: Click "Process" to generate documentation for the selected project.
   - **Reconstruct**: Select a previously generated documentation file and click "Process" to reconstruct the project.
5. **View Output**: The generated documentation will be saved in the project folder.

---

## Configuration

### API Settings

To use OpenAI or Google models, configure your API keys in the "API Settings" dialog:
1. Go to **Settings > API Settings**.
2. Enter your API key and select the desired model.
3. Save the settings.

### Application Settings

Customize the application behavior in the "Settings" menu:
- **Output Format**: Choose between TXT and DOCX.
- **LLM Temperature**: Adjust the creativity level of the LLM.
- **Recursive Selection**: Enable/disable automatic selection of all files in a folder.

---

## File Structure

```
project-manager/
├── core/                  # Core functionality (project, document, processor, etc.)
├── gui/                   # GUI components (layout, dialogs, utils)
├── llm/                   # LLM integration (OpenAI, Google)
├── settings/              # Settings management
├── utils/                 # Utility functions (file handling, logging)
├── tests/                 # Unit tests
├── icons/                 # Application icons
├── main.py                # Main application entry point
├── README.md              # Project documentation
├── requirements.txt       # Python dependencies
└── settings.json          # Application settings
```

---

## Contributing

Contributions are welcome! Follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m 'Add your feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contact

For questions or feedback, feel free to reach out:

- **GitHub**: [your-username](https://github.com/Anonymousinterpares)
```

---

### Checklist for GitHub Upload

1. **Organize the Project Structure**:
   - Ensure all files are in the correct folders (`core/`, `gui/`, `llm/`, etc.).
   - Remove any unnecessary files or folders.

2. **Add a `.gitignore` File**:
   Create a `.gitignore` file to exclude unnecessary files (e.g., `__pycache__`, virtual environments, etc.).

   <boltArtifact id="gitignore" title=".gitignore">
   <boltAction type="file" filePath=".gitignore">
   __pycache__/
   *.pyc
   *.pyo
   *.pyd
   *.db
   *.sqlite3
   *.log
   .env
   venv/
   .vscode/
   .idea/
   *.DS_Store
