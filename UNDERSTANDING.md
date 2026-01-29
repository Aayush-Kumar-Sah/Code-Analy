# Understanding Tests vs Your Code Analysis

## Visual Guide

```
┌─────────────────────────────────────────────────────────────┐
│                    Code-Analy Tool                          │
│                                                             │
│  ┌───────────────┐                ┌────────────────┐       │
│  │  Tests        │                │  Your Code     │       │
│  │  (Hardcoded)  │                │  (Flexible!)   │       │
│  │               │                │                │       │
│  │  tests/       │                │  - your_file.py│       │
│  │  ├─test_*.py  │                │  - your_dir/   │       │
│  │  └─...        │                │  - sample.py   │       │
│  │               │                │  - ANY code!   │       │
│  │  Purpose:     │                │                │       │
│  │  Validate     │                │  Purpose:      │       │
│  │  tool works   │                │  Find issues   │       │
│  │               │                │  in YOUR code  │       │
│  └───────┬───────┘                └────────┬───────┘       │
│          │                                 │               │
│          ↓                                 ↓               │
│  ┌───────────────────────────────────────────────────┐    │
│  │         Code-Analy Analyzer Engine               │    │
│  │  (Detects: params, imports, dead code, etc.)     │    │
│  └───────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## The Confusion - Explained

### ❌ What Users Think:
> "The tests are the only code I can analyze"
> "I have to modify test files to check my code"

### ✅ Reality:
> "Tests validate the tool works correctly"
> "I can analyze ANY Python code I want!"

## Analogy

Think of Code-Analy like a **spell checker**:

| Spell Checker | Code-Analy |
|--------------|------------|
| Tests verify it catches "teh" → "the" | Tests verify it catches too many params |
| You use it on YOUR documents | You use it on YOUR code |
| You don't edit the spell checker tests | You don't edit Code-Analy tests |
| You write whatever document you want | You analyze whatever code you want |

## How To Use

### ❌ Wrong Approach:
```bash
# DON'T: Try to modify tests to analyze your code
vim tests/test_analyzer.py  # ← No!
```

### ✅ Correct Approach:
```bash
# DO: Use the tool on your code
python analyze_your_code.py your_file.py  # ← Yes!

# OR: Use the Python API
python -c "
from code_analy.analyzer import analyze_code
with open('your_file.py') as f:
    issues = analyze_code(f.read())
    print(issues)
"

# OR: Use the MCP server
python -m code_analy.server
# Then send YOUR code to analyze
```

## Real World Examples

### Example 1: Analyze Your Django Views

```bash
python analyze_your_code.py myproject/views.py
```

Output:
```
================================================================================
Analyzing: myproject/views.py
================================================================================

3 issue(s) found:

TOO MANY PARAMETERS:
  Line 45: Function 'create_user_profile' has 8 parameters (max: 5)

UNUSED IMPORT:
  Line 2: Unused import: 'datetime'

LONG METHOD:
  Line 120: Function 'process_payment' is too long (78 lines, max: 50)
```

### Example 2: Analyze Your Flask App

```bash
python analyze_your_code.py flask_app/
```

Output:
```
================================================================================
Analyzing directory: flask_app/
================================================================================

Analysis Summary:
  Total files: 15
  Total issues: 47
  Total lines of code: 2,340

Files with most issues:
  flask_app/routes.py: 12 issues
  flask_app/models.py: 8 issues
  flask_app/utils.py: 6 issues
```

### Example 3: Quick Check

```python
from code_analy.analyzer import analyze_code

# Your code snippet
code = """
def login(username, password, remember, session, redirect_url, csrf_token):
    # ... code ...
    pass
"""

issues = analyze_code(code)
print(f"Found {len(issues)} issue(s)")
# Output: Found 1 issue(s) (too many parameters)
```

## Summary Table

| Item | Hardcoded? | Modifiable? | Purpose |
|------|-----------|-------------|---------|
| **Tests** (`tests/`) | ✅ Yes | ❌ No (unless contributing) | Validate tool |
| **Your Code** | ❌ No | ✅ Yes - analyze anything! | Find issues |
| **Thresholds** (`config.py`) | ❌ No | ✅ Yes - customize! | Configure rules |
| **Analyzer** (`src/`) | 🔒 Core logic | ✅ Can extend | Tool engine |

## Key Points

1. **Tests are for validation** - They prove the analyzer works
2. **Your code is for analysis** - You choose what to analyze
3. **You don't modify tests** - Create your own analysis scripts
4. **Everything is customizable** - Thresholds, rules, etc.

## Getting Started Checklist

- [ ] Read [FAQ.md](FAQ.md)
- [ ] Read [QUICKSTART.md](QUICKSTART.md)
- [ ] Run `python analyze_your_code.py sample_code.py`
- [ ] Run `python analyze_your_code.py YOUR_FILE.py`
- [ ] Customize `config.py` if needed
- [ ] Integrate into your workflow!

## Questions?

See:
- [FAQ.md](FAQ.md) - Detailed questions and answers
- [QUICKSTART.md](QUICKSTART.md) - 60-second guide
- [README.md](README.md) - Full documentation

**Remember: The tests are the proof, your code is the subject!**
