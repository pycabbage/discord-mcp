# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This repository contains a Discord Model Context Protocol (MCP) server written in Python. It provides tools for sending messages and interacting with Discord, as well as resources for accessing message history and templates.

## Architecture

The codebase is organized as follows:

- `discord_mcp/server.py`: The core MCP server implementation that handles tool registration, execution, and resource serving
- `discord_mcp/discord.py`: Handles Discord client functionality including message sending, user interaction, and message history retrieval
- `discord_mcp/models.py`: Defines data models for Discord tools and messages
- `discord_mcp/env.py`: Environment configuration for Discord bot token and user ID
- `discord_mcp/templates.py`: Message template management with predefined templates

## MCP Tools

The server exposes the following tools:

### 1. send_message
Sends a message to a Discord DM channel.
- **Input**: `content` (string) - The message content to send
- **Output**: Success/error status with destination information

### 2. ask_to_user
Sends a message to a user and waits for their response.
- **Input**: 
  - `content` (string) - The message content to send
  - `timeout_seconds` (int, default: 60) - Timeout for waiting response
- **Output**: User's response or timeout/error status
- **Note**: Uses timestamp checking to ensure only messages sent after the prompt are accepted as responses

## MCP Resources

The server provides the following resources:

### 1. discord://dm-history
Returns recent DM message history as JSON.
- **Output**: Array of messages with id, author, content, timestamp, and bot status
- **Limit**: 10 most recent messages (chronologically ordered)

## Environment Setup

The server requires the following environment variables:

- `DISCORD_TOKEN`: Discord bot token
- `DISCORD_USER_ID`: Discord user ID

These should be configured in a `.env` file or set as environment variables.

## Commands

### Running the Discord MCP Server

```bash
# Run the MCP server using uv (default: STDIO)
uv run discord-mcp

# Run with verbose output
uv run discord-mcp -v

# Run as SSE server on port 8080
uv run discord-mcp -t sse

# Run as HTTP server on custom port
uv run discord-mcp -t streamable_http -p 3000

# Run directly with Python
python -m discord_mcp

# Run with verbose output (Python)
python -m discord_mcp -v

# Debug with MCP Inspector
npx @modelcontextprotocol/inspector uv run discord-mcp
```

### Server Types

The Discord MCP server supports three different transport protocols:

1. **STDIO (default)**: Standard input/output communication
   ```bash
   uv run discord-mcp
   ```

2. **SSE (Server-Sent Events)**: HTTP-based server with SSE transport
   ```bash
   uv run discord-mcp -t sse -p 8080
   ```

3. **Streamable HTTP**: HTTP-based server with streaming responses
   ```bash
   uv run discord-mcp -t streamable_http -p 8080
   ```

### Development Commands

```bash
# Format code with Ruff
ruff format .

# Lint code with Ruff
ruff check .
```

## Testing

To test the Discord MCP server, follow these steps:

1. Set up environment variables in a `.env` file:
   ```
   DISCORD_TOKEN=your_discord_bot_token
   DISCORD_USER_ID=your_discord_user_id
   ```

2. Run the MCP server with debugging enabled:
   ```bash
   python -m discord_mcp -v
   ```

3. Use an MCP client to send requests to the server.

## Installation

This package can be installed as an MCP server using:

```json
{
  "mcpServers": {
    "discord-mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/pycabbage/discord-mcp@main",
        "discord-mcp"
      ],
      "env": {}
    }
  }
}
```

## Code Guidelines

- ユーザーへの返答とコード内のコメントは日本語で記述します。