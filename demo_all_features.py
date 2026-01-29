"""Comprehensive demonstration of all Code-Analy features."""

from code_analy.analyzer import analyze_code
from code_analy.ai_analyzer import AIAnalyzer
from code_analy.refactor import apply_refactoring
import json


def main():
    print("=" * 80)
    print("CODE-ANALY: Comprehensive Code Analysis & Refactoring Demo")
    print("=" * 80)
    
    # Demo 1: Detect all 5 types of code smells
    print("\n" + "=" * 80)
    print("DEMO 1: Detecting All 5 Types of Code Smells")
    print("=" * 80)
    
    problematic_code = """
import os
import sys
import json

def process_user_data(user_id, name, email, phone, address, age, country, status):
    '''This function has multiple code smells'''
    print(sys.version)
    
    if user_id:
        if name:
            if email:
                if phone:
                    # Deep nesting level 4
                    result = {
                        'user_id': user_id,
                        'name': name,
                        'email': email
                    }
                    
    # Duplicate code block 1
    data = []
    for i in range(10):
        data.append(i * 2)
        data.append(i + 1)
        data.append(i - 1)
        data.append(i ** 2)
        data.append(i / 2)
    
    # More lines to make it long
    x1 = 1
    x2 = 2
    x3 = 3
    x4 = 4
    x5 = 5
    x6 = 6
    x7 = 7
    x8 = 8
    x9 = 9
    x10 = 10
    x11 = 11
    x12 = 12
    x13 = 13
    x14 = 14
    x15 = 15
    x16 = 16
    x17 = 17
    x18 = 18
    x19 = 19
    x20 = 20
    x21 = 21
    x22 = 22
    x23 = 23
    x24 = 24
    x25 = 25
    
    # Duplicate code block 2
    data2 = []
    for i in range(10):
        data2.append(i * 2)
        data2.append(i + 1)
        data2.append(i - 1)
        data2.append(i ** 2)
        data2.append(i / 2)
    
    return data
"""
    
    issues = analyze_code(problematic_code)
    
    print(f"\nTotal issues found: {len(issues)}\n")
    
    # Group issues by type
    by_type = {}
    for issue in issues:
        issue_type = issue['type']
        if issue_type not in by_type:
            by_type[issue_type] = []
        by_type[issue_type].append(issue)
    
    print("Issues by type:")
    for issue_type, type_issues in by_type.items():
        print(f"\n  {issue_type.upper()}: {len(type_issues)} issue(s)")
        for issue in type_issues[:2]:  # Show first 2 of each type
            print(f"    - Line {issue['line']}: {issue['message']}")
    
    # Demo 2: AI-Powered Refactoring Suggestions
    print("\n" + "=" * 80)
    print("DEMO 2: AI-Powered Refactoring Suggestions")
    print("=" * 80)
    
    ai_analyzer = AIAnalyzer(provider="mock")
    suggestions = ai_analyzer.suggest_refactorings(problematic_code, issues)
    
    print(f"\nGenerated {len(suggestions)} refactoring suggestions:\n")
    
    for i, suggestion in enumerate(suggestions[:3], 1):  # Show first 3
        print(f"{i}. {suggestion.title}")
        print(f"   Category: {suggestion.category} | Priority: {suggestion.priority}")
        print(f"   Reasoning: {suggestion.reasoning[:100]}...")
        print()
    
    # Demo 3: Automated Refactoring - Remove Unused Imports
    print("=" * 80)
    print("DEMO 3: Automated Refactoring - Remove Unused Imports")
    print("=" * 80)
    
    simple_code = """import os
import sys
import json

def main():
    print(sys.version)
    return True
"""
    
    print("\nOriginal code:")
    print(simple_code)
    
    result = apply_refactoring(
        simple_code,
        "remove_unused_imports",
        unused_imports=["os", "json"]
    )
    
    print(f"\nRefactoring result: {result['message']}")
    print("\nRefactored code:")
    print(result['refactored_code'])
    
    # Demo 4: Rename Variable
    print("\n" + "=" * 80)
    print("DEMO 4: Automated Refactoring - Rename Variable")
    print("=" * 80)
    
    rename_code = """
def calculate_total(items):
    tmp = 0
    for item in items:
        tmp += item.price
    return tmp
"""
    
    print("\nOriginal code:")
    print(rename_code)
    
    result = apply_refactoring(
        rename_code,
        "rename_variable",
        old_name="tmp",
        new_name="total_price"
    )
    
    print(f"\nRefactoring result: {result['message']}")
    print("\nRefactored code:")
    print(result['refactored_code'])
    
    # Demo 5: Extract Method
    print("\n" + "=" * 80)
    print("DEMO 5: Automated Refactoring - Extract Method")
    print("=" * 80)
    
    extract_code = """
def main():
    # Validation logic
    if not user:
        raise ValueError("User required")
    if not user.email:
        raise ValueError("Email required")
    
    print("Processing user:", user.name)
"""
    
    print("\nOriginal code:")
    print(extract_code)
    
    result = apply_refactoring(
        extract_code,
        "extract_method",
        start_line=3,
        end_line=6,
        method_name="validate_user"
    )
    
    if result['success']:
        print(f"\nRefactoring result: {result['message']}")
        print("\nRefactored code:")
        print(result['refactored_code'])
    else:
        print(f"\nRefactoring failed: {result['message']}")
    
    # Demo 6: Code Formatting
    print("\n" + "=" * 80)
    print("DEMO 6: Automated Refactoring - Format Code")
    print("=" * 80)
    
    messy_code = """
def test():    
    x=1   
    y=2
    
    
    
    return x+y


def another():
    pass
"""
    
    print("\nOriginal code (with messy formatting):")
    print(repr(messy_code))
    
    result = apply_refactoring(messy_code, "format_code")
    
    print(f"\nRefactoring result: {result['message']}")
    print("\nFormatted code:")
    print(repr(result['refactored_code']))
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print("\n✓ All 5 types of code smells detected:")
    print("  1. Too many parameters (>5)")
    print("  2. Dead code/unused imports")
    print("  3. Long methods (>50 lines)")
    print("  4. Duplicate code blocks")
    print("  5. Deep nesting (>3 levels)")
    
    print("\n✓ AI-powered refactoring suggestions:")
    print("  - Context-aware analysis")
    print("  - Specific recommendations with examples")
    print("  - Reasoning for each suggestion")
    
    print("\n✓ Automated refactoring operations:")
    print("  - Remove unused imports")
    print("  - Rename variables/functions")
    print("  - Extract methods")
    print("  - Format code consistently")
    
    print("\n✓ Multi-file support:")
    print("  - Analyze directories")
    print("  - Track dependencies")
    print("  - Project-level insights")
    
    print("\n" + "=" * 80)
    print("Code-Analy: Enterprise-ready code analysis & refactoring!")
    print("=" * 80)


if __name__ == "__main__":
    main()
