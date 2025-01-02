import os
import chardet

def _read_file_content(file_path):
    """
    Reads the content of a file with improved encoding handling and error reporting.
    """
    print(f"Attempting to read file: {file_path}")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            print(f"Read content (UTF-8) from {file_path}: {content[:20]}...")
            return content
    except UnicodeDecodeError:
        print(f"Trying alternative encodings for: {file_path}")
        try:
            with open(file_path, "rb") as f:
                rawdata = f.read()
                result = chardet.detect(rawdata)
                encoding = result['encoding']

            with open(file_path, "r", encoding=encoding) as f:
                content = f.read()
                print(f"Successfully read {file_path} using detected encoding: {encoding}")
                print(f"Read content ({encoding}) from {file_path}: {content[:20]}...")
                return content
        except ImportError:
            error_msg = f"ERROR: Could not read content due to encoding issues. Install 'chardet' for better encoding detection."
            print(error_msg)
            return error_msg
        except Exception as e_alt:
            error_msg = f"Error reading file with detected encoding: {file_path} - {e_alt}"
            print(error_msg)
            return error_msg
    except Exception as e:
        error_msg = f"Unexpected error reading file: {file_path} - {e}"
        print(error_msg)
        return error_msg

def has_extension(filename, extension):
    """
    Checks if a filename has a specific extension (case-insensitive).

    Args:
        filename: The filename to check.
        extension: The extension to check for (e.g., ".txt").

    Returns:
        True if the filename has the specified extension, False otherwise.
    """
    return filename.lower().endswith(extension.lower())

def has_any_extension(filename, extensions):
    """
    Checks if a filename has any of the specified extensions (case-insensitive).

    Args:
        filename: The filename to check.
        extensions: A list of extensions to check for (e.g., [".txt", ".py"]).

    Returns:
        True if the filename has any of the specified extensions, False otherwise.
    """
    for ext in extensions:
        if has_extension(filename, ext):
            return True
    return False
