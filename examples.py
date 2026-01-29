"""Example demonstrating the code analysis functionality."""

from code_analy.analyzer import analyze_code


def main():
    """Run example code analysis."""
    
    # Example 1: Too many parameters
    print("=" * 60)
    print("Example 1: Function with too many parameters")
    print("=" * 60)
    
    code1 = """
def process_user_data(user_id, name, email, phone, address, age, country):
    return f"{name} from {country}"
"""
    
    issues1 = analyze_code(code1)
    print(f"Code:\n{code1}")
    print(f"\nIssues found: {len(issues1)}")
    for issue in issues1:
        print(f"  - Line {issue['line']}: {issue['message']} [{issue['severity']}]")
    
    # Example 2: Unused imports
    print("\n" + "=" * 60)
    print("Example 2: Unused imports")
    print("=" * 60)
    
    code2 = """
import os
import sys
import json
from typing import List, Dict

def get_version():
    return sys.version
"""
    
    issues2 = analyze_code(code2)
    print(f"Code:\n{code2}")
    print(f"\nIssues found: {len(issues2)}")
    for issue in issues2:
        print(f"  - Line {issue['line']}: {issue['message']} [{issue['severity']}]")
    
    # Example 3: Dead code
    print("\n" + "=" * 60)
    print("Example 3: Dead/unreachable code")
    print("=" * 60)
    
    code3 = """
def calculate_price(amount, discount):
    if discount > 100:
        raise ValueError("Invalid discount")
        print("This will never execute")
    
    final_price = amount * (1 - discount / 100)
    return final_price
    print("This is also unreachable")
"""
    
    issues3 = analyze_code(code3)
    print(f"Code:\n{code3}")
    print(f"\nIssues found: {len(issues3)}")
    for issue in issues3:
        print(f"  - Line {issue['line']}: {issue['message']} [{issue['severity']}]")
    
    # Example 4: Multiple issues
    print("\n" + "=" * 60)
    print("Example 4: Code with multiple issues")
    print("=" * 60)
    
    code4 = """
import os
import sys
import json

def complex_function(a, b, c, d, e, f, g, h):
    print(sys.version)
    result = a + b + c
    return result
    print("Dead code here")
"""
    
    issues4 = analyze_code(code4)
    print(f"Code:\n{code4}")
    print(f"\nIssues found: {len(issues4)}")
    for issue in issues4:
        print(f"  - Line {issue['line']}, Col {issue['column']}: {issue['type']} - {issue['message']} [{issue['severity']}]")
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total examples analyzed: 4")
    print(f"Total issues found: {len(issues1) + len(issues2) + len(issues3) + len(issues4)}")
    print("\nCode-Analy successfully detected:")
    print("  ✓ Functions with too many parameters")
    print("  ✓ Unused imports")
    print("  ✓ Dead/unreachable code")


if __name__ == "__main__":
    main()
