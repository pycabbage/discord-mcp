"""
設定管理モジュール
環境変数からDiscord Bot設定を読み込む
"""

from typing import Self

from pydantic import Field, ValidationError, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class DiscordConfig(BaseSettings):
    """Discord Bot設定

    環境変数または.envファイルから設定を読み込みます。
    Pydantic BaseSettingsを使用して、自動的に環境変数をマッピングします。
    """

    model_config = SettingsConfigDict(
        # .envファイルのサポート
        env_file=".env",
        env_file_encoding="utf-8",
        # 大文字小文字を区別しない
        case_sensitive=False,
        # 追加フィールドを禁止
        extra="forbid",
    )

    # Discord Bot Token (必須)
    discord_bot_token: str = Field(
        ...,
        description="Discord Botのアクセストークン",
    )

    # サーバーID (オプション)
    discord_server_id: str | None = Field(
        default=None,
        description="メッセージを送信するDiscordサーバーのID",
    )

    # チャンネルID (オプション)
    discord_channel_id: str | None = Field(
        default=None,
        description="メッセージを送信するチャンネルのID",
    )

    # ユーザーID (オプション)
    discord_user_id: str | None = Field(
        default=None,
        description="DMを送信するユーザーのID",
    )

    @model_validator(mode="after")
    def validate_destination(self) -> Self:
        """送信先設定の妥当性をチェック"""
        # サーバー/チャンネルIDまたはユーザーIDのいずれかが必要
        has_server_channel = self.discord_server_id and self.discord_channel_id
        has_user = self.discord_user_id

        if not (has_server_channel or has_user):
            raise ValueError(
                "メッセージ送信先が設定されていません。\n"
                "以下のいずれかを設定してください：\n"
                "- チャンネル送信: DISCORD_SERVER_ID と DISCORD_CHANNEL_ID\n"
                "- DM送信: DISCORD_USER_ID"
            )

        if has_server_channel and has_user:
            raise ValueError(
                "サーバー/チャンネルIDとユーザーIDの両方が設定されています。\n"
                "どちらか一方のみを設定してください。"
            )

        return self


def get_config() -> DiscordConfig:
    """設定を取得し、妥当性をチェックして返す

    Pydantic BaseSettingsが自動的に以下の順序で設定を読み込みます：
    1. 環境変数
    2. .envファイル（存在する場合）

    Returns:
        DiscordConfig: 検証済みの設定オブジェクト

    Raises:
        ValueError: 必須の設定が不足している場合
    """
    try:
        # Pydanticが自動的に環境変数を読み込み、バリデーションを実行
        return DiscordConfig()  # type: ignore[call-arg]
    except ValidationError as e:
        # Pydanticのバリデーションエラーをユーザーフレンドリーなメッセージに変換
        missing_fields: list[str] = []
        for error in e.errors():
            if error["type"] == "missing":
                field_name = str(error["loc"][0]) if error["loc"] else "unknown"
                missing_fields.append(field_name.upper())

        if "DISCORD_BOT_TOKEN" in missing_fields:
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
    except ValueError:
        # model_validatorからのエラーはそのまま再発生
        raise
