"""MCP Server for Intelligent Code Analysis and Refactoring."""

import asyncio
import json
from typing import Any
from mcp.server import Server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
from mcp.server.stdio import stdio_server

from .analyzer import analyze_code


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
                "Detects: functions with too many parameters (>5), "
                "unused imports, and dead/unreachable code."
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
    if name == "analyze_code":
        source_code = arguments.get("source_code")
        if not source_code:
            raise ValueError("source_code is required")
        
        try:
            issues = analyze_code(source_code)
            result = {
                "total_issues": len(issues),
                "issues": issues
            }
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]
        except ValueError as e:
            return [TextContent(
                type="text",
                text=json.dumps({"error": str(e)}, indent=2)
            )]
    
    elif name == "check_function_parameters":
        source_code = arguments.get("source_code")
        max_params = arguments.get("max_params", 5)
        
        if not source_code:
            raise ValueError("source_code is required")
        
        try:
            all_issues = analyze_code(source_code)
            param_issues = [
                issue for issue in all_issues
                if issue["type"] == "too_many_parameters"
            ]
            result = {
                "total_issues": len(param_issues),
                "issues": param_issues
            }
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]
        except ValueError as e:
            return [TextContent(
                type="text",
                text=json.dumps({"error": str(e)}, indent=2)
            )]
    
    elif name == "check_unused_imports":
        source_code = arguments.get("source_code")
        if not source_code:
            raise ValueError("source_code is required")
        
        try:
            all_issues = analyze_code(source_code)
            import_issues = [
                issue for issue in all_issues
                if issue["type"] == "unused_import"
            ]
            result = {
                "total_issues": len(import_issues),
                "issues": import_issues
            }
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]
        except ValueError as e:
            return [TextContent(
                type="text",
                text=json.dumps({"error": str(e)}, indent=2)
            )]
    
    elif name == "check_dead_code":
        source_code = arguments.get("source_code")
        if not source_code:
            raise ValueError("source_code is required")
        
        try:
            all_issues = analyze_code(source_code)
            dead_code_issues = [
                issue for issue in all_issues
                if issue["type"] == "dead_code"
            ]
            result = {
                "total_issues": len(dead_code_issues),
                "issues": dead_code_issues
            }
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]
        except ValueError as e:
            return [TextContent(
                type="text",
                text=json.dumps({"error": str(e)}, indent=2)
            )]
    
    else:
        raise ValueError(f"Unknown tool: {name}")


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
