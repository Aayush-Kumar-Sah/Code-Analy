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
    
    # Validate common parameter
    source_code = arguments.get("source_code")
    if not source_code:
        raise ValueError("source_code is required")
    
    try:
        issues = analyze_code(source_code)
        
        if name == "analyze_code":
            result = format_result(issues)
        elif name == "check_function_parameters":
            result = format_result(issues, "too_many_parameters")
        elif name == "check_unused_imports":
            result = format_result(issues, "unused_import")
        elif name == "check_dead_code":
            result = format_result(issues, "dead_code")
        else:
            raise ValueError(f"Unknown tool: {name}")
        
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]
    
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
