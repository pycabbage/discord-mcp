# Discord MCP Server

Discord Botでメッセージを送信できるModel Context Protocol (MCP) サーバー

## 概要

このプロジェクトは、Discord Botを使用してメッセージを送信するためのMCPサーバーです。Claude Desktopなどのクライアントから、設定されたDiscordチャンネルまたはユーザーのDMにメッセージを送信できます。

## 機能

- Discord Botトークンを使用したメッセージ送信
- サーバーのチャンネルまたはユーザーのDMへの送信対応
- MCPプロトコルによる標準化されたインターフェース

## 必要要件

- Python 3.13以上
- Discord Bot Token

## セットアップ

### 1. Discord Botの作成

1. [Discord Developer Portal](https://discord.com/developers/applications) にアクセス
2. 新しいアプリケーションを作成
3. Bot セクションでボットを作成し、トークンを取得
4. 必要な権限を設定（メッセージ送信など）

### 2. 環境変数の設定

`.env` ファイルを作成し、以下の環境変数を設定してください：

```env
# Discord Bot Token（必須）
DISCORD_BOT_TOKEN=your_bot_token_here

# オプション1: サーバーのチャンネルに送信する場合
DISCORD_SERVER_ID=your_server_id
DISCORD_CHANNEL_ID=your_channel_id

# オプション2: ユーザーのDMに送信する場合
DISCORD_USER_ID=your_user_id
```

注意：サーバー/チャンネル設定とユーザーDM設定のどちらか一方を選択してください。

### 3. インストール

```bash
uv add discord-mcp-server
```

または、開発版として：

```bash
git clone https://github.com/pycabbage/discord-mcp-server.git
cd discord-mcp-server
uv sync --dev
```

## 使用方法

### コマンドライン実行

```bash
discord-mcp-server
```

### Claude Desktopでの設定

Claude Desktopの設定ファイル（`claude_desktop_config.json`）に以下を追加：

```json
{
  "mcpServers": {
    "discord-mcp-server": {
      "command": "discord-mcp-server",
      "env": {
        "DISCORD_BOT_TOKEN": "your_bot_token_here",
        "DISCORD_SERVER_ID": "your_server_id",
        "DISCORD_CHANNEL_ID": "your_channel_id"
      }
    }
  }
}
```

## 利用可能なツール

### discord_send_message

Discord Botを使用してメッセージを送信します。

**パラメータ：**

- `message` (string, 必須): 送信するメッセージ内容（Discordマークダウン記法対応）

**例：**

```plaintext
環境変数で設定されたチャンネルまたはユーザーに「Hello, World!」を送信してください。
```

## 開発

### 開発環境のセットアップ

```bash
# リポジトリのクローン
git clone https://github.com/pycabbage/discord-mcp-server.git
cd discord-mcp-server

# 依存関係のインストール
uv sync --dev
```

### コード品質ツール

```bash
# Linting
uvx ruff check .

# Type checking
uvx mypy .

# Testing
uvx pytest
```

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は[LICENSE](LICENSE)ファイルをご確認ください。
