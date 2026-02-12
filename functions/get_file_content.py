import os
from config import MAX_FILE_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):
    """
    Read and return the contents of a file within the working directory.
    
    Args:
        working_directory: The permitted directory path
        file_path: The path to the file to read
        
    Returns:
        The file contents as a string (up to MAX_FILE_CHARS characters),
        or an error message string if validation fails
    """
    try:
        # Resolve absolute paths
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
        
        # Validate that file_path is within working_directory
        if not abs_file_path.startswith(abs_working_dir + os.sep) and abs_file_path != abs_working_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        # Check if path exists and is a regular file
        if not os.path.isfile(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        # Read file content with character limit
        with open(abs_file_path, 'r', encoding='utf-8') as f:
            content = f.read(MAX_FILE_CHARS)

            # Check if file is larger than limit
            if f.read(1):
                content += '\n[Content truncated]'

        return content
        
    except Exception as e:
        return f'Error: {str(e)}'
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a specified file relative to the working directory, with a character limit",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)
