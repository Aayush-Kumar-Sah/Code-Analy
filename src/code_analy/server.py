"""MCP Server for Intelligent Code Analysis and Refactoring."""

import asyncio
import json
import os
from typing import Any
from mcp.server import Server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
from mcp.server.stdio import stdio_server

from .analyzer import analyze_code
from .ai_analyzer import AIAnalyzer
from .refactor import apply_refactoring
from .multi_file import analyze_directory


# Create MCP server instance
app = Server("code-analy")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available code analysis tools.
    
    Returns:
        List of Tool objects describing available analysis capabilities
    """
    return [
        Tool(
            name="analyze_code",
            description=(
                "Analyze Python source code for code smells and issues. "
                "Detects: too many parameters (>5), unused imports, dead code, "
                "long methods (>50 lines), deep nesting (>3 levels), and duplicate code blocks."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "source_code": {
                        "type": "string",
                        "description": "Python source code to analyze"
                    }
                },
                "required": ["source_code"]
            }
        ),
        Tool(
            name="detect_code_smells",
            description=(
                "Comprehensive code smell detection including: "
                "long methods (>50 lines), duplicate code blocks, "
                "deep nesting (>3 levels), too many parameters (>5), "
                "and dead code/unused imports."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "source_code": {
                        "type": "string",
                        "description": "Python source code to analyze"
                    }
                },
                "required": ["source_code"]
            }
        ),
        Tool(
            name="suggest_refactoring",
            description=(
                "AI-powered refactoring suggestions using LLM analysis. "
                "Provides specific, actionable recommendations with code examples "
                "and reasoning for each suggestion."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "source_code": {
                        "type": "string",
                        "description": "Python source code to analyze"
                    },
                    "api_key": {
                        "type": "string",
                        "description": "Optional API key for LLM provider"
                    },
                    "provider": {
                        "type": "string",
                        "description": "LLM provider: 'openai', 'anthropic', or 'mock' (default: 'mock')",
                        "enum": ["openai", "anthropic", "mock"]
                    }
                },
                "required": ["source_code"]
            }
        ),
        Tool(
            name="apply_refactoring",
            description=(
                "Apply safe, automated refactorings: "
                "rename variables/functions, extract methods, "
                "remove unused imports, or format code consistently."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "source_code": {
                        "type": "string",
                        "description": "Python source code to refactor"
                    },
                    "operation": {
                        "type": "string",
                        "description": "Refactoring operation to apply",
                        "enum": ["remove_unused_imports", "rename_variable", "extract_method", "format_code"]
                    },
                    "parameters": {
                        "type": "object",
                        "description": "Operation-specific parameters"
                    }
                },
                "required": ["source_code", "operation"]
            }
        ),
        Tool(
            name="analyze_directory",
            description=(
                "Analyze all Python files in a directory. "
                "Tracks dependencies between files and generates project-level insights."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "directory_path": {
                        "type": "string",
                        "description": "Path to the directory to analyze"
                    },
                    "recursive": {
                        "type": "boolean",
                        "description": "Whether to analyze subdirectories recursively (default: true)"
                    }
                },
                "required": ["directory_path"]
            }
        ),
        Tool(
            name="check_function_parameters",
            description=(
                "Check if functions have too many parameters. "
                "Functions with more than 5 parameters (excluding self/cls) "
                "are considered to have too many parameters."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "source_code": {
                        "type": "string",
                        "description": "Python source code to analyze"
                    },
                    "max_params": {
                        "type": "integer",
                        "description": "Maximum allowed parameters (default: 5)",
                        "default": 5
                    }
                },
                "required": ["source_code"]
            }
        ),
        Tool(
            name="check_unused_imports",
            description=(
                "Detect unused imports in Python code. "
                "Reports imports that are declared but never used."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "source_code": {
                        "type": "string",
                        "description": "Python source code to analyze"
                    }
                },
                "required": ["source_code"]
            }
        ),
        Tool(
            name="check_dead_code",
            description=(
                "Detect unreachable code (dead code) in Python source. "
                "Reports code that appears after return, raise, break, or continue statements."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "source_code": {
                        "type": "string",
                        "description": "Python source code to analyze"
                    }
                },
                "required": ["source_code"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent | ImageContent | EmbeddedResource]:
    """Handle tool execution requests.
    
    Args:
        name: Name of the tool to execute
        arguments: Tool arguments
        
    Returns:
        List containing the tool execution results
        
    Raises:
        ValueError: If the tool name is unknown or arguments are invalid
    """
    
    def format_result(issues: list, issue_type: str = None) -> dict:
        """Helper to format analysis results.
        
        Args:
            issues: List of all issues
            issue_type: Optional filter for specific issue type
            
        Returns:
            Formatted result dictionary
        """
        if issue_type:
            filtered_issues = [i for i in issues if i["type"] == issue_type]
        else:
            filtered_issues = issues
        
        return {
            "total_issues": len(filtered_issues),
            "issues": filtered_issues
        }
    
    try:
        # Handle different tools
        if name in ["analyze_code", "detect_code_smells"]:
            source_code = arguments.get("source_code")
            if not source_code:
                raise ValueError("source_code is required")
            
            issues = analyze_code(source_code)
            result = format_result(issues)
            
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]
        
        elif name == "suggest_refactoring":
            source_code = arguments.get("source_code")
            if not source_code:
                raise ValueError("source_code is required")
            
            # Get issues first
            issues = analyze_code(source_code)
            
            # Get AI suggestions
            api_key = arguments.get("api_key") or os.environ.get("LLM_API_KEY")
            provider = arguments.get("provider", "mock")
            
            ai_analyzer = AIAnalyzer(api_key=api_key, provider=provider)
            suggestions = ai_analyzer.suggest_refactorings(source_code, issues)
            
            result = {
                "total_suggestions": len(suggestions),
                "suggestions": [
                    {
                        "title": s.title,
                        "reasoning": s.reasoning,
                        "code_before": s.code_before,
                        "code_after": s.code_after,
                        "category": s.category,
                        "priority": s.priority
                    }
                    for s in suggestions
                ]
            }
            
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]
        
        elif name == "apply_refactoring":
            source_code = arguments.get("source_code")
            operation = arguments.get("operation")
            parameters = arguments.get("parameters", {})
            
            if not source_code or not operation:
                raise ValueError("source_code and operation are required")
            
            result = apply_refactoring(source_code, operation, **parameters)
            
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]
        
        elif name == "analyze_directory":
            directory_path = arguments.get("directory_path")
            recursive = arguments.get("recursive", True)
            
            if not directory_path:
                raise ValueError("directory_path is required")
            
            result = analyze_directory(directory_path, recursive)
            
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]
        
        elif name == "check_function_parameters":
            source_code = arguments.get("source_code")
            if not source_code:
                raise ValueError("source_code is required")
            
            issues = analyze_code(source_code)
            result = format_result(issues, "too_many_parameters")
            
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]
        
        elif name == "check_unused_imports":
            source_code = arguments.get("source_code")
            if not source_code:
                raise ValueError("source_code is required")
            
            issues = analyze_code(source_code)
            result = format_result(issues, "unused_import")
            
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]
        
        elif name == "check_dead_code":
            source_code = arguments.get("source_code")
            if not source_code:
                raise ValueError("source_code is required")
            
            issues = analyze_code(source_code)
            result = format_result(issues, "dead_code")
            
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]
        
        else:
            raise ValueError(f"Unknown tool: {name}")
    
    except ValueError as e:
        return [TextContent(
            type="text",
            text=json.dumps({"error": str(e)}, indent=2)
        )]
    except Exception as e:
        return [TextContent(
            type="text",
            text=json.dumps({"error": f"Unexpected error: {str(e)}"}, indent=2)
        )]


async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
