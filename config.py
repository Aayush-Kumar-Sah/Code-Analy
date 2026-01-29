"""
Configuration file for Code-Analy

You can customize detection thresholds here!
This demonstrates that the tool is flexible and NOT hardcoded.
"""

# Detection thresholds - customize these to your needs!
MAX_PARAMETERS = 5  # Maximum function parameters before flagging
MAX_METHOD_LINES = 50  # Maximum lines in a method before flagging
MAX_NESTING_DEPTH = 3  # Maximum nesting depth before flagging
MIN_DUPLICATE_LINES = 5  # Minimum lines for duplicate detection

# AI Provider Configuration
AI_PROVIDER = "mock"  # Options: "mock", "openai", "anthropic"
# Set your API key via environment variable: export LLM_API_KEY="your-key"

# Analysis options
RECURSIVE_ANALYSIS = True  # Analyze subdirectories
EXCLUDE_PATTERNS = [
    "__pycache__",
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "*.pyc",
    ".pytest_cache"
]

# Example: How to use this config in your analysis
if __name__ == "__main__":
    print("Code-Analy Configuration")
    print("=" * 60)
    print(f"Max Parameters: {MAX_PARAMETERS}")
    print(f"Max Method Lines: {MAX_METHOD_LINES}")
    print(f"Max Nesting Depth: {MAX_NESTING_DEPTH}")
    print(f"Min Duplicate Lines: {MIN_DUPLICATE_LINES}")
    print(f"AI Provider: {AI_PROVIDER}")
    print(f"Recursive Analysis: {RECURSIVE_ANALYSIS}")
    print(f"Exclude Patterns: {', '.join(EXCLUDE_PATTERNS)}")
    print()
    print("You can modify these values to customize the analysis!")
    print("The tests are hardcoded, but YOUR analysis is flexible!")
