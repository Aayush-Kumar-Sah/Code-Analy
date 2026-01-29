# Code-Analy

Intelligent Code Analysis & Refactoring MCP Server

## 🎯 Quick Links

- **[Quick Start Guide](QUICKSTART.md)** - Get started in 60 seconds
- **[FAQ](FAQ.md)** - Can I change the test code? (Answer: You don't need to!)
- **[Configuration](config.py)** - Customize detection thresholds
- **[Sample Code](sample_code.py)** - Example to analyze

## ⚠️ Important Note

**The tests in `tests/` are hardcoded to validate the tool works correctly.**

**You can analyze ANY Python code you want!** Use:
```bash
python analyze_your_code.py your_file.py
```

See [FAQ.md](FAQ.md) for details.

## Overview

Code-Analy is a comprehensive MCP (Model Context Protocol) server that enables AI agents to analyze Python codebases, detect code smells, suggest intelligent refactorings, and apply automated code transformations. It uses AST (Abstract Syntax Tree) based analysis combined with AI-powered suggestions to provide deep code insights.

## Features

### 1. Comprehensive Code Smell Detection

Detects **6 types** of code smells:

1. **Too Many Parameters (>5)**
   - Identifies functions with more than 5 parameters (excluding `self`/`cls`)
   - Helps maintain code readability and reduce complexity

2. **Unused Imports**
   - Finds imports that are declared but never used
   - Helps keep code clean and reduce dependencies

3. **Dead Code**
   - Identifies unreachable code after return, raise, break, or continue statements
   - Improves code quality and maintainability

4. **Long Methods (>50 lines)**
   - Detects functions that are too long and difficult to maintain
   - Encourages breaking down complex logic into smaller functions

5. **Deep Nesting (>3 levels)**
   - Identifies deeply nested control structures
   - Promotes flatter, more readable code

6. **Duplicate Code Blocks**
   - Finds repeated code patterns across the codebase
   - Encourages DRY (Don't Repeat Yourself) principles

### 2. AI-Powered Refactoring Suggestions

- **LLM Integration**: Supports OpenAI GPT-4 and Anthropic Claude APIs
- **Context-Aware Analysis**: Understands code patterns and suggests appropriate refactorings
- **Detailed Recommendations**: Provides specific examples with before/after code
- **Reasoning**: Explains why each refactoring is beneficial
- **Categorization**: Groups suggestions by complexity, readability, maintainability, and cleanliness
- **Priority Levels**: Ranks suggestions by importance (high, medium, low)

### 3. Automated Refactoring Operations

Safe, automated code transformations:

- **Remove Unused Imports**: Automatically clean up import statements
- **Rename Variables/Functions**: Intelligently rename identifiers throughout the code
- **Extract Methods**: Pull out code blocks into separate, reusable functions
- **Format Code**: Apply consistent formatting rules (whitespace, blank lines, etc.)

### 4. Multi-File Support

- **Directory Analysis**: Scan entire projects recursively
- **Dependency Tracking**: Identify relationships between files
- **Project-Level Insights**: Generate comprehensive reports with statistics
- **Scalable**: Handles codebases of any size

## Installation

```bash
# Install dependencies
pip install -e .

# Install development dependencies
pip install -e ".[dev]"

# Optional: Install AI providers for advanced suggestions
pip install openai anthropic
```

## Usage

### ⚠️ Important: Analyzing Your Own Code

**The tests in the `tests/` folder are hardcoded only for validation.** You can analyze **ANY Python code** you want! The tool is completely flexible.

**Quick Start - Analyze Your Code:**

```bash
# Analyze a single file
python analyze_your_code.py path/to/your/file.py

# Analyze an entire directory
python analyze_your_code.py path/to/your/project/
```

See [FAQ.md](FAQ.md) for detailed examples and customization options.

### Running the MCP Server

```bash
python -m code_analy.server
```

### Available MCP Tools

The server exposes the following tools through the MCP protocol:

1. **analyze_code** - Comprehensive analysis detecting all types of issues
2. **detect_code_smells** - Focused code smell detection
3. **suggest_refactoring** - AI-powered refactoring suggestions (requires API key)
4. **apply_refactoring** - Apply automated code transformations
5. **analyze_directory** - Analyze entire projects
6. **check_function_parameters** - Check for functions with too many parameters
7. **check_unused_imports** - Detect unused imports
8. **check_dead_code** - Find unreachable code

### Python API Examples

#### Detect All Code Smells

```python
from code_analy.analyzer import analyze_code

source = """
import os
import sys

def process_data(a, b, c, d, e, f):
    print(sys.version)
    return a + b
    print("This won't execute")
"""

issues = analyze_code(source)
for issue in issues:
    print(f"{issue['type']} at line {issue['line']}: {issue['message']}")
```

#### Get AI-Powered Suggestions

```python
from code_analy.ai_analyzer import AIAnalyzer
from code_analy.analyzer import analyze_code

# Analyze code first
issues = analyze_code(source_code)

# Get AI suggestions (using mock mode for testing)
ai = AIAnalyzer(provider="mock")
suggestions = ai.suggest_refactorings(source_code, issues)

for s in suggestions:
    print(f"{s.title}")
    print(f"Reasoning: {s.reasoning}")
    print(f"Before: {s.code_before}")
    print(f"After: {s.code_after}")
```

#### Apply Automated Refactoring

```python
from code_analy.refactor import apply_refactoring

# Remove unused imports
result = apply_refactoring(
    source_code,
    "remove_unused_imports",
    unused_imports=["os"]
)

# Rename variable
result = apply_refactoring(
    source_code,
    "rename_variable",
    old_name="tmp",
    new_name="total"
)

# Extract method
result = apply_refactoring(
    source_code,
    "extract_method",
    start_line=5,
    end_line=10,
    method_name="helper_function"
)

# Format code
result = apply_refactoring(source_code, "format_code")

print(result['refactored_code'])
```

#### Analyze Entire Directory

```python
from code_analy.multi_file import analyze_directory

results = analyze_directory("./my_project", recursive=True)

print(f"Total files: {results['total_files']}")
print(f"Total issues: {results['total_issues']}")
print(f"Summary: {results['summary']}")
```

## Configuration

### AI Provider Setup

To use AI-powered suggestions with real LLM APIs:

```bash
# For OpenAI
export LLM_API_KEY="your-openai-api-key"

# Or for Anthropic
export LLM_API_KEY="your-anthropic-api-key"
```

Then specify the provider when creating the analyzer:

```python
# Using OpenAI
ai = AIAnalyzer(provider="openai")

# Using Anthropic
ai = AIAnalyzer(provider="anthropic")

# Using mock (for testing, no API key needed)
ai = AIAnalyzer(provider="mock")
```

## Testing

**Note:** The tests use hardcoded code snippets to validate that the analyzer works correctly. They do NOT limit what code you can analyze. You can analyze ANY Python code - see [FAQ.md](FAQ.md) for examples.

Run the comprehensive test suite:

```bash
pytest tests/
```

The test suite includes 29+ test cases covering:
- All 6 types of code smell detection
- AI-powered suggestion generation
- Automated refactoring operations
- Multi-file analysis
- Edge cases and error handling

## Analyzing Your Own Code

### Command-Line Tool

The easiest way to analyze your own code:

```bash
# Analyze a single file
python analyze_your_code.py your_script.py

# Analyze a directory
python analyze_your_code.py your_project/

# Example with a Django project
python analyze_your_code.py /path/to/django/project/
```

### Python API for Custom Code

You can analyze ANY code string or file:

```python
from code_analy.analyzer import analyze_code

# Read your file
with open('your_file.py', 'r') as f:
    your_code = f.read()

# Or define code as a string
your_code = """
def my_function(param1, param2, param3, param4, param5, param6):
    # Your code here
    pass
"""

# Analyze it!
issues = analyze_code(your_code)

# View results
for issue in issues:
    print(f"Line {issue['line']}: {issue['message']}")
```

### Analyze Entire Projects

```python
from code_analy.multi_file import analyze_directory

# Analyze your project
results = analyze_directory("/path/to/your/project", recursive=True)

print(f"Total files: {results['total_files']}")
print(f"Total issues: {results['total_issues']}")
print(f"Summary: {results['summary']}")
```

**See [FAQ.md](FAQ.md) for more examples and customization options!**

## Demo

Run the comprehensive demo to see all features in action:

```bash
python demo_all_features.py
```

## Architecture

### Project Structure

```
Code-Analy/
├── src/
│   └── code_analy/
│       ├── __init__.py          # Package initialization
│       ├── analyzer.py          # AST-based code analysis (5 code smells)
│       ├── ai_analyzer.py       # AI-powered refactoring suggestions
│       ├── refactor.py          # Automated refactoring operations
│       ├── multi_file.py        # Multi-file and directory analysis
│       └── server.py            # MCP server implementation
├── tests/
│   ├── __init__.py
│   ├── test_analyzer.py         # Tests for code smell detection
│   └── test_new_features.py    # Tests for AI and refactoring
├── pyproject.toml               # Package configuration
├── demo_all_features.py         # Comprehensive demo
└── README.md                    # This file
```

### Core Components

1. **Analyzer** (`analyzer.py`): AST-based code analysis engine
   - Detects all 6 types of code smells
   - Uses Python's `ast` module for accurate parsing
   - Provides detailed issue reports with line numbers

2. **AI Analyzer** (`ai_analyzer.py`): LLM-powered suggestions
   - Integrates with OpenAI and Anthropic APIs
   - Generates context-aware refactoring recommendations
   - Includes mock mode for testing without API keys

3. **Refactor** (`refactor.py`): Automated code transformations
   - Safe, tested refactoring operations
   - Preserves code semantics
   - Provides detailed change reports

4. **Multi-File Analyzer** (`multi_file.py`): Project-level analysis
   - Scans directories recursively
   - Tracks file dependencies
   - Generates project statistics

5. **MCP Server** (`server.py`): Protocol integration
   - Exposes 8 tools via MCP
   - Async/await architecture
   - Comprehensive error handling

## Requirements

- Python >= 3.10
- mcp >= 0.9.0
- Optional: openai, anthropic (for AI features)

## Performance

- Fast AST-based analysis
- Efficient duplicate code detection using hashing
- Scalable to large codebases
- Memory-efficient file processing

## Security

- No code execution (static analysis only)
- Safe refactoring operations
- API keys handled securely via environment variables
- Comprehensive input validation

## License

This project is open source.

## Contributing

Contributions are welcome! Please ensure all tests pass before submitting PRs.

## Support

For issues and questions, please open a GitHub issue.