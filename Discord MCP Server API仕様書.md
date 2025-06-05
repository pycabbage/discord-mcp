# Discord MCP Server API仕様書

## 概要

Discord MCP Serverは、Model Context Protocol (MCP) に準拠したサーバーで、Discord Botの機能をMCPツールとして提供します。

## MCPプロトコル仕様

### サーバー情報

- **サーバー名**: `discord-mcp-server`
- **バージョン**: `0.1.0`
- **プロトコル**: MCP 1.0

### 通信方式

- **入力**: stdin
- **出力**: stdout
- **エラー**: stderr

## 提供ツール

### discord_send_message

Discord Botを使用してメッセージを送信するツールです。

#### 基本情報

- **ツール名**: `discord_send_message`
- **説明**: Discord Bot を使用してメッセージを送信します。環境変数で設定されたチャンネルまたはユーザーにメッセージを送信できます。

#### 入力スキーマ

```json
{
  "type": "object",
  "properties": {
    "message": {
      "type": "string",
      "description": "送信するメッセージの内容。Discord のマークダウン記法が使用できます。"
    }
  },
  "required": ["message"]
}
```

#### パラメータ詳細

| パラメータ | 型 | 必須 | 説明 |
|-----------|---|------|------|
| message | string | ✓ | 送信するメッセージの内容。Discordのマークダウン記法（**太字**、*斜体*、`コード`など）が使用可能 |

#### 戻り値

成功時:
```json
{
  "content": [
    {
      "type": "text",
      "text": "Message sent successfully to server 123456789, channel 987654321"
    }
  ],
  "isError": false
}
```

エラー時:
```json
{
  "content": [
    {
      "type": "text", 
      "text": "Error: Discord client is not initialized"
    }
  ],
  "isError": true
}
```

#### 使用例

##### チャンネルへのメッセージ送信

```json
{
  "method": "tools/call",
  "params": {
    "name": "discord_send_message",
    "arguments": {
      "message": "🤖 AIエージェントが作業を開始しました。\n\n**タスク**: データ分析\n**開始時刻**: 2024-01-15 10:30:00"
    }
  }
}
```

##### DMでの通知

```json
{
  "method": "tools/call", 
  "params": {
    "name": "discord_send_message",
    "arguments": {
      "message": "作業が完了しました！\n\n結果は添付ファイルをご確認ください。"
    }
  }
}
```

## 環境変数設定

### 必須設定

#### DISCORD_BOT_TOKEN
- **型**: string
- **説明**: Discord Botのトークン
- **取得方法**: Discord Developer Portalで作成したBotのトークン

### 送信先設定（いずれか一方を選択）

#### サーバーチャンネル送信

##### DISCORD_SERVER_ID
- **型**: string
- **説明**: 送信先サーバー（ギルド）のID
- **取得方法**: サーバー名を右クリック → "IDをコピー"

##### DISCORD_CHANNEL_ID  
- **型**: string
- **説明**: 送信先チャンネルのID
- **取得方法**: チャンネル名を右クリック → "IDをコピー"

#### ユーザーDM送信

##### DISCORD_USER_ID
- **型**: string
- **説明**: 送信先ユーザーのID
- **取得方法**: ユーザー名を右クリック → "IDをコピー"

### 設定例

#### チャンネル送信の場合
```bash
DISCORD_BOT_TOKEN=your_bot_token_here
DISCORD_SERVER_ID=123456789012345678
DISCORD_CHANNEL_ID=987654321098765432
```

#### DM送信の場合
```bash
DISCORD_BOT_TOKEN=your_bot_token_here
DISCORD_USER_ID=111222333444555666
```

## エラーハンドリング

### 一般的なエラー

#### 認証エラー
- **原因**: 無効なBotトークン
- **メッセージ**: "Discord Bot is not ready"
- **対処法**: `DISCORD_BOT_TOKEN`を確認

#### 権限エラー
- **原因**: Botに必要な権限がない
- **メッセージ**: "Bot does not have permission to send messages"
- **対処法**: Botの権限設定を確認

#### 送信先エラー
- **原因**: 指定されたチャンネルやユーザーが見つからない
- **メッセージ**: "Channel not found" / "User not found"
- **対処法**: IDが正しいか確認

#### 設定エラー
- **原因**: 環境変数の設定不備
- **メッセージ**: "Either (DISCORD_SERVER_ID and DISCORD_CHANNEL_ID) or DISCORD_USER_ID must be provided"
- **対処法**: 環境変数の設定を確認

## Discord Botの権限要件

### 必要な権限

| 権限 | 説明 | 必須度 |
|------|------|--------|
| Send Messages | メッセージの送信 | 必須 |
| Read Message History | メッセージ履歴の読み取り | 推奨 |
| Use External Emojis | 外部絵文字の使用 | オプション |
| Embed Links | リンクの埋め込み | オプション |

### 権限の設定方法

1. Discord Developer Portalでアプリケーションを選択
2. "Bot"セクションに移動
3. "Privileged Gateway Intents"で必要なIntentを有効化
4. OAuth2 URL Generatorで適切な権限を選択してBotを招待

## セキュリティ考慮事項

### Botトークンの管理
- Botトークンは機密情報として扱う
- 環境変数やシークレット管理システムを使用
- コードやログにトークンを含めない

### 権限の最小化
- 必要最小限の権限のみを付与
- 定期的に権限の見直しを実施

### ログ管理
- 送信メッセージの内容をログに記録する際は個人情報に注意
- エラーログにトークンが含まれないよう注意

## パフォーマンス

### レート制限
- Discord APIのレート制限に準拠
- 大量のメッセージ送信時は適切な間隔を設ける

### 接続管理
- Bot接続の維持とエラー時の再接続
- 長時間の非アクティブ状態での接続管理

## バージョン履歴

### v0.1.0
- 初回リリース
- 基本的なメッセージ送信機能
- チャンネルとDMの両方に対応
- MCP 1.0プロトコル対応

