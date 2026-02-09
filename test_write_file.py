import os
import sys
import tempfile
import shutil
from functions.write_file import write_file

# Add parent directory to path to import the function
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))



def test_write_file_basic():
    """Test writing to a file in the working directory"""
    with tempfile.TemporaryDirectory() as tmpdir:
        result = write_file(tmpdir, os.path.join(tmpdir, "lorem.txt"), "wait, this isn't lorem ipsum")
        print(f"Test 1 - Basic write: {result}")
        assert "Successfully wrote" in result


def test_write_file_nested():
    """Test writing to a file in nested directories"""
    with tempfile.TemporaryDirectory() as tmpdir:
        result = write_file(tmpdir, os.path.join(tmpdir, "pkg/morelorem.txt"), "lorem ipsum dolor sit amet")
        print(f"Test 2 - Nested write: {result}")
        assert "Successfully wrote" in result


def test_write_file_outside_directory():
    """Test that writing outside working directory is prevented"""
    with tempfile.TemporaryDirectory() as tmpdir:
        result = write_file(tmpdir, "/tmp/temp.txt", "this should not be allowed")
        print(f"Test 3 - Outside directory: {result}")
        assert "Error" in result


if __name__ == "__main__":
    test_write_file_basic()
    test_write_file_nested()
    test_write_file_outside_directory()
    print("\nAll tests completed!")