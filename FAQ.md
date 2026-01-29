# Frequently Asked Questions (FAQ)

## Can I Change the Test Code?

### Short Answer
**YES!** The test code is NOT hardcoded for your analysis. The tests are only used to validate that the Code-Analy tool itself works correctly.

### Detailed Explanation

**The tests in `tests/` folder are for validation only:**
- They use hardcoded Python code snippets to ensure the analyzer detects issues correctly
- They verify that the tool works as expected
- You should NOT modify these tests unless you're contributing to the project

**You CAN analyze your own code in multiple ways:**

#### 1. Using the Command-Line Script

We provide `analyze_your_code.py` for easy analysis of your own files:

```bash
# Analyze a single file
python analyze_your_code.py path/to/your/file.py

# Analyze an entire directory
python analyze_your_code.py path/to/your/project/
```

#### 2. Using the Python API

You can write your own scripts to analyze any code:

```python
from code_analy.analyzer import analyze_code

# Your own code as a string
my_code = """
def my_function(a, b, c, d, e, f, g):
    return a + b
"""

# Analyze it
issues = analyze_code(my_code)

# View results
for issue in issues:
    print(f"Line {issue['line']}: {issue['message']}")
```

#### 3. Using the MCP Server

The MCP server can analyze ANY code you send it:

```bash
# Start the server
python -m code_analy.server

# Use MCP tools to analyze your code
```

## How Do I Analyze My Own Project?

### Option 1: Directory Analysis

```python
from code_analy.multi_file import analyze_directory

# Analyze your entire project
results = analyze_directory("/path/to/your/project", recursive=True)

print(f"Total files: {results['total_files']}")
print(f"Total issues: {results['total_issues']}")
```

### Option 2: File-by-File Analysis

```python
from code_analy.analyzer import analyze_code

# Read your file
with open('your_file.py', 'r') as f:
    source_code = f.read()

# Analyze it
issues = analyze_code(source_code)

# Process results
for issue in issues:
    print(f"{issue['type']} at line {issue['line']}: {issue['message']}")
```

## Can I Customize What Issues Are Detected?

**YES!** You can configure the analyzer:

```python
from code_analy.analyzer import CodeAnalyzer

# Create analyzer with your code
analyzer = CodeAnalyzer(your_source_code)

# Run only specific checks
analyzer._check_too_many_parameters(max_params=7)  # Custom threshold
analyzer._check_long_methods(max_lines=100)  # Custom threshold

# Or use the standard analyze() for all checks
all_issues = analyzer.analyze()
```

## What Code Can I Analyze?

**ANY Python code!** The tool is completely flexible:

- ✅ Your own Python files
- ✅ Any Python project
- ✅ Code snippets from anywhere
- ✅ Generated code
- ✅ Code from textbooks, tutorials, etc.

The only limitation: it must be valid Python syntax (Python 3.10+).

## What About the AI Suggestions?

AI suggestions work with **any** code you analyze:

```python
from code_analy.analyzer import analyze_code
from code_analy.ai_analyzer import AIAnalyzer

# Analyze your code
issues = analyze_code(your_code)

# Get AI suggestions for YOUR code
ai = AIAnalyzer(provider="mock")  # or "openai" or "anthropic"
suggestions = ai.suggest_refactorings(your_code, issues)

for s in suggestions:
    print(f"{s.title}: {s.reasoning}")
```

## Can I Modify the Detection Rules?

**YES!** The code is open source and modular:

1. **Fork the repository**
2. **Modify `src/code_analy/analyzer.py`** to add/modify detection rules
3. **Add your own checks** by adding methods to `CodeAnalyzer` class
4. **Adjust thresholds** (e.g., max parameters, max method length)

Example of adding a custom check:

```python
class CodeAnalyzer:
    def _check_custom_rule(self):
        """Your custom detection logic."""
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                # Your logic here
                pass
    
    def analyze(self):
        """Add your check to the analysis."""
        self.issues = []
        self._check_too_many_parameters()
        self._check_unused_imports()
        self._check_dead_code()
        self._check_long_methods()
        self._check_deep_nesting()
        self._check_duplicate_code()
        self._check_custom_rule()  # Your custom check!
        return self.issues
```

## Summary

| Question | Answer |
|----------|--------|
| Are tests hardcoded? | Yes, but only for validation |
| Can I analyze my own code? | **YES!** |
| Can I customize detection? | **YES!** |
| Can I modify thresholds? | **YES!** |
| Do I need to edit test files? | **NO** - create your own scripts |
| What code can I analyze? | **ANY** Python code |

## Examples

### Analyze Your Django Project

```python
from code_analy.multi_file import analyze_directory

results = analyze_directory("/path/to/django/project", recursive=True)
print(f"Found {results['total_issues']} issues in your Django project")
```

### Analyze Code from a String

```python
from code_analy.analyzer import analyze_code

code_to_check = """
import unused_module

def problematic_function(a, b, c, d, e, f, g, h):
    if True:
        if True:
            if True:
                if True:
                    return a
    return None
"""

issues = analyze_code(code_to_check)
print(f"Found {len(issues)} issues")
```

### Create Your Own Analysis Script

```python
#!/usr/bin/env python3
"""My custom code analyzer."""

import sys
from code_analy.analyzer import analyze_code

def analyze_my_files(filenames):
    for filename in filenames:
        with open(filename) as f:
            code = f.read()
        
        issues = analyze_code(code)
        
        if issues:
            print(f"\n{filename}:")
            for issue in issues:
                print(f"  {issue['line']}: {issue['message']}")

if __name__ == "__main__":
    analyze_my_files(sys.argv[1:])
```

## Need More Help?

- Check the [README.md](README.md) for more examples
- Run `python demo_all_features.py` to see the tool in action
- Use `python analyze_your_code.py <your_file>` for quick analysis
- Read the source code in `src/code_analy/` - it's well documented!

**Remember: The tests validate the tool. YOU choose what code to analyze!**
