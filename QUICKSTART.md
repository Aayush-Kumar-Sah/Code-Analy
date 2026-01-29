# Quick Start Guide: Analyzing Your Own Code

## TL;DR - Can I Change the Test Code?

**The tests are hardcoded, BUT you don't need to change them!**

The tests in `tests/` validate that the tool works. They are NOT the code being analyzed.

**You analyze your OWN code by:**
1. Using `python analyze_your_code.py your_file.py`
2. Using the Python API with your code
3. Using the MCP server with your code

## Getting Started in 60 Seconds

### Step 1: Test the tool works

```bash
# Run the existing tests to verify everything works
pytest tests/

# Should show: 29 tests passed
```

### Step 2: Analyze the sample file

```bash
# Analyze the provided sample
python analyze_your_code.py sample_code.py
```

You'll see it detects:
- Too many parameters
- Unused imports
- Dead code
- Deep nesting

### Step 3: Analyze YOUR own file

```bash
# Create your own Python file
cat > my_code.py << 'EOF'
import unused_module

def my_function(a, b, c, d, e, f, g):
    return a + b
    print("unreachable")
EOF

# Analyze it!
python analyze_your_code.py my_code.py
```

## Understanding the Project Structure

```
Code-Analy/
├── tests/                      # Hardcoded tests (for validation)
│   ├── test_analyzer.py       # DON'T modify (unless contributing)
│   └── test_new_features.py   # DON'T modify (unless contributing)
│
├── src/code_analy/            # The actual analyzer code
│   ├── analyzer.py            # CAN customize thresholds here
│   ├── ai_analyzer.py         # Works with ANY code you provide
│   ├── refactor.py            # Works with ANY code you provide
│   └── ...
│
├── analyze_your_code.py       # USE THIS for your files! ⭐
├── sample_code.py             # Example to analyze ⭐
├── config.py                  # Customize settings ⭐
├── FAQ.md                     # Detailed Q&A ⭐
└── README.md                  # Full documentation
```

## Common Workflows

### Workflow 1: Analyze a Single File

```bash
python analyze_your_code.py /path/to/your/script.py
```

### Workflow 2: Analyze a Directory

```bash
python analyze_your_code.py /path/to/your/project/
```

### Workflow 3: Use Python API

```python
from code_analy.analyzer import analyze_code

# Your code
code = """
def problematic(a, b, c, d, e, f):
    pass
"""

# Analyze it
issues = analyze_code(code)

# See results
for issue in issues:
    print(issue)
```

### Workflow 4: Integrate into CI/CD

```bash
# Add to your CI pipeline
python analyze_your_code.py src/ > code_analysis_report.txt

# Or use in a pre-commit hook
git diff --name-only --cached | grep '\.py$' | while read file; do
    python analyze_your_code.py "$file"
done
```

### Workflow 5: Custom Thresholds

```python
from code_analy.analyzer import CodeAnalyzer

code = "your code here"
analyzer = CodeAnalyzer(code)

# Use custom thresholds!
analyzer._check_too_many_parameters(max_params=7)  # More permissive
analyzer._check_long_methods(max_lines=100)        # Longer methods OK

issues = analyzer.issues
```

## Real-World Examples

### Example 1: Django Project

```bash
python analyze_your_code.py /path/to/django/project/
```

### Example 2: Flask App

```bash
python analyze_your_code.py /path/to/flask/app/
```

### Example 3: Data Science Notebooks (converted)

```bash
# Convert notebook to .py first
jupyter nbconvert --to python notebook.ipynb

# Analyze it
python analyze_your_code.py notebook.py
```

### Example 4: Legacy Codebase

```python
from code_analy.multi_file import analyze_directory

# Analyze legacy code
results = analyze_directory("/path/to/legacy/code", recursive=True)

# Generate report
print(f"Files: {results['total_files']}")
print(f"Total Issues: {results['total_issues']}")

# Find worst offenders
for file, data in sorted(results['files'].items(), 
                         key=lambda x: len(x[1]['issues']), 
                         reverse=True)[:10]:
    print(f"{file}: {len(data['issues'])} issues")
```

## Customizing Detection

### Method 1: Edit config.py

```python
# Edit config.py to change thresholds
MAX_PARAMETERS = 7  # More permissive
MAX_METHOD_LINES = 100
```

### Method 2: Programmatic

```python
from code_analy.analyzer import CodeAnalyzer
import ast

class MyCustomAnalyzer(CodeAnalyzer):
    def _check_too_many_parameters(self):
        # Override with your own logic
        max_params = 10  # Your threshold
        super()._check_too_many_parameters(max_params=max_params)

# Use it
analyzer = MyCustomAnalyzer(your_code)
issues = analyzer.analyze()
```

## Advanced: Adding Custom Rules

```python
from code_analy.analyzer import CodeAnalyzer, CodeIssue
import ast

class CustomAnalyzer(CodeAnalyzer):
    def _check_naming_conventions(self):
        """Custom check: Function names should be snake_case."""
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                name = node.name
                if not name.islower() or '-' in name:
                    self.issues.append(CodeIssue(
                        line=node.lineno,
                        column=node.col_offset,
                        issue_type="naming_convention",
                        message=f"Function '{name}' should use snake_case",
                        severity="info"
                    ))
    
    def analyze(self):
        # Call parent's analyze
        super().analyze()
        # Add your custom check
        self._check_naming_conventions()
        return self.issues

# Use your custom analyzer
analyzer = CustomAnalyzer(your_code)
issues = analyzer.analyze()
```

## Integration Examples

### Pre-commit Hook

```bash
# .git/hooks/pre-commit
#!/bin/bash
python analyze_your_code.py $(git diff --cached --name-only --diff-filter=ACM | grep '\.py$')
```

### GitHub Actions

```yaml
# .github/workflows/code-analysis.yml
name: Code Analysis
on: [push, pull_request]
jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
      - name: Install dependencies
        run: pip install -e .
      - name: Analyze code
        run: python analyze_your_code.py src/
```

### VS Code Task

```json
// .vscode/tasks.json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Analyze Current File",
            "type": "shell",
            "command": "python analyze_your_code.py ${file}",
            "problemMatcher": []
        }
    ]
}
```

## FAQ Quick Reference

| Question | Answer |
|----------|--------|
| Can I analyze my own code? | **YES!** Use `analyze_your_code.py` |
| Are the tests limiting? | **NO!** Tests only validate the tool |
| Can I customize thresholds? | **YES!** Edit `config.py` or use API |
| Do I modify test files? | **NO!** Create your own scripts instead |
| What code can I analyze? | **ANY** Python code (3.10+) |
| Can I add custom rules? | **YES!** Extend the `CodeAnalyzer` class |

## Getting Help

1. Read the [FAQ.md](FAQ.md) - Comprehensive Q&A
2. Check [README.md](README.md) - Full documentation
3. Run `python demo_all_features.py` - See tool in action
4. Look at `examples.py` - More examples
5. Read the source code - It's well documented!

## Key Takeaway

**The tests are hardcoded to validate the tool works correctly.**

**YOU choose what code to analyze - it can be anything!**

Think of it like a calculator:
- The tests verify 2+2=4 works correctly
- But YOU decide what numbers to calculate!

Code-Analy tests verify it can detect issues correctly.
But YOU decide what code to analyze!
