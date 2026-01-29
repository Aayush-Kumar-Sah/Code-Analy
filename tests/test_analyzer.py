"""Comprehensive test suite for code analysis functionality."""

import pytest
from code_analy.analyzer import CodeAnalyzer, analyze_code, CodeIssue


class TestTooManyParameters:
    """Test cases for detecting functions with too many parameters."""
    
    def test_function_with_six_parameters(self):
        """Test case 1: Function with 6 parameters should be flagged."""
        code = """
def process_data(param1, param2, param3, param4, param5, param6):
    return param1 + param2
"""
        issues = analyze_code(code)
        param_issues = [i for i in issues if i["type"] == "too_many_parameters"]
        assert len(param_issues) == 1
        assert "6 parameters" in param_issues[0]["message"]
    
    def test_function_with_five_parameters(self):
        """Test case 2: Function with exactly 5 parameters should not be flagged."""
        code = """
def process_data(param1, param2, param3, param4, param5):
    return param1 + param2
"""
        issues = analyze_code(code)
        param_issues = [i for i in issues if i["type"] == "too_many_parameters"]
        assert len(param_issues) == 0
    
    def test_method_with_self_excluded(self):
        """Test case 3: 'self' parameter should not be counted."""
        code = """
class MyClass:
    def method(self, p1, p2, p3, p4, p5, p6):
        return p1 + p2
"""
        issues = analyze_code(code)
        param_issues = [i for i in issues if i["type"] == "too_many_parameters"]
        assert len(param_issues) == 1
        assert "6 parameters" in param_issues[0]["message"]
    
    def test_classmethod_with_cls_excluded(self):
        """Test case 4: 'cls' parameter should not be counted."""
        code = """
class MyClass:
    @classmethod
    def method(cls, p1, p2, p3, p4, p5, p6):
        return p1 + p2
"""
        issues = analyze_code(code)
        param_issues = [i for i in issues if i["type"] == "too_many_parameters"]
        assert len(param_issues) == 1
        assert "6 parameters" in param_issues[0]["message"]


class TestUnusedImports:
    """Test cases for detecting unused imports."""
    
    def test_unused_single_import(self):
        """Test case 5: Detect single unused import."""
        code = """
import os
import sys

print(sys.version)
"""
        issues = analyze_code(code)
        import_issues = [i for i in issues if i["type"] == "unused_import"]
        assert len(import_issues) == 1
        assert "os" in import_issues[0]["message"]
    
    def test_unused_from_import(self):
        """Test case 6: Detect unused 'from' import."""
        code = """
from os import path, getcwd

print(path.exists('/tmp'))
"""
        issues = analyze_code(code)
        import_issues = [i for i in issues if i["type"] == "unused_import"]
        assert len(import_issues) == 1
        assert "getcwd" in import_issues[0]["message"]
    
    def test_all_imports_used(self):
        """Test case 7: No issues when all imports are used."""
        code = """
import os
import sys

print(os.path.exists('/tmp'))
print(sys.version)
"""
        issues = analyze_code(code)
        import_issues = [i for i in issues if i["type"] == "unused_import"]
        assert len(import_issues) == 0
    
    def test_import_alias_used(self):
        """Test case 8: Import with alias that is used should not be flagged."""
        code = """
import numpy as np

arr = np.array([1, 2, 3])
"""
        issues = analyze_code(code)
        import_issues = [i for i in issues if i["type"] == "unused_import"]
        assert len(import_issues) == 0


class TestDeadCode:
    """Test cases for detecting dead/unreachable code."""
    
    def test_code_after_return(self):
        """Test case 9: Detect code after return statement."""
        code = """
def calculate(x):
    return x * 2
    print("This will never execute")
"""
        issues = analyze_code(code)
        dead_code_issues = [i for i in issues if i["type"] == "dead_code"]
        assert len(dead_code_issues) == 1
        assert "return" in dead_code_issues[0]["message"].lower()
    
    def test_code_after_raise(self):
        """Test case 10: Detect code after raise statement."""
        code = """
def validate(value):
    if value < 0:
        raise ValueError("Negative value")
        print("This is unreachable")
"""
        issues = analyze_code(code)
        dead_code_issues = [i for i in issues if i["type"] == "dead_code"]
        assert len(dead_code_issues) == 1
    
    def test_no_dead_code(self):
        """Test case 11: No dead code in clean function."""
        code = """
def calculate(x):
    result = x * 2
    return result
"""
        issues = analyze_code(code)
        dead_code_issues = [i for i in issues if i["type"] == "dead_code"]
        assert len(dead_code_issues) == 0


class TestMultipleIssues:
    """Test cases for detecting multiple issues in the same code."""
    
    def test_multiple_issue_types(self):
        """Test case 12: Detect multiple types of issues in one code block."""
        code = """
import os
import sys

def complex_function(a, b, c, d, e, f, g):
    print(sys.version)
    return a + b
    print("Dead code")
"""
        issues = analyze_code(code)
        
        # Should have: 1 unused import, 1 too many params, 1 dead code
        assert len(issues) >= 3
        
        issue_types = {issue["type"] for issue in issues}
        assert "unused_import" in issue_types
        assert "too_many_parameters" in issue_types
        assert "dead_code" in issue_types


class TestEdgeCases:
    """Test cases for edge cases and error handling."""
    
    def test_invalid_syntax(self):
        """Test case 13: Handle invalid Python syntax."""
        code = "def invalid syntax here"
        
        with pytest.raises(ValueError) as exc_info:
            analyze_code(code)
        
        assert "Invalid Python syntax" in str(exc_info.value)
    
    def test_empty_code(self):
        """Test case 14: Handle empty source code."""
        code = ""
        issues = analyze_code(code)
        assert issues == []
    
    def test_async_function_parameters(self):
        """Test case 15: Check async functions for too many parameters."""
        code = """
async def fetch_data(url, headers, timeout, retries, cache, validate):
    return await get(url)
"""
        issues = analyze_code(code)
        param_issues = [i for i in issues if i["type"] == "too_many_parameters"]
        assert len(param_issues) == 1


class TestCodeAnalyzerClass:
    """Test cases for the CodeAnalyzer class directly."""
    
    def test_analyzer_initialization(self):
        """Test case 16: Test CodeAnalyzer initialization."""
        code = "x = 1"
        analyzer = CodeAnalyzer(code)
        assert analyzer.source_code == code
        assert analyzer.tree is not None
    
    def test_analyzer_returns_code_issues(self):
        """Test case 17: Test that analyzer returns CodeIssue objects."""
        code = """
def too_many_params(a, b, c, d, e, f):
    pass
"""
        analyzer = CodeAnalyzer(code)
        issues = analyzer.analyze()
        
        assert len(issues) > 0
        assert all(isinstance(issue, CodeIssue) for issue in issues)
        assert issues[0].line > 0
        assert issues[0].issue_type == "too_many_parameters"
