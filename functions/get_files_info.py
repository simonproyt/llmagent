import os

def get_files_info(working_directory, directory="."):
    """
    List the contents of a directory with metadata (name and size).
    
    Args:
        working_directory: The base directory to restrict access to
        directory: The target directory to list (relative to working_directory)
    
    Returns:
        A string describing the directory contents or an error message
    """
    try:
        # Get absolute path of working directory
        working_dir_abs = os.path.abspath(working_directory)
        
        # Construct and normalize the target directory path
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        
        # Validate that target directory is within working directory
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        # Check if target directory exists and is a directory
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        
        # List files and directories with metadata
        items = []
        for item in sorted(os.listdir(target_dir)):
            item_path = os.path.join(target_dir, item)
            file_size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
            items.append(f"- {item}: file_size={file_size} bytes, is_dir={is_dir}")
        
        return "\n".join(items)
    
    except Exception as e:
        return f"Error: {str(e)}"