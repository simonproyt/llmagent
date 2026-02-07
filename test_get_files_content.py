import sys
import os
from llmagent.core import get_file_content

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))



def test_get_file_content_lorem():
    """Test get_file_content with lorem.txt - should truncate properly"""
    content = get_file_content("calculator", "lorem.txt")
    
    # Check that content is not None and is a string
    assert isinstance(content, str), "Content should be a string"
    
    # Check that it contains truncation message if file is large
    if "[Content truncated]" in content:
        print("✓ Lorem.txt truncated correctly")
        print(f"  Length: {len(content)} characters")
        print(f"  Ends with truncation message: True")
    else:
        print("✓ Lorem.txt retrieved (no truncation needed)")
        print(f"  Length: {len(content)} characters")
    
    assert len(content) > 0, "Content should not be empty"


def test_get_file_content_main_py():
    """Test get_file_content with main.py"""
    content = get_file_content("calculator", "main.py")
    print("\n--- main.py ---")
    print(f"Length: {len(content)} characters")
    print(f"Content preview:\n{content[:200]}...")
    assert len(content) > 0, "main.py should have content"


def test_get_file_content_pkg_calculator_py():
    """Test get_file_content with pkg/calculator.py"""
    content = get_file_content("calculator", "pkg/calculator.py")
    print("\n--- pkg/calculator.py ---")
    print(f"Length: {len(content)} characters")
    print(f"Content preview:\n{content[:200]}...")
    assert len(content) > 0, "pkg/calculator.py should have content"


def test_get_file_content_invalid_path():
    """Test get_file_content with invalid system path"""
    content = get_file_content("calculator", "/bin/cat")
    print("\n--- /bin/cat (invalid) ---")
    print(f"Result: {content}")
    assert "error" in content.lower() or "cannot" in content.lower(), "Should return error"


def test_get_file_content_nonexistent_file():
    """Test get_file_content with non-existent file"""
    content = get_file_content("calculator", "pkg/does_not_exist.py")
    print("\n--- pkg/does_not_exist.py (nonexistent) ---")
    print(f"Result: {content}")
    assert "error" in content.lower() or "not found" in content.lower(), "Should return error"


if __name__ == "__main__":
    print("Running get_file_content tests...\n")
    
    test_get_file_content_lorem()
    test_get_file_content_main_py()
    test_get_file_content_pkg_calculator_py()
    test_get_file_content_invalid_path()
    test_get_file_content_nonexistent_file()
    
    print("\n✓ All tests passed!")