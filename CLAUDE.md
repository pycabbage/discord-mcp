# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 開発環境設定

このプロジェクトはuvを使用してPython依存関係を管理しています：

```bash
# 開発環境セットアップ
uv sync --group dev

# サーバー実行（開発時）
uv run discord-mcp-server

# リンタリング
uv run ruff check
uv run ruff format

# 型チェック
uv run mypy src/

# テスト実行  
uv run pytest
```

## アーキテクチャ

このプロジェクトはModel Context Protocol (MCP) サーバーとして動作し、Discord Bot経由でメッセージ送信機能を提供します。

### 主要コンポーネント

- **config.py**: 環境変数からDiscord Bot設定を読み込み、設定バリデーションを実行
- **discord_client.py**: Discord.py ライブラリを使用したBot認証とメッセージ送信機能
- **server.py**: MCPプロトコルサーバー実装、`discord_send_message`ツールを提供

### 設定パターン

プロジェクトは2つのメッセージ送信モードをサポート：

1. サーバーチャンネル送信: `DISCORD_SERVER_ID` + `DISCORD_CHANNEL_ID`
2. ユーザーDM送信: `DISCORD_USER_ID`

どちらか一方を設定する必要があり、両方同時設定は不可。

### エラーハンドリング

設定エラーは日本語のユーザーフレンドリーなメッセージで表示され、適切なSetup手順へ誘導されます。

## コーディング規約

- 全ての文字列、コメント、エラーメッセージは日本語で記述
- Ruff設定に従ったコードフォーマット（88文字行長、ダブルクォート使用）
- 完全な型アノテーション必須（mypy strict設定）
- async/await パターンの一貫使用
