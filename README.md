# discord-mcp

Discordでメッセージを送信するMCP

## インストール

### `uvx`

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
      "env": {
        "DISCORD_TOKEN": "YOUR_DISCORD_BOT_TOKEN",
        "DISCORD_USER_ID": "YOUR_DISCORD_USER_ID"
      }
    }
  }
}
```

### Docker

```json
{
  "mcpServers": {
    "discord-mcp": {
      "command": "docker",
      "args": [
        "run",
        "--pull",
        "always",
        "-i",
        "--rm",
        "-e",
        "DISCORD_TOKEN",
        "-e",
        "DISCORD_USER_ID",
        "ghcr.io/pycabbage/discord-mcp:latest"
      ],
      "env": {
        "DISCORD_TOKEN": "YOUR_DISCORD_BOT_TOKEN",
        "DISCORD_USER_ID": "YOUR_DISCORD_USER_ID"
      }
    }
  }
}
```

## デバッグ

```shell
pnpm dlx @modelcontextprotocol/inspector@latest uv run discord-mcp
```
