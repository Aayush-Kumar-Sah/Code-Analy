"""AST-based code analysis tools for detecting code smells."""

import ast
import hashlib
from collections import defaultdict
from typing import List, Dict, Any, Set, Tuple
from dataclasses import dataclass


@dataclass
class CodeIssue:
    """Represents a code issue found during analysis."""
    line: int
    column: int
    issue_type: str
    message: str
    severity: str = "warning"


class CodeAnalyzer:
    """AST-based code analyzer for detecting various code smells."""
    
    def __init__(self, source_code: str):
        """Initialize the analyzer with source code.
        
        Args:
            source_code: Python source code to analyze
        """
        self.source_code = source_code
        self.issues: List[CodeIssue] = []
        try:
            self.tree = ast.parse(source_code)
        except SyntaxError as e:
            raise ValueError(f"Invalid Python syntax: {e}")
    
    def analyze(self) -> List[CodeIssue]:
        """Run all analysis checks and return found issues.
        
        Returns:
            List of CodeIssue objects found during analysis
        """
        self.issues = []
        self._check_too_many_parameters()
        self._check_unused_imports()
        self._check_dead_code()
        self._check_long_methods()
        self._check_deep_nesting()
        self._check_duplicate_code()
        return self.issues
    
    def _check_too_many_parameters(self, max_params: int = 5) -> None:
        """Check for functions with too many parameters.
        
        Args:
            max_params: Maximum number of allowed parameters (default: 5)
        """
        for node in ast.walk(self.tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # Count parameters (excluding self/cls in methods)
                param_count = len(node.args.args)
                
                # Check if this is a method by looking at parent class
                is_method = self._is_method(node)
                if is_method and param_count > 0 and node.args.args[0].arg in ('self', 'cls'):
                    param_count -= 1
                
                # Also count other parameter types
                param_count += len(node.args.posonlyargs)
                param_count += len(node.args.kwonlyargs)
                # Note: *args and **kwargs are not counted as they serve different purposes
                
                if param_count > max_params:
                    self.issues.append(CodeIssue(
                        line=node.lineno,
                        column=node.col_offset,
                        issue_type="too_many_parameters",
                        message=f"Function '{node.name}' has {param_count} parameters (max: {max_params})",
                        severity="warning"
                    ))
    
    def _is_method(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
        """Check if a function is a method inside a class.
        
        Args:
            node: Function or AsyncFunction node
            
        Returns:
            True if the function is defined inside a class
        """
        for parent in ast.walk(self.tree):
            if isinstance(parent, ast.ClassDef):
                if node in ast.walk(parent):
                    return True
        return False
    
    def _check_unused_imports(self) -> None:
        """Check for unused imports in the code."""
        # Collect all imports
        imports: Dict[str, ast.ImportFrom | ast.Import] = {}
        
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    name = alias.asname if alias.asname else alias.name
                    imports[name] = node
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    name = alias.asname if alias.asname else alias.name
                    imports[name] = node
        
        # Collect all name references including in annotations
        used_names: Set[str] = set()
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Name):
                used_names.add(node.id)
            elif isinstance(node, ast.Attribute):
                # For attribute access like 'module.function'
                if isinstance(node.value, ast.Name):
                    used_names.add(node.value.id)
        
        # Find unused imports
        for import_name, import_node in imports.items():
            # Skip wildcard imports
            if import_name == '*':
                continue
            
            # Check if the import is used
            if import_name not in used_names:
                self.issues.append(CodeIssue(
                    line=import_node.lineno,
                    column=import_node.col_offset,
                    issue_type="unused_import",
                    message=f"Unused import: '{import_name}'",
                    severity="info"
                ))
    
    def _check_dead_code(self) -> None:
        """Check for unreachable code (dead code)."""
        for node in ast.walk(self.tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if hasattr(node, 'body') and node.body:
                    self._check_unreachable_code(node.body)
            elif isinstance(node, (ast.If, ast.For, ast.While, ast.With)):
                if hasattr(node, 'body') and node.body:
                    self._check_unreachable_code(node.body)
                # Also check else/orelse clauses
                if hasattr(node, 'orelse') and node.orelse:
                    self._check_unreachable_code(node.orelse)
                # Check finally blocks for With statements
                if hasattr(node, 'finalbody') and node.finalbody:
                    self._check_unreachable_code(node.finalbody)
    
    def _check_unreachable_code(self, body: List[ast.stmt]) -> None:
        """Check if there's code after return/raise/break/continue statements.
        
        Args:
            body: List of AST statement nodes to check
        """
        for i, stmt in enumerate(body):
            # Check if this is a terminal statement
            if isinstance(stmt, (ast.Return, ast.Raise)):
                # Check if there's code after this statement
                if i < len(body) - 1:
                    next_stmt = body[i + 1]
                    self.issues.append(CodeIssue(
                        line=next_stmt.lineno,
                        column=next_stmt.col_offset,
                        issue_type="dead_code",
                        message="Unreachable code after return/raise statement",
                        severity="warning"
                    ))
                    break  # Only report the first occurrence
            elif isinstance(stmt, (ast.Break, ast.Continue)):
                if i < len(body) - 1:
                    next_stmt = body[i + 1]
                    self.issues.append(CodeIssue(
                        line=next_stmt.lineno,
                        column=next_stmt.col_offset,
                        issue_type="dead_code",
                        message="Unreachable code after break/continue statement",
                        severity="warning"
                    ))
                    break
    
    def _check_long_methods(self, max_lines: int = 50) -> None:
        """Check for methods/functions that are too long.
        
        Args:
            max_lines: Maximum number of lines allowed (default: 50)
        """
        source_lines = self.source_code.splitlines()
        
        for node in ast.walk(self.tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # Calculate the number of lines in the function
                start_line = node.lineno
                end_line = node.end_lineno if node.end_lineno else start_line
                
                # Count non-empty, non-comment lines
                func_lines = 0
                for line_num in range(start_line - 1, end_line):
                    if line_num < len(source_lines):
                        line = source_lines[line_num].strip()
                        # Skip empty lines and comments
                        if line and not line.startswith('#'):
                            func_lines += 1
                
                if func_lines > max_lines:
                    self.issues.append(CodeIssue(
                        line=node.lineno,
                        column=node.col_offset,
                        issue_type="long_method",
                        message=f"Function '{node.name}' is too long ({func_lines} lines, max: {max_lines})",
                        severity="warning"
                    ))
    
    def _check_deep_nesting(self, max_depth: int = 3) -> None:
        """Check for deeply nested code blocks.
        
        Args:
            max_depth: Maximum nesting depth allowed (default: 3)
        """
        def calculate_depth(node: ast.AST, current_depth: int = 0) -> int:
            """Recursively calculate nesting depth."""
            max_depth_found = current_depth
            
            for child in ast.iter_child_nodes(node):
                # Increment depth for control flow structures
                if isinstance(child, (ast.If, ast.For, ast.While, ast.With, ast.Try)):
                    child_depth = calculate_depth(child, current_depth + 1)
                    max_depth_found = max(max_depth_found, child_depth)
                else:
                    child_depth = calculate_depth(child, current_depth)
                    max_depth_found = max(max_depth_found, child_depth)
            
            return max_depth_found
        
        for node in ast.walk(self.tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                depth = calculate_depth(node)
                if depth > max_depth:
                    self.issues.append(CodeIssue(
                        line=node.lineno,
                        column=node.col_offset,
                        issue_type="deep_nesting",
                        message=f"Function '{node.name}' has deep nesting (depth: {depth}, max: {max_depth})",
                        severity="warning"
                    ))
    
    def _check_duplicate_code(self, min_lines: int = 5) -> None:
        """Check for duplicate code blocks.
        
        Args:
            min_lines: Minimum number of lines to consider as duplicate (default: 5)
        """
        source_lines = self.source_code.splitlines()
        
        # Create a map of code block hashes to their locations
        block_hashes: Dict[str, List[Tuple[int, int]]] = defaultdict(list)
        
        # Analyze blocks of consecutive lines
        for start_line in range(len(source_lines)):
            for end_line in range(start_line + min_lines, min(start_line + min_lines + 20, len(source_lines) + 1)):
                # Extract block and normalize (remove leading/trailing whitespace)
                block_lines = []
                for i in range(start_line, end_line):
                    line = source_lines[i].strip()
                    # Skip empty lines and comments for comparison
                    if line and not line.startswith('#'):
                        block_lines.append(line)
                
                if len(block_lines) >= min_lines:
                    # Create hash of the normalized block
                    block_text = '\n'.join(block_lines)
                    block_hash = hashlib.md5(block_text.encode()).hexdigest()
                    
                    # Store location
                    block_hashes[block_hash].append((start_line + 1, end_line))
        
        # Report duplicates
        reported_blocks = set()
        for block_hash, locations in block_hashes.items():
            if len(locations) > 1 and block_hash not in reported_blocks:
                # Report the first occurrence
                first_start, first_end = locations[0]
                num_lines = first_end - first_start
                self.issues.append(CodeIssue(
                    line=first_start,
                    column=0,
                    issue_type="duplicate_code",
                    message=f"Duplicate code block found ({num_lines} lines, {len(locations)} occurrences)",
                    severity="info"
                ))
                reported_blocks.add(block_hash)


def analyze_code(source_code: str) -> List[Dict[str, Any]]:
    """Analyze Python source code and return list of issues.
    
    Args:
        source_code: Python source code to analyze
        
    Returns:
        List of dictionaries containing issue information
        
    Raises:
        ValueError: If the source code has invalid syntax
    """
    analyzer = CodeAnalyzer(source_code)
    issues = analyzer.analyze()
    
    return [
        {
            "line": issue.line,
            "column": issue.column,
            "type": issue.issue_type,
            "message": issue.message,
            "severity": issue.severity
        }
        for issue in issues
    ]
