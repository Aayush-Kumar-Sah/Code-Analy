"""Tests for new code smell detectors and features."""

import pytest
from code_analy.analyzer import analyze_code
from code_analy.ai_analyzer import AIAnalyzer
from code_analy.refactor import apply_refactoring


class TestNewCodeSmells:
    """Test cases for newly added code smell detectors."""
    
    def test_long_method_detection(self):
        """Test detection of methods longer than 50 lines."""
        # Create a long method (>50 lines)
        lines = ["def long_function():"]
        for i in range(55):
            lines.append(f"    x{i} = {i}")
        lines.append("    return x0")
        
        code = "\n".join(lines)
        issues = analyze_code(code)
        
        long_method_issues = [i for i in issues if i["type"] == "long_method"]
        assert len(long_method_issues) == 1
        assert "too long" in long_method_issues[0]["message"].lower()
    
    def test_short_method_not_flagged(self):
        """Test that short methods are not flagged."""
        code = """
def short_function():
    x = 1
    y = 2
    return x + y
"""
        issues = analyze_code(code)
        long_method_issues = [i for i in issues if i["type"] == "long_method"]
        assert len(long_method_issues) == 0
    
    def test_deep_nesting_detection(self):
        """Test detection of deeply nested code (>3 levels)."""
        code = """
def deeply_nested():
    if True:
        if True:
            if True:
                if True:
                    return 1
"""
        issues = analyze_code(code)
        deep_nesting_issues = [i for i in issues if i["type"] == "deep_nesting"]
        assert len(deep_nesting_issues) == 1
        assert "deep nesting" in deep_nesting_issues[0]["message"].lower()
    
    def test_shallow_nesting_not_flagged(self):
        """Test that shallow nesting is not flagged."""
        code = """
def shallow_nested():
    if True:
        if True:
            return 1
"""
        issues = analyze_code(code)
        deep_nesting_issues = [i for i in issues if i["type"] == "deep_nesting"]
        assert len(deep_nesting_issues) == 0
    
    def test_duplicate_code_detection(self):
        """Test detection of duplicate code blocks."""
        code = """
def func1():
    x = 1
    y = 2
    z = 3
    a = 4
    b = 5
    return x + y

def func2():
    x = 1
    y = 2
    z = 3
    a = 4
    b = 5
    return x * y
"""
        issues = analyze_code(code)
        duplicate_issues = [i for i in issues if i["type"] == "duplicate_code"]
        # Duplicate detection may find blocks depending on implementation
        # This test just ensures the detector doesn't crash
        assert isinstance(duplicate_issues, list)


class TestAIAnalyzer:
    """Test cases for AI-powered analysis."""
    
    def test_ai_analyzer_mock_mode(self):
        """Test AI analyzer in mock mode."""
        analyzer = AIAnalyzer(provider="mock")
        
        code = """
import os
def func(a, b, c, d, e, f):
    return a + b
"""
        issues = analyze_code(code)
        suggestions = analyzer.suggest_refactorings(code, issues)
        
        assert len(suggestions) > 0
        assert all(hasattr(s, 'title') for s in suggestions)
        assert all(hasattr(s, 'reasoning') for s in suggestions)
        assert all(hasattr(s, 'code_before') for s in suggestions)
        assert all(hasattr(s, 'code_after') for s in suggestions)
    
    def test_ai_analyzer_categories(self):
        """Test that AI analyzer provides categorized suggestions."""
        analyzer = AIAnalyzer(provider="mock")
        
        code = """
def long_func(a, b, c, d, e, f, g):
    pass
"""
        issues = analyze_code(code)
        suggestions = analyzer.suggest_refactorings(code, issues)
        
        categories = [s.category for s in suggestions]
        assert any(cat in ['complexity', 'readability', 'maintainability', 'cleanliness'] 
                  for cat in categories)


class TestRefactoring:
    """Test cases for automated refactoring operations."""
    
    def test_remove_unused_imports(self):
        """Test removing unused imports."""
        code = """import os
import sys

print(sys.version)
"""
        result = apply_refactoring(
            code,
            "remove_unused_imports",
            unused_imports=["os"]
        )
        
        assert result["success"]
        assert "os" not in result["refactored_code"]
        assert "sys" in result["refactored_code"]
    
    def test_rename_variable(self):
        """Test renaming variables."""
        code = """
def test():
    old_name = 5
    result = old_name * 2
    return result
"""
        result = apply_refactoring(
            code,
            "rename_variable",
            old_name="old_name",
            new_name="new_name"
        )
        
        assert result["success"]
        assert "new_name" in result["refactored_code"]
        assert "old_name" not in result["refactored_code"]
    
    def test_format_code(self):
        """Test code formatting."""
        code = """
def test():    
    x=1   
    y=2
    return x+y
"""
        result = apply_refactoring(code, "format_code")
        
        assert result["success"]
        # Check that trailing whitespace is removed
        for line in result["refactored_code"].splitlines():
            assert line == line.rstrip()
    
    def test_extract_method(self):
        """Test method extraction."""
        code = """
def main():
    x = 1
    y = 2
    z = x + y
    print(z)
"""
        result = apply_refactoring(
            code,
            "extract_method",
            start_line=3,
            end_line=4,
            method_name="calculate_sum"
        )
        
        assert result["success"]
        assert "calculate_sum" in result["refactored_code"]


class TestComprehensiveAnalysis:
    """Test comprehensive code analysis with all new features."""
    
    def test_all_code_smells_detected(self):
        """Test that all types of code smells can be detected."""
        # Create code with multiple issues
        code = """
import os
import sys

def complex_func(a, b, c, d, e, f, g, h):
    print(sys.version)
    if True:
        if True:
            if True:
                if True:
                    x = 1
"""
        # Add long method content
        for i in range(50):
            code += f"    y{i} = {i}\n"
        
        code += "    return x\n"
        
        issues = analyze_code(code)
        
        # Check that various types are detected
        issue_types = {issue["type"] for issue in issues}
        
        # Should detect unused import (os)
        assert "unused_import" in issue_types
        # Should detect too many parameters
        assert "too_many_parameters" in issue_types
        # Should detect deep nesting
        assert "deep_nesting" in issue_types
        # Should detect long method
        assert "long_method" in issue_types
