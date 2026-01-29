# Code-Analy

Intelligent Code Analysis & Refactoring MCP Server

## Overview

Code-Analy is an MCP (Model Context Protocol) server that enables AI agents to analyze Python codebases, detect code smells, and suggest refactorings. It uses AST (Abstract Syntax Tree) based analysis to provide intelligent code insights.

## Features

### Code Analysis Tools

1. **Too Many Parameters Detection**
   - Identifies functions with more than 5 parameters (excluding `self`/`cls`)
   - Helps maintain code readability and reduce complexity

2. **Unused Imports Detection**
   - Finds imports that are declared but never used
   - Helps keep code clean and reduce dependencies

3. **Dead Code Detection**
   - Identifies unreachable code after return, raise, break, or continue statements
   - Improves code quality and maintainability

## Installation

```bash
# Install dependencies
pip install -e .

# Install development dependencies
pip install -e ".[dev]"
```

## Usage

### Running the MCP Server

```bash
python -m code_analy.server
```

### Available Tools

The server exposes the following tools through the MCP protocol:

1. **analyze_code** - Comprehensive analysis detecting all types of issues
2. **check_function_parameters** - Check for functions with too many parameters
3. **check_unused_imports** - Detect unused imports
4. **check_dead_code** - Find unreachable code

### Example

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

## Testing

Run the comprehensive test suite:

```bash
pytest tests/
```

The test suite includes 17+ test cases covering:
- Functions with too many parameters
- Unused imports detection
- Dead code detection
- Multiple issues in the same code
- Edge cases and error handling

## Development

### Project Structure

```
Code-Analy/
├── src/
│   └── code_analy/
│       ├── __init__.py
│       ├── analyzer.py      # AST-based code analysis
│       └── server.py         # MCP server implementation
├── tests/
│   ├── __init__.py
│   └── test_analyzer.py     # Comprehensive test suite
├── pyproject.toml
└── README.md
```

## Requirements

- Python >= 3.10
- mcp >= 0.9.0

## License

This project is open source.