# Discord MCP Server [WIP]

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

### Environment Variables

環境変数は以下の方法で設定できます：

1. **環境変数として直接設定**
2. **.envファイルを使用** (Pydantic BaseSettingsにより自動読み込み)

必要な環境変数：

- `DISCORD_BOT_TOKEN`: Discord Botのトークン（必須）
- 以下のいずれか：
  - チャンネル送信: `DISCORD_SERVER_ID` と `DISCORD_CHANNEL_ID`
  - DM送信: `DISCORD_USER_ID`

### .env ファイルの例

```bash
# Discord Bot Token (必須)
DISCORD_BOT_TOKEN=your_bot_token_here

# サーバーチャンネル送信の場合
DISCORD_SERVER_ID=1234567890
DISCORD_CHANNEL_ID=0987654321

# またはDM送信の場合（上記の代わりに）
# DISCORD_USER_ID=1111111111
```

### Claude Desktop Configuration

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

## Debugging

```shell
git clone https://github.com/pycabbage/discord-mcp.git
cd discord-mcp
uv sync
npx @modelcontextprotocol/inspector -e "DISCORD_BOT_TOKEN=your_bot_token_here" -e "DISCORD_USER_ID=your_user_id_here" uv run discord-mcp-server
```

## License

This project is released under the MIT License. See the [LICENSE](LICENSE) file for details.
