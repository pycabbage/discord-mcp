# Discord MCP Server

Discord Botでメッセージを送信できるMCPサーバー

## 概要

Discord MCP Serverは、Model Context Protocol (MCP) を使用してDiscord Botの機能を提供するサーバーです。AIエージェントが作業開始、途中、終了時にDiscordチャンネルやユーザーにメッセージを送信できます。

## 主な機能

- Discord Botトークンによる認証
- 指定されたサーバーのチャンネルへのメッセージ送信
- 指定されたユーザーへのDM送信
- 環境変数による設定管理
- MCPプロトコルによるツール提供

## 技術スタック

- **Python**: 3.13.4
- **パッケージマネージャー**: uv
- **コード品質管理**: ruff, mypy
- **テストフレームワーク**: pytest
- **主要ライブラリ**: discord.py, mcp, pydantic

## 必要な環境変数

以下の環境変数を設定する必要があります：

### 必須
- `DISCORD_BOT_TOKEN`: Discord Botのトークン

### 送信先設定（いずれか一方を選択）
- **サーバーのチャンネルに送信する場合**:
  - `DISCORD_SERVER_ID`: サーバー（ギルド）ID
  - `DISCORD_CHANNEL_ID`: チャンネルID

- **ユーザーにDMを送信する場合**:
  - `DISCORD_USER_ID`: ユーザーID

## インストール方法

### 1. リポジトリのクローン

```bash
git clone <repository-url>
cd discord-mcp-server
```

### 2. uvのインストール

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
```

### 3. 依存関係のインストール

```bash
uv sync
```

### 4. 環境変数の設定

`.env.example`をコピーして`.env`ファイルを作成し、必要な値を設定してください：

```bash
cp .env.example .env
# .envファイルを編集して適切な値を設定
```

## 開発環境構築方法

### 1. 開発用依存関係のインストール

```bash
uv sync --dev
```

### 2. コード品質チェック

```bash
# Ruffによるlint
uv run ruff check src/ tests/

# Ruffによる自動修正
uv run ruff check --fix src/ tests/

# mypyによる型チェック
uv run mypy src/

# テストの実行
uv run pytest tests/ -v
```

### 3. フォーマット

```bash
uv run ruff format src/ tests/
```

## 使用方法

### MCPサーバーとして起動

```bash
uv run discord-mcp-server
```

### 提供されるツール

#### `discord_send_message`

Discord Botを使用してメッセージを送信します。

**パラメータ:**
- `message` (string, 必須): 送信するメッセージの内容。Discordのマークダウン記法が使用できます。

**使用例:**
```json
{
  "name": "discord_send_message",
  "arguments": {
    "message": "AIエージェントが作業を開始しました。"
  }
}
```

## Discord Botの設定

### 1. Discord Developer Portalでアプリケーションを作成

1. [Discord Developer Portal](https://discord.com/developers/applications)にアクセス
2. "New Application"をクリックしてアプリケーションを作成
3. "Bot"セクションでBotを作成
4. Botトークンをコピーして`DISCORD_BOT_TOKEN`に設定

### 2. 必要な権限の設定

Botには以下の権限が必要です：
- `Send Messages` (メッセージの送信)
- `Read Message History` (メッセージ履歴の読み取り)

### 3. サーバーへの招待

OAuth2 URL Generatorを使用してBotをサーバーに招待してください。

### 4. IDの取得方法

#### サーバーIDとチャンネルIDの取得
1. Discordで開発者モードを有効にする（設定 > 詳細設定 > 開発者モード）
2. サーバー名を右クリック → "IDをコピー"でサーバーIDを取得
3. チャンネル名を右クリック → "IDをコピー"でチャンネルIDを取得

#### ユーザーIDの取得
1. ユーザー名を右クリック → "IDをコピー"でユーザーIDを取得

## プロジェクト構造

```
discord-mcp-server/
├── src/
│   └── discord_mcp_server/
│       ├── __init__.py          # パッケージ初期化
│       ├── server.py            # MCPサーバーメイン
│       ├── discord_client.py    # Discord Bot クライアント
│       └── config.py            # 設定管理
├── tests/
│   ├── __init__.py
│   └── test_server.py           # テストファイル
├── .github/
│   └── workflows/
│       └── lint.yml             # GitHub Actions設定
├── pyproject.toml               # プロジェクト設定
├── .ruff.toml                   # Ruff設定
├── .env.example                 # 環境変数設定例
├── .gitignore                   # Git除外設定
└── README.md                    # このファイル
```

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 貢献

プルリクエストやイシューの報告を歓迎します。開発に参加する場合は、まず開発環境を構築し、コード品質チェックを通過することを確認してください。

## トラブルシューティング

### よくある問題

1. **Botがメッセージを送信できない**
   - Botトークンが正しく設定されているか確認
   - Botが対象のサーバーに参加しているか確認
   - 必要な権限が付与されているか確認

2. **環境変数が読み込まれない**
   - `.env`ファイルが正しい場所に配置されているか確認
   - 環境変数名が正しいか確認

3. **型チェックエラー**
   - `uv run mypy src/`でエラーの詳細を確認
   - 必要に応じて型アノテーションを追加

## サポート

問題が発生した場合は、GitHubのIssuesで報告してください。

