import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        # Resolve paths to absolute paths
        working_directory_abs = os.path.abspath(working_directory)
        full_path = os.path.abspath(os.path.join(working_directory, file_path))
        
        # Check if file_path is within working_directory
        if not full_path.startswith(working_directory_abs):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        # Check if file exists and is a regular file
        if not os.path.isfile(full_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        # Check if file is a Python file
        if not full_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        
        # Build the command
        command = ["python", full_path]
        if args:
            command.extend(args)
        
        # Run the subprocess
        result = subprocess.run(
            command,
            cwd=working_directory,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Build output string
        output = ""
        
        if result.returncode != 0:
            output += f"Process exited with code {result.returncode}\n"
        
        if not result.stdout and not result.stderr:
            output += "No output produced"
        else:
            if result.stdout:
                output += f"STDOUT:\n{result.stdout}"
            if result.stderr:
                output += f"STDERR:\n{result.stderr}"
        
        return output.rstrip()
    
    except Exception as e:
        return f"Error: executing Python file: {e}"
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a specified Python file relative to the working directory with optional arguments",
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
