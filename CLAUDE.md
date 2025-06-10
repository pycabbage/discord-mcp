# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This repository contains a Discord Model Context Protocol (MCP) server written in Python. It allows sending messages to Discord channels or DMs through MCP.

## Architecture

The codebase is organized as follows:

- `discord_mcp/server.py`: The core MCP server implementation that handles tool registration and execution
- `discord_mcp/discord.py`: Handles Discord client functionality and message sending
- `discord_mcp/models.py`: Defines data models for Discord tools and messages
- `discord_mcp/env.py`: Environment configuration for Discord bot token and user ID

The server exposes a single MCP tool called `send_message` which allows sending messages to Discord.

## Environment Setup

The server requires the following environment variables:

- `DISCORD_TOKEN`: Discord bot token
- `DISCORD_USER_ID`: Discord user ID

These should be configured in a `.env` file or set as environment variables.

## Commands

### Running the Discord MCP Server

```bash
# Run the MCP server directly
python -m discord_mcp

# Run with verbose output
python -m discord_mcp -v

# Debug with MCP Inspector
npx @modelcontextprotocol/inspector uv run discord-mcp
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