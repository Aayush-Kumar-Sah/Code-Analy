"""AST-based code analysis tools for detecting code smells."""

import ast
from typing import List, Dict, Any, Set
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
