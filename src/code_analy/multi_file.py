"""Multi-file and directory analysis support."""

import os
import ast
from pathlib import Path
from typing import List, Dict, Any, Set
from dataclasses import dataclass, field

from .analyzer import analyze_code, CodeAnalyzer


@dataclass
class FileAnalysis:
    """Analysis results for a single file."""
    filepath: str
    issues: List[Dict[str, Any]]
    imports: List[str] = field(default_factory=list)
    functions: List[str] = field(default_factory=list)
    classes: List[str] = field(default_factory=list)
    lines_of_code: int = 0


@dataclass
class ProjectAnalysis:
    """Analysis results for an entire project."""
    total_files: int
    total_issues: int
    file_analyses: List[FileAnalysis]
    dependencies: Dict[str, List[str]] = field(default_factory=dict)
    summary: Dict[str, Any] = field(default_factory=dict)


class MultiFileAnalyzer:
    """Analyzer for multiple files and directories."""
    
    def __init__(self, path: str, recursive: bool = True):
        """Initialize the multi-file analyzer.
        
        Args:
            path: File or directory path to analyze
            recursive: Whether to analyze subdirectories
        """
        self.path = Path(path)
        self.recursive = recursive
        self.file_analyses: List[FileAnalysis] = []
    
    def analyze(self) -> ProjectAnalysis:
        """Analyze all Python files in the given path.
        
        Returns:
            ProjectAnalysis with aggregated results
        """
        python_files = self._find_python_files()
        
        # Analyze each file
        for filepath in python_files:
            try:
                file_analysis = self._analyze_file(filepath)
                self.file_analyses.append(file_analysis)
            except Exception as e:
                # Skip files that can't be analyzed
                print(f"Error analyzing {filepath}: {e}")
                continue
        
        # Build dependency graph
        dependencies = self._build_dependency_graph()
        
        # Generate summary
        summary = self._generate_summary()
        
        return ProjectAnalysis(
            total_files=len(self.file_analyses),
            total_issues=sum(len(fa.issues) for fa in self.file_analyses),
            file_analyses=self.file_analyses,
            dependencies=dependencies,
            summary=summary
        )
    
    def _find_python_files(self) -> List[Path]:
        """Find all Python files in the given path.
        
        Returns:
            List of Python file paths
        """
        if self.path.is_file():
            return [self.path] if self.path.suffix == '.py' else []
        
        # Directory - find all .py files
        if self.recursive:
            return list(self.path.rglob('*.py'))
        else:
            return list(self.path.glob('*.py'))
    
    def _analyze_file(self, filepath: Path) -> FileAnalysis:
        """Analyze a single Python file.
        
        Args:
            filepath: Path to the Python file
            
        Returns:
            FileAnalysis with results
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        # Get code issues
        issues = analyze_code(source_code)
        
        # Parse AST to extract metadata
        try:
            tree = ast.parse(source_code)
        except SyntaxError:
            return FileAnalysis(
                filepath=str(filepath),
                issues=issues,
                lines_of_code=len(source_code.splitlines())
            )
        
        # Extract imports, functions, and classes
        imports = []
        functions = []
        classes = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                functions.append(node.name)
            elif isinstance(node, ast.ClassDef):
                classes.append(node.name)
        
        # Count lines of code (excluding blank lines and comments)
        lines_of_code = 0
        for line in source_code.splitlines():
            stripped = line.strip()
            if stripped and not stripped.startswith('#'):
                lines_of_code += 1
        
        return FileAnalysis(
            filepath=str(filepath),
            issues=issues,
            imports=imports,
            functions=functions,
            classes=classes,
            lines_of_code=lines_of_code
        )
    
    def _build_dependency_graph(self) -> Dict[str, List[str]]:
        """Build a dependency graph between files.
        
        Returns:
            Dictionary mapping file paths to their dependencies
        """
        dependencies = {}
        
        # Create a mapping of module names to file paths
        module_to_file = {}
        for analysis in self.file_analyses:
            # Convert file path to potential module name
            rel_path = Path(analysis.filepath).relative_to(self.path) if self.path.is_dir() else Path(analysis.filepath)
            module_name = str(rel_path.with_suffix('')).replace(os.sep, '.')
            module_to_file[module_name] = analysis.filepath
        
        # Build dependency relationships
        for analysis in self.file_analyses:
            deps = []
            for imp in analysis.imports:
                # Check if this import corresponds to another file in the project
                for module_name, filepath in module_to_file.items():
                    if imp.startswith(module_name) or module_name.endswith(imp):
                        if filepath != analysis.filepath:
                            deps.append(filepath)
            
            if deps:
                dependencies[analysis.filepath] = list(set(deps))
        
        return dependencies
    
    def _generate_summary(self) -> Dict[str, Any]:
        """Generate a summary of the project analysis.
        
        Returns:
            Dictionary with summary statistics
        """
        if not self.file_analyses:
            return {}
        
        # Count issues by type
        issue_counts = {}
        for analysis in self.file_analyses:
            for issue in analysis.issues:
                issue_type = issue['type']
                issue_counts[issue_type] = issue_counts.get(issue_type, 0) + 1
        
        # Calculate totals
        total_lines = sum(fa.lines_of_code for fa in self.file_analyses)
        total_functions = sum(len(fa.functions) for fa in self.file_analyses)
        total_classes = sum(len(fa.classes) for fa in self.file_analyses)
        
        # Find files with most issues
        files_by_issues = sorted(
            self.file_analyses,
            key=lambda fa: len(fa.issues),
            reverse=True
        )
        
        top_files = [
            {
                "file": fa.filepath,
                "issues": len(fa.issues)
            }
            for fa in files_by_issues[:5]
        ]
        
        return {
            "total_lines_of_code": total_lines,
            "total_functions": total_functions,
            "total_classes": total_classes,
            "issue_counts": issue_counts,
            "top_files_with_issues": top_files,
            "average_issues_per_file": (
                sum(len(fa.issues) for fa in self.file_analyses) / len(self.file_analyses)
                if self.file_analyses else 0
            )
        }


def analyze_directory(directory_path: str, recursive: bool = True) -> Dict[str, Any]:
    """Analyze all Python files in a directory.
    
    Args:
        directory_path: Path to the directory
        recursive: Whether to analyze subdirectories
        
    Returns:
        Dictionary with project analysis results
    """
    analyzer = MultiFileAnalyzer(directory_path, recursive)
    project_analysis = analyzer.analyze()
    
    return {
        "total_files": project_analysis.total_files,
        "total_issues": project_analysis.total_issues,
        "files": [
            {
                "filepath": fa.filepath,
                "issues": fa.issues,
                "imports": fa.imports,
                "functions": fa.functions,
                "classes": fa.classes,
                "lines_of_code": fa.lines_of_code
            }
            for fa in project_analysis.file_analyses
        ],
        "dependencies": project_analysis.dependencies,
        "summary": project_analysis.summary
    }
