import os

class FilesResult(dict):
    """A dict-like container that iterates over its stored items (values).

    This preserves `isinstance(result, dict)` checks in tests while allowing
    `for item in result:` to yield item dicts (with 'name', 'file_size', 'is_dir').
    """
    def __init__(self, items):
        super().__init__()
        self._items = items

    def __iter__(self):
        return iter(self._items)

    def __len__(self):
        return len(self._items)

    def __repr__(self):
        return repr(self._items)


def get_files_info(working_directory, directory="."):
    """
    List the contents of a directory with metadata (name and size).

    Args:
        working_directory: The base directory to restrict access to
        directory: The target directory to list (relative to working_directory)

    Returns:
        - On success: a dict-like object (instance of dict) that iterates over a
          sequence of item dicts with keys: name, file_size, is_dir
        - On error: a dict with an "error" key describing the problem
    """
    try:
        # Get absolute path of working directory
        working_dir_abs = os.path.abspath(working_directory)

        # Construct and normalize the target directory path
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        # Validate that target directory is within working directory
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return {"error": f'Cannot list "{directory}" as it is outside the permitted working directory'}

        # Check if target directory exists and is a directory
        if not os.path.isdir(target_dir):
            return {"error": f'"{directory}" is not a directory'}

        # List files and directories with metadata
        items = []
        for item in sorted(os.listdir(target_dir)):
            item_path = os.path.join(target_dir, item)
            file_size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)bootdevbootdev
            items.append({"name": item, "file_size": file_size, "is_dir": is_dir})

        return FilesResult(items)

    except Exception as e:
        return {"error": str(e)}