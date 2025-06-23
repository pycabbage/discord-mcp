"""Discord メッセージテンプレート管理"""

from typing import TypedDict


class MessageTemplate(TypedDict):
    id: str
    name: str
    description: str
    content: str
    placeholders: list[str]


# プリセットテンプレート
TEMPLATES: list[MessageTemplate] = [
    {
        "id": "greeting",
        "name": "挨拶",
        "description": "基本的な挨拶メッセージ",
        "content": "こんにちは、{name}さん！今日はどのようなご用件でしょうか？",
        "placeholders": ["name"],
    },
    {
        "id": "task_completed",
        "name": "タスク完了通知",
        "description": "タスクが完了したことを通知するメッセージ",
        "content": "✅ タスク「{task_name}」が完了しました！\n処理時間: {duration}\n結果: {result}",
        "placeholders": ["task_name", "duration", "result"],
    },
    {
        "id": "error_notification",
        "name": "エラー通知",
        "description": "エラーが発生したことを通知するメッセージ",
        "content": "⚠️ エラーが発生しました\nエラー内容: {error_message}\n発生場所: {location}\n時刻: {timestamp}",
        "placeholders": ["error_message", "location", "timestamp"],
    },
    {
        "id": "reminder",
        "name": "リマインダー",
        "description": "リマインダーメッセージ",
        "content": "🔔 リマインダー: {title}\n内容: {description}\n期限: {due_date}",
        "placeholders": ["title", "description", "due_date"],
    },
    {
        "id": "progress_update",
        "name": "進捗更新",
        "description": "作業の進捗を報告するメッセージ",
        "content": "📊 進捗報告\nタスク: {task_name}\n進捗率: {progress}%\n残り時間: {remaining_time}",
        "placeholders": ["task_name", "progress", "remaining_time"],
    },
]


def get_templates() -> list[MessageTemplate]:
    """利用可能なテンプレートのリストを取得"""
    return TEMPLATES


def get_template_by_id(template_id: str) -> MessageTemplate | None:
    """IDでテンプレートを取得"""
    for template in TEMPLATES:
        if template["id"] == template_id:
            return template
    return None
