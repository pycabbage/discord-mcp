"""
設定管理モジュール
環境変数からDiscord Bot設定を読み込む
"""

from pydantic import Field, ValidationError
from pydantic_settings import BaseSettings


class DiscordConfig(BaseSettings):
    """Discord Bot設定"""

    # Discord Bot Token (必須)
    discord_bot_token: str = Field(..., env="DISCORD_BOT_TOKEN")

    # サーバーID (オプション)
    discord_server_id: str | None = Field(None, env="DISCORD_SERVER_ID")

    # チャンネルID (オプション)
    discord_channel_id: str | None = Field(None, env="DISCORD_CHANNEL_ID")

    # ユーザーID (オプション)
    discord_user_id: str | None = Field(None, env="DISCORD_USER_ID")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    def validate_config(self) -> None:
        """設定の妥当性をチェック"""
        if not self.discord_bot_token:
            raise ValueError("DISCORD_BOT_TOKEN is required")

        # サーバー/チャンネルIDまたはユーザーIDのいずれかが必要
        has_server_channel = self.discord_server_id and self.discord_channel_id
        has_user = self.discord_user_id

        if not (has_server_channel or has_user):
            raise ValueError(
                "Either (DISCORD_SERVER_ID and DISCORD_CHANNEL_ID) "
                "or DISCORD_USER_ID must be provided"
            )

        if has_server_channel and has_user:
            raise ValueError(
                "Cannot specify both server/channel and user ID. Choose one."
            )


def get_config() -> DiscordConfig:
    """設定を取得し、妥当性をチェックして返す"""
    try:
        config = DiscordConfig()  # type: ignore[call-arg]
        config.validate_config()
        return config
    except ValidationError as e:
        # Pydanticのバリデーションエラーをユーザーフレンドリーなメッセージに変換
        missing_fields = []
        for error in e.errors():
            if error["type"] == "missing":
                field_name = error["loc"][0] if error["loc"] else "unknown"
                missing_fields.append(field_name)

        if "discord_bot_token" in missing_fields:
            raise ValueError(
                "環境変数 DISCORD_BOT_TOKEN が設定されていません。\n"
                "Discord Bot のトークンを設定してください。\n"
                "詳細はREADME.mdを参照してください。"
            ) from e
        else:
            raise ValueError(
                f"必須の環境変数が設定されていません: {', '.join(missing_fields)}\n"
                "詳細はREADME.mdを参照してください。"
            ) from e
    except ValueError as e:
        # validate_config() からのエラーはそのまま再発生
        if "Either (DISCORD_SERVER_ID and DISCORD_CHANNEL_ID)" in str(e):
            raise ValueError(
                "メッセージ送信先が設定されていません。\n"
                "以下のいずれかを設定してください：\n"
                "- チャンネル送信: DISCORD_SERVER_ID と DISCORD_CHANNEL_ID\n"
                "- DM送信: DISCORD_USER_ID\n"
                "詳細はREADME.mdを参照してください。"
            ) from e
        else:
            raise
