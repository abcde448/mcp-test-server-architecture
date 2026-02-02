#!/usr/bin/env python3
"""
Simple script to run tests for the MCP server
Usage: python run_tests.py
"""

import subprocess
import sys
import os

def run_tests():
    """Run pytest with appropriate settings"""
    try:
        print("Running MCP Server Tests...")
        print("=" * 50)
        
        # Ensure we're in the project root
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        
        # Run pytest - it will use pytest.ini configuration
        result = subprocess.run([
            sys.executable, "-m", "pytest"
        ], capture_output=False)
        
        if result.returncode == 0:
            print("\n" + "=" * 50)
            print("✅ All tests passed!")
        else:
            print("\n" + "=" * 50)
            print("❌ Some tests failed!")
            
        return result.returncode
        
    except Exception as e:
        print(f"Error running tests: {e}")
        return 1

if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)