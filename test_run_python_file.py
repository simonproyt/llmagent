import sys

sys.path.insert(0, '/home/simonuwu/llmagent')

from functions.run_python_file import run_python_file


def test_run_python_file():
    """Test cases for run_python_file function"""
    
    # Test 1: Run calculator main.py without arguments
    print("Test 1: run_python_file('calculator', 'main.py')")
    result = run_python_file("calculator", "main.py")
    print(f"Result: {result}\n")
    
    # Test 2: Run calculator main.py with arguments
    print("Test 2: run_python_file('calculator', 'main.py', ['3 + 5'])")
    result = run_python_file("calculator", "main.py", ["3 + 5"])
    print(f"Result: {result}\n")
    
    # Test 3: Run calculator tests.py
    print("Test 3: run_python_file('calculator', 'tests.py')")
    result = run_python_file("calculator", "tests.py")
    print(f"Result: {result}\n")
    
    # Test 4: Try to run with path traversal (should error)
    print("Test 4: run_python_file('calculator', '../main.py')")
    result = run_python_file("calculator", "../main.py")
    print(f"Result: {result}\n")
    
    # Test 5: Try to run nonexistent file (should error)
    print("Test 5: run_python_file('calculator', 'nonexistent.py')")
    result = run_python_file("calculator", "nonexistent.py")
    print(f"Result: {result}\n")
    
    # Test 6: Try to run non-Python file (should error)
    print("Test 6: run_python_file('calculator', 'lorem.txt')")
    result = run_python_file("calculator", "lorem.txt")
    print(f"Result: {result}\n")

if __name__ == "__main__":
    test_run_python_file()