from functions import get_files_info

def main():
    # Test 1: Current directory
    print('get_files_info("calculator", "."):\n')
    result = get_files_info("calculator", ".")
    print("Result for current directory:")
    if isinstance(result, dict) and "error" not in result:
        for item in result:
            print(f"  - {item['name']}: file_size={item['file_size']} bytes, is_dir={item['is_dir']}")
    else:
        print(f"  Error: {result.get('error', 'Unknown error')}")
    
    # Test 2: pkg subdirectory
    print('\nget_files_info("calculator", "pkg"):\n')
    result = get_files_info("calculator", "pkg")
    print("Result for 'pkg' directory:")
    if isinstance(result, dict) and "error" not in result:
        for item in result:
            print(f"  - {item['name']}: file_size={item['file_size']} bytes, is_dir={item['is_dir']}")
    else:
        print(f"  Error: {result.get('error', 'Unknown error')}")
    
    # Test 3: Outside permitted directory (/bin)
    print('\nget_files_info("calculator", "/bin"):\n')
    result = get_files_info("calculator", "/bin")
    print("Result for '/bin' directory:")
    if isinstance(result, dict) and "error" in result:
        print(f"  Error: {result['error']}")
    else:
        for item in result:
            print(f"  - {item['name']}: file_size={item['file_size']} bytes, is_dir={item['is_dir']}")
    
    # Test 4: Outside permitted directory (../)
    print('\nget_files_info("calculator", "../"):\n')
    result = get_files_info("calculator", "../")
    print("Result for '../' directory:")
    if isinstance(result, dict) and "error" in result:
        print(f"  Error: {result['error']}")
    else:
        for item in result:
            print(f"  - {item['name']}: file_size={item['file_size']} bytes, is_dir={item['is_dir']}")

if __name__ == "__main__":
    main()
