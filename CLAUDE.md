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

### 2. Resource Templates

Returns available message templates as JSON.

- **Output**: Array of templates with id, name, description, content, and placeholders
- **Available templates**: greeting, task_completed, error_notification, reminder, progress_update

## Environment Setup

The server requires the following environment variables:

- `DISCORD_TOKEN`: Discord bot token
- `DISCORD_USER_ID`: Discord user ID

These should be configured in a `.env` file or set as environment variables.

## Commands

### Running the Discord MCP Server

```bash
# Run the MCP server using uv
uv run discord-mcp

# Run with verbose output
uv run discord-mcp -v

# Debug with MCP Inspector
pnpm dlx @modelcontextprotocol/inspector@latest uv run discord-mcp
```

### Development Commands

```bash
# Format code with Ruff
uvx ruff format .

# Lint code with Ruff
uvx ruff check .

# Type check with Pyright
uvx pyright
```

## Testing

To test the Discord MCP server, follow these steps:

1. Set up environment variables in a `.env` file:

   ```env
   DISCORD_TOKEN=your_discord_bot_token
   DISCORD_USER_ID=your_discord_user_id
   ```

2. Run the MCP server with debugging enabled:

   ```shell
   uv run discord-mcp
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

## Development Notes

- コード変更後、 `uvx ruff format .` コマンドを実行し、フォーマットエラーを修正します。
- コード変更後、 `uvx pyright` コマンドで型チェックを行ってください。
- コード変更後、コミットを行いません。
