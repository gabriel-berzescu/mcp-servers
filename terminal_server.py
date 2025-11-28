#!/usr/bin/env python3
"""
MCP Server with Windows Terminal Tool
Provides a terminal command execution tool for Windows 11
"""

import subprocess
import asyncio
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio


# Create server instance
server = Server("windows-terminal-server")


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools."""
    return [
        types.Tool(
            name="execute_terminal_command",
            description="Execute a command in the Windows terminal (cmd.exe). Returns the command output, exit code, and any errors.",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The command to execute in the Windows terminal"
                    },
                    "timeout": {
                        "type": "number",
                        "description": "Optional timeout in seconds (default: 30)",
                        "default": 30
                    }
                },
                "required": ["command"]
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool execution requests."""

    if name != "execute_terminal_command":
        raise ValueError(f"Unknown tool: {name}")

    if not arguments:
        raise ValueError("Missing arguments")

    command = arguments.get("command")
    if not command:
        raise ValueError("Missing command argument")

    timeout = arguments.get("timeout", 30)

    try:
        # Execute command using cmd.exe on Windows
        process = await asyncio.create_subprocess_shell(
            command,
            stdin=asyncio.subprocess.DEVNULL,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            shell=True
        )

        # Wait for command to complete with timeout
        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=timeout
            )
        except asyncio.TimeoutError:
            process.kill()
            await process.wait()
            return [
                types.TextContent(
                    type="text",
                    text=f"Command timed out after {timeout} seconds"
                )
            ]

        # Decode output
        stdout_text = stdout.decode('utf-8', errors='replace') if stdout else ""
        stderr_text = stderr.decode('utf-8', errors='replace') if stderr else ""

        # Format result
        result = f"Exit Code: {process.returncode}\n\n"

        if stdout_text:
            result += f"STDOUT:\n{stdout_text}\n"

        if stderr_text:
            result += f"STDERR:\n{stderr_text}\n"

        if not stdout_text and not stderr_text:
            result += "No output\n"

        return [
            types.TextContent(
                type="text",
                text=result
            )
        ]

    except Exception as e:
        return [
            types.TextContent(
                type="text",
                text=f"Error executing command: {str(e)}"
            )
        ]


async def main():
    """Run the server using stdio transport."""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="windows-terminal-server",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
