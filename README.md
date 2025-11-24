# Windows Terminal MCP Server

A Model Context Protocol (MCP) server that provides terminal command execution capabilities for Windows 11.

## Features

- Execute Windows terminal commands via cmd.exe
- Async command execution with configurable timeouts
- Returns stdout, stderr, and exit codes
- Stdio transport for easy integration with MCP clients

## Installation

1. Create and activate a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Server

```bash
python terminal_server.py
```

The server runs over stdio and can be integrated with any MCP client.

### Available Tools

#### `execute_terminal_command`

Executes a command in the Windows terminal.

**Parameters:**
- `command` (string, required): The command to execute
- `timeout` (number, optional): Timeout in seconds (default: 30)

**Returns:**
- Exit code
- Standard output (stdout)
- Standard error (stderr)

**Example:**
```json
{
  "command": "dir",
  "timeout": 10
}
```

## Configuration

To use this server with Claude Desktop or other MCP clients, add it to your MCP configuration file located at `%APPDATA%\Claude\claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "windows-terminal": {
      "command": "c:\\path\\to\\mcp-servers\\venv\\Scripts\\python.exe",
      "args": ["c:\\path\\to\\mcp-servers\\terminal_server.py"]
    }
  }
}
```

**Important:** Make sure to use the full path to the Python executable in your virtual environment, not just `python`. This ensures the MCP dependencies installed in your venv are available.

## Security

This server is designed to run in a sandboxed environment. Be cautious when executing arbitrary commands, as they will run with the permissions of the user running the server.

## Requirements

- Python 3.10+
- Windows 11
- MCP Python SDK

## License

MIT
