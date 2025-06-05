# Discord MCP Server

A Model Context Protocol (MCP) server that enables sending messages through Discord Bot.

## Overview

This project is an MCP server for sending messages using Discord Bot. It allows clients like Claude Desktop to send messages to configured Discord channels or user DMs.

## Features

- Message sending using Discord Bot token
- Support for both server channels and user DMs
- Standardized interface through MCP protocol

## Requirements

- uv
- Discord Bot Token

## Setup

```jsonc
{
  "mcpServers": {
    "discord-mcp-server": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/pycabbage/discord-mcp@main",
        "discord-mcp-server"
      ],
      "env": {
        "DISCORD_BOT_TOKEN": "your_bot_token_here",
        "DISCORD_SERVER_ID": "your_server_id",
        "DISCORD_CHANNEL_ID": "your_channel_id",
        // or:
        "DISCORD_USER_ID": "your_user_id_here",
      }
    }
  }
}
```

## License

This project is released under the MIT License. See the [LICENSE](LICENSE) file for details.
