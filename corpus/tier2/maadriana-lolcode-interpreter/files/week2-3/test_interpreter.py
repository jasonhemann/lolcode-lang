"""
Simple test script for the LOLCODE interpreter (Week 2)
Looks for .lol test files in the ./test/ directory
"""

import os
import sys
import subprocess

def run_test(test_file):
    """Run a test file through the interpreter"""
    print(f"Testing {test_file}...")
    print("-" * 40)
    
    try:
        result = subprocess.run(
            [sys.executable, "main.py", test_file], 
            capture_output=True, 
            text=True
        )
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("\nSTDERR:")
            print(result.stderr)
        
        if result.returncode != 0:
            print(f"\nTest failed with return code {result.returncode}")
        else:
            print("\nTest completed successfully!")
        
    except Exception as e:
        print(f"Error running test: {e}")
    
    print("-" * 40)
    print()

def main():
    """Run all test files in ./test/"""
    test_dir = 'test'
    
    if not os.path.exists(test_dir):
        print("❌ 'test/' directory not found.")
        return

    test_files = [os.path.join(test_dir, f) for f in os.listdir(test_dir) if f.endswith('.lol')]
    
    if not test_files:
        print("No .lol test files found in the 'test/' directory.")
        return
    
    print(f"Found {len(test_files)} test file(s).")
    
    for test_file in test_files:
        run_test(test_file)

if __name__ == "__main__":
    main()
