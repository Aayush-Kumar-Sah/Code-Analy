"""Quick test of MCP server functionality."""

import json
from code_analy.analyzer import analyze_code
from code_analy.ai_analyzer import AIAnalyzer
from code_analy.refactor import apply_refactoring
from code_analy.multi_file import analyze_directory
import tempfile
import os


def test_basic_analysis():
    """Test basic code analysis."""
    print("Testing basic code analysis...")
    code = """
import os
def func(a, b, c, d, e, f):
    return a + b
"""
    issues = analyze_code(code)
    assert len(issues) > 0
    print(f"✓ Found {len(issues)} issues")
    print()


def test_all_code_smells():
    """Test all 5 types of code smells."""
    print("Testing all 5 code smells...")
    
    # Long method
    long_code = "def long():\n" + "\n".join([f"    x{i} = {i}" for i in range(55)])
    issues = analyze_code(long_code)
    assert any(i['type'] == 'long_method' for i in issues)
    print("✓ Long method detection works")
    
    # Deep nesting
    deep_code = """
def deep():
    if True:
        if True:
            if True:
                if True:
                    pass
"""
    issues = analyze_code(deep_code)
    assert any(i['type'] == 'deep_nesting' for i in issues)
    print("✓ Deep nesting detection works")
    
    # Too many params
    param_code = "def func(a, b, c, d, e, f, g): pass"
    issues = analyze_code(param_code)
    assert any(i['type'] == 'too_many_parameters' for i in issues)
    print("✓ Too many parameters detection works")
    
    # Unused imports
    import_code = "import os\nprint('hello')"
    issues = analyze_code(import_code)
    assert any(i['type'] == 'unused_import' for i in issues)
    print("✓ Unused import detection works")
    
    # Dead code
    dead_code = """
def test():
    return 1
    print("unreachable")
"""
    issues = analyze_code(dead_code)
    assert any(i['type'] == 'dead_code' for i in issues)
    print("✓ Dead code detection works")
    print()


def test_ai_suggestions():
    """Test AI-powered suggestions."""
    print("Testing AI suggestions...")
    code = "def func(a, b, c, d, e, f): pass"
    issues = analyze_code(code)
    
    ai = AIAnalyzer(provider="mock")
    suggestions = ai.suggest_refactorings(code, issues)
    
    assert len(suggestions) > 0
    assert all(hasattr(s, 'title') for s in suggestions)
    assert all(hasattr(s, 'reasoning') for s in suggestions)
    print(f"✓ Generated {len(suggestions)} AI suggestions")
    print()


def test_refactoring():
    """Test automated refactoring."""
    print("Testing automated refactoring...")
    
    # Remove unused imports
    code = "import os\nprint('hi')"
    result = apply_refactoring(code, "remove_unused_imports", unused_imports=["os"])
    assert result['success']
    assert "os" not in result['refactored_code']
    print("✓ Remove unused imports works")
    
    # Rename variable
    code = "x = 1\ny = x + 1"
    result = apply_refactoring(code, "rename_variable", old_name="x", new_name="value")
    assert result['success']
    assert "value" in result['refactored_code']
    print("✓ Rename variable works")
    
    # Format code
    code = "def test():  \n    x=1  \n    return x"
    result = apply_refactoring(code, "format_code")
    assert result['success']
    print("✓ Format code works")
    print()


def test_multi_file():
    """Test multi-file analysis."""
    print("Testing multi-file analysis...")
    
    # Create temporary directory with Python files
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test files
        file1 = os.path.join(tmpdir, "file1.py")
        with open(file1, 'w') as f:
            f.write("import os\ndef func1(): pass")
        
        file2 = os.path.join(tmpdir, "file2.py")
        with open(file2, 'w') as f:
            f.write("def func2(a, b, c, d, e, f): pass")
        
        # Analyze directory
        result = analyze_directory(tmpdir, recursive=False)
        
        assert result['total_files'] == 2
        assert result['total_issues'] > 0
        print(f"✓ Analyzed {result['total_files']} files with {result['total_issues']} issues")
    print()


def main():
    """Run all tests."""
    print("=" * 60)
    print("QUICK TEST: Code-Analy MCP Server Functionality")
    print("=" * 60)
    print()
    
    test_basic_analysis()
    test_all_code_smells()
    test_ai_suggestions()
    test_refactoring()
    test_multi_file()
    
    print("=" * 60)
    print("ALL TESTS PASSED ✓")
    print("=" * 60)
    print()
    print("MCP Server is ready to use!")
    print("Run: python -m code_analy.server")


if __name__ == "__main__":
    main()
