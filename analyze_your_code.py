#!/usr/bin/env python3
"""
Script to analyze your own Python code with Code-Analy.

This demonstrates that you can analyze ANY Python code, not just the hardcoded tests.
The tests are only used to validate the tool itself works correctly.

Usage:
    python analyze_your_code.py <path_to_your_file.py>
    python analyze_your_code.py <path_to_directory>
"""

import sys
import os
from pathlib import Path

# Add src to path so we can import code_analy
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from code_analy.analyzer import analyze_code
from code_analy.ai_analyzer import AIAnalyzer
from code_analy.multi_file import analyze_directory


def analyze_file(filepath: str):
    """Analyze a single Python file."""
    print(f"\n{'='*80}")
    print(f"Analyzing: {filepath}")
    print('='*80)
    
    try:
        with open(filepath, 'r') as f:
            source_code = f.read()
        
        # Run analysis
        issues = analyze_code(source_code)
        
        if not issues:
            print("✓ No issues found! Your code looks clean.")
        else:
            print(f"\n{len(issues)} issue(s) found:\n")
            
            # Group by type
            by_type = {}
            for issue in issues:
                issue_type = issue.get('type', 'unknown')
                if issue_type not in by_type:
                    by_type[issue_type] = []
                by_type[issue_type].append(issue)
            
            # Display grouped results
            for issue_type, type_issues in by_type.items():
                print(f"\n{issue_type.upper().replace('_', ' ')}:")
                for issue in type_issues:
                    print(f"  Line {issue['line']}: {issue['message']}")
        
        # Optional: Get AI-powered suggestions (requires API key or use mock)
        print(f"\n{'='*80}")
        print("AI-Powered Refactoring Suggestions")
        print('='*80)
        
        if issues:
            print("\nGenerating suggestions (using mock mode)...")
            ai = AIAnalyzer(provider="mock")
            suggestions = ai.suggest_refactorings(source_code, issues)
            
            if suggestions:
                print(f"\nFound {len(suggestions)} suggestion(s):\n")
                for i, suggestion in enumerate(suggestions, 1):
                    print(f"{i}. {suggestion.title}")
                    print(f"   Category: {suggestion.category}")
                    print(f"   Priority: {suggestion.priority}")
                    print(f"   Reasoning: {suggestion.reasoning}")
                    print()
            else:
                print("No AI suggestions available.")
        
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
    except Exception as e:
        print(f"Error analyzing file: {e}")


def analyze_dir(dirpath: str):
    """Analyze all Python files in a directory."""
    print(f"\n{'='*80}")
    print(f"Analyzing directory: {dirpath}")
    print('='*80)
    
    try:
        results = analyze_directory(dirpath, recursive=True)
        
        print(f"\nAnalysis Summary:")
        print(f"  Total files: {results['total_files']}")
        print(f"  Total issues: {results['total_issues']}")
        print(f"  Total lines of code: {results['total_lines']}")
        
        if results.get('files'):
            print(f"\nFiles with most issues:")
            # Sort files by issue count
            sorted_files = sorted(
                results['files'].items(),
                key=lambda x: len(x[1].get('issues', [])),
                reverse=True
            )
            
            for filepath, file_data in sorted_files[:5]:  # Top 5
                issue_count = len(file_data.get('issues', []))
                if issue_count > 0:
                    print(f"  {filepath}: {issue_count} issues")
        
        if results.get('summary'):
            print(f"\nIssue breakdown:")
            for issue_type, count in results['summary'].items():
                print(f"  {issue_type}: {count}")
        
    except Exception as e:
        print(f"Error analyzing directory: {e}")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nExamples:")
        print("  python analyze_your_code.py myproject/main.py")
        print("  python analyze_your_code.py myproject/")
        print("\nYou can analyze ANY Python code - the tests are just for validation!")
        sys.exit(1)
    
    target = sys.argv[1]
    
    if not os.path.exists(target):
        print(f"Error: '{target}' does not exist.")
        sys.exit(1)
    
    if os.path.isfile(target):
        analyze_file(target)
    elif os.path.isdir(target):
        analyze_dir(target)
    else:
        print(f"Error: '{target}' is neither a file nor a directory.")
        sys.exit(1)
    
    print(f"\n{'='*80}")
    print("Analysis complete!")
    print('='*80)
    print("\nRemember: The tests in tests/ are hardcoded to validate the tool.")
    print("You can analyze ANY Python code by passing it to the analysis functions!")
    print("\nFor more control, you can use the Python API directly:")
    print("  from code_analy.analyzer import analyze_code")
    print("  issues = analyze_code(your_source_code)")


if __name__ == "__main__":
    main()
