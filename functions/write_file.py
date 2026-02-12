import os
from google.genai import types
def write_file(working_directory, file_path, content):
    """
    Write content to a file, creating parent directories as needed.
    
    Args:
        working_directory: The base directory that file_path must be within
        file_path: The path to the file to write
        content: The content to write to the file
        
    Returns:
        Success message or error string
    """
    # Validate that file_path is within working_directory
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(file_path)
    
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    # Check if file_path points to a directory
    if os.path.isdir(abs_file_path):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    
    # Create parent directories if they don't exist
    parent_dir = os.path.dirname(abs_file_path)
    if parent_dir:
        os.makedirs(parent_dir, exist_ok=True)
    
    # Write content to file
    with open(abs_file_path, "w") as f:
        f.write(content)
    
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a specified file relative to the working directory, creating parent directories as needed",
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
