# discord-mcp

Discordでメッセージを送信するMCP

## インストール

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

## デバッグ

```shell
npx @modelcontextprotocol/inspector uv run discord-mcp
```
