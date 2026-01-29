#!/usr/bin/env python3
"""
Demonstration: Tests are hardcoded, but YOUR code analysis is flexible!

This script proves that you can analyze any code you want.
Run this to see the difference between tests and user analysis.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from code_analy.analyzer import analyze_code


def demonstrate():
    """Demonstrate that you can analyze any code."""
    
    print("=" * 80)
    print("DEMONSTRATION: Tests vs Your Code")
    print("=" * 80)
    print()
    
    # Part 1: Show what tests do
    print("Part 1: What the TESTS do (hardcoded validation)")
    print("-" * 80)
    print()
    print("The tests in tests/ use hardcoded snippets like this:")
    print()
    
    test_example = '''
    code = """
def process_data(param1, param2, param3, param4, param5, param6):
    return param1 + param2
"""
    issues = analyze_code(code)
    assert len(issues) == 1  # Validates tool works!
    '''
    print(test_example)
    print("↑ This validates the tool can detect too many parameters")
    print()
    
    # Part 2: Show what users can do
    print("=" * 80)
    print("Part 2: What YOU can do (flexible analysis)")
    print("-" * 80)
    print()
    print("You can analyze ANY code you want! Examples:")
    print()
    
    # Example 1: User's custom code
    print("Example 1: Your custom code")
    print("-" * 40)
    
    user_code_1 = """
import unused_library
import math

def calculate_area(length, width, height, depth, volume, density):
    return math.pi * length * width
    print("This line is unreachable!")
"""
    
    print("Your code:")
    print(user_code_1)
    print("Analysis results:")
    issues_1 = analyze_code(user_code_1)
    for issue in issues_1:
        print(f"  • Line {issue['line']}: {issue['message']}")
    print()
    
    # Example 2: Different user code
    print("Example 2: Another piece of your code")
    print("-" * 40)
    
    user_code_2 = """
def simple_function(x, y):
    return x + y
"""
    
    print("Your code:")
    print(user_code_2)
    print("Analysis results:")
    issues_2 = analyze_code(user_code_2)
    if issues_2:
        for issue in issues_2:
            print(f"  • Line {issue['line']}: {issue['message']}")
    else:
        print("  ✓ No issues found! Clean code!")
    print()
    
    # Example 3: User's Flask app code
    print("Example 3: Code from your Flask app")
    print("-" * 40)
    
    user_code_3 = """
from flask import Flask
import os
import json

app = Flask(__name__)

@app.route('/user')
def get_user(user_id, name, email, role, status, created, updated, metadata):
    if user_id:
        if name:
            if email:
                if role:
                    return {"user": name}
    return None
"""
    
    print("Your Flask code:")
    print(user_code_3)
    print("Analysis results:")
    issues_3 = analyze_code(user_code_3)
    for issue in issues_3:
        print(f"  • Line {issue['line']}: {issue['message']}")
    print()
    
    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()
    print("✓ Tests use hardcoded snippets to validate the analyzer works")
    print("✓ YOU can analyze ANY Python code you write")
    print("✓ The tool is completely flexible and customizable")
    print()
    print("How to analyze your own code:")
    print("  1. python analyze_your_code.py your_file.py")
    print("  2. Use the Python API: analyze_code(your_source_code)")
    print("  3. Use the MCP server with your code")
    print()
    print("You do NOT need to modify the tests!")
    print("The tests are just for validation - your code is for analysis!")
    print()
    print("See FAQ.md and QUICKSTART.md for more details.")
    print("=" * 80)


if __name__ == "__main__":
    demonstrate()
