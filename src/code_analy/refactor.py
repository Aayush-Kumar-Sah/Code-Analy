"""Automated code refactoring operations."""

import ast
import re
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass


@dataclass
class RefactoringResult:
    """Result of a refactoring operation."""
    success: bool
    message: str
    original_code: str
    refactored_code: str
    changes_made: List[str]


class CodeRefactor:
    """Automated code refactoring operations."""
    
    def __init__(self, source_code: str):
        """Initialize the refactoring engine.
        
        Args:
            source_code: Python source code to refactor
        """
        self.source_code = source_code
        self.lines = source_code.splitlines()
        self.changes_made: List[str] = []
    
    def remove_unused_imports(self, unused_imports: List[str]) -> RefactoringResult:
        """Remove unused import statements.
        
        Args:
            unused_imports: List of unused import names
            
        Returns:
            RefactoringResult with the refactored code
        """
        refactored_lines = []
        imports_removed = []
        
        for line in self.lines:
            # Check if this line contains an unused import
            should_keep = True
            for unused in unused_imports:
                # Match various import patterns
                if re.match(rf'^\s*import\s+{re.escape(unused)}\s*$', line):
                    should_keep = False
                    imports_removed.append(unused)
                    break
                elif re.search(rf'\bfrom\s+\S+\s+import\s+.*\b{re.escape(unused)}\b', line):
                    # Handle "from X import Y" - remove only the specific import
                    if ',' in line:
                        # Multiple imports on one line
                        line = re.sub(rf',?\s*{re.escape(unused)}\s*,?', '', line)
                        line = re.sub(r',\s*$', '', line)  # Remove trailing comma
                        line = re.sub(r'import\s*,', 'import ', line)  # Remove leading comma after import
                        if 'import' in line and not re.search(r'import\s+\w', line):
                            should_keep = False
                    else:
                        # Single import on the line
                        should_keep = False
                    imports_removed.append(unused)
                    break
            
            if should_keep:
                refactored_lines.append(line)
        
        refactored_code = '\n'.join(refactored_lines)
        
        return RefactoringResult(
            success=True,
            message=f"Removed {len(imports_removed)} unused import(s): {', '.join(imports_removed)}",
            original_code=self.source_code,
            refactored_code=refactored_code,
            changes_made=[f"Removed unused import: {imp}" for imp in imports_removed]
        )
    
    def rename_variable(
        self, 
        old_name: str, 
        new_name: str,
        scope: Optional[str] = None
    ) -> RefactoringResult:
        """Rename a variable throughout the code.
        
        Args:
            old_name: Current variable name
            new_name: New variable name
            scope: Optional scope (function name) to limit renaming
            
        Returns:
            RefactoringResult with the refactored code
        """
        try:
            tree = ast.parse(self.source_code)
        except SyntaxError as e:
            return RefactoringResult(
                success=False,
                message=f"Syntax error in source code: {e}",
                original_code=self.source_code,
                refactored_code=self.source_code,
                changes_made=[]
            )
        
        # Find all occurrences of the variable
        occurrences = []
        
        class VariableFinder(ast.NodeVisitor):
            def __init__(self, target_name: str, target_scope: Optional[str]):
                self.target_name = target_name
                self.target_scope = target_scope
                self.current_scope = None
                self.occurrences = []
            
            def visit_FunctionDef(self, node):
                old_scope = self.current_scope
                self.current_scope = node.name
                self.generic_visit(node)
                self.current_scope = old_scope
            
            def visit_Name(self, node):
                if node.id == self.target_name:
                    if self.target_scope is None or self.current_scope == self.target_scope:
                        self.occurrences.append((node.lineno, node.col_offset))
        
        finder = VariableFinder(old_name, scope)
        finder.visit(tree)
        occurrences = finder.occurrences
        
        if not occurrences:
            return RefactoringResult(
                success=False,
                message=f"Variable '{old_name}' not found in the specified scope",
                original_code=self.source_code,
                refactored_code=self.source_code,
                changes_made=[]
            )
        
        # Replace occurrences (from last to first to maintain positions)
        refactored_lines = self.lines.copy()
        for line_num, col_offset in sorted(occurrences, reverse=True):
            line_idx = line_num - 1
            line = refactored_lines[line_idx]
            
            # Use word boundaries to avoid partial replacements
            pattern = r'\b' + re.escape(old_name) + r'\b'
            refactored_lines[line_idx] = re.sub(pattern, new_name, line, count=1)
        
        refactored_code = '\n'.join(refactored_lines)
        
        return RefactoringResult(
            success=True,
            message=f"Renamed '{old_name}' to '{new_name}' ({len(occurrences)} occurrences)",
            original_code=self.source_code,
            refactored_code=refactored_code,
            changes_made=[f"Renamed variable: {old_name} -> {new_name}"]
        )
    
    def extract_method(
        self,
        start_line: int,
        end_line: int,
        method_name: str
    ) -> RefactoringResult:
        """Extract a code block into a separate method.
        
        Args:
            start_line: Starting line number (1-indexed)
            end_line: Ending line number (1-indexed)
            method_name: Name for the extracted method
            
        Returns:
            RefactoringResult with the refactored code
        """
        if start_line < 1 or end_line > len(self.lines) or start_line > end_line:
            return RefactoringResult(
                success=False,
                message="Invalid line range",
                original_code=self.source_code,
                refactored_code=self.source_code,
                changes_made=[]
            )
        
        # Extract the code block
        extracted_lines = self.lines[start_line - 1:end_line]
        
        # Determine indentation
        base_indent = len(extracted_lines[0]) - len(extracted_lines[0].lstrip())
        
        # Create the new method
        method_lines = [
            f"def {method_name}():",
        ]
        
        for line in extracted_lines:
            # Adjust indentation
            if line.strip():
                method_lines.append("    " + line[base_indent:])
            else:
                method_lines.append("")
        
        # Build refactored code
        refactored_lines = []
        
        # Add lines before extraction point
        refactored_lines.extend(self.lines[:start_line - 1])
        
        # Add method call
        indent = " " * base_indent
        refactored_lines.append(f"{indent}{method_name}()")
        
        # Add lines after extraction point
        refactored_lines.extend(self.lines[end_line:])
        
        # Insert the extracted method at the beginning (after imports)
        insert_pos = 0
        for i, line in enumerate(refactored_lines):
            if line.strip() and not line.strip().startswith('import') and not line.strip().startswith('from'):
                insert_pos = i
                break
        
        # Insert method with blank lines
        refactored_lines.insert(insert_pos, "")
        refactored_lines.insert(insert_pos, "")
        for method_line in reversed(method_lines):
            refactored_lines.insert(insert_pos, method_line)
        
        refactored_code = '\n'.join(refactored_lines)
        
        return RefactoringResult(
            success=True,
            message=f"Extracted method '{method_name}' from lines {start_line}-{end_line}",
            original_code=self.source_code,
            refactored_code=refactored_code,
            changes_made=[f"Extracted method: {method_name}"]
        )
    
    def format_code(self) -> RefactoringResult:
        """Format code consistently using basic formatting rules.
        
        Returns:
            RefactoringResult with the formatted code
        """
        formatted_lines = []
        changes = []
        
        for i, line in enumerate(self.lines):
            original_line = line
            
            # Remove trailing whitespace
            line = line.rstrip()
            
            # Ensure blank lines between top-level definitions
            if i > 0 and line.startswith(('def ', 'class ', 'async def ')):
                if formatted_lines and formatted_lines[-1].strip():
                    # Add blank line before function/class if missing
                    if not (len(formatted_lines) > 1 and formatted_lines[-1] == ""):
                        formatted_lines.append("")
            
            formatted_lines.append(line)
            
            if original_line != line:
                changes.append(f"Formatted line {i + 1}")
        
        # Remove multiple consecutive blank lines
        final_lines = []
        prev_blank = False
        for line in formatted_lines:
            is_blank = not line.strip()
            if is_blank and prev_blank:
                continue
            final_lines.append(line)
            prev_blank = is_blank
        
        refactored_code = '\n'.join(final_lines)
        
        return RefactoringResult(
            success=True,
            message=f"Code formatted ({len(changes)} changes)",
            original_code=self.source_code,
            refactored_code=refactored_code,
            changes_made=changes if changes else ["Code formatting applied"]
        )


def apply_refactoring(
    source_code: str,
    operation: str,
    **kwargs
) -> Dict[str, Any]:
    """Apply a refactoring operation to source code.
    
    Args:
        source_code: Python source code to refactor
        operation: Type of refactoring to apply
        **kwargs: Operation-specific parameters
        
    Returns:
        Dictionary with refactoring results
    """
    refactor = CodeRefactor(source_code)
    
    if operation == "remove_unused_imports":
        unused_imports = kwargs.get("unused_imports", [])
        result = refactor.remove_unused_imports(unused_imports)
    
    elif operation == "rename_variable":
        old_name = kwargs.get("old_name")
        new_name = kwargs.get("new_name")
        scope = kwargs.get("scope")
        
        if not old_name or not new_name:
            return {
                "success": False,
                "message": "Missing required parameters: old_name and new_name",
                "original_code": source_code,
                "refactored_code": source_code,
                "changes_made": []
            }
        
        result = refactor.rename_variable(old_name, new_name, scope)
    
    elif operation == "extract_method":
        start_line = kwargs.get("start_line")
        end_line = kwargs.get("end_line")
        method_name = kwargs.get("method_name")
        
        if not all([start_line, end_line, method_name]):
            return {
                "success": False,
                "message": "Missing required parameters: start_line, end_line, method_name",
                "original_code": source_code,
                "refactored_code": source_code,
                "changes_made": []
            }
        
        result = refactor.extract_method(start_line, end_line, method_name)
    
    elif operation == "format_code":
        result = refactor.format_code()
    
    else:
        return {
            "success": False,
            "message": f"Unknown operation: {operation}",
            "original_code": source_code,
            "refactored_code": source_code,
            "changes_made": []
        }
    
    return {
        "success": result.success,
        "message": result.message,
        "original_code": result.original_code,
        "refactored_code": result.refactored_code,
        "changes_made": result.changes_made
    }
