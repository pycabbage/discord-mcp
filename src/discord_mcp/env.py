import os
import logging
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)


class Environment(BaseSettings):
    token: str = ""
    user_id: str = ""

    model_config = SettingsConfigDict(env_prefix="discord_")

    def __init__(self):
        # .envファイルの存在を確認
        env_file = ".env"
        if os.path.exists(env_file):
            logger.info(f".envファイルが見つかりました: {env_file}")
            super().__init__(_env_file=env_file, _env_file_encoding="utf-8")
        else:
            logger.info(
                ".envファイルが見つかりません。環境変数から設定を読み込みます。"
            )
            super().__init__()

        # 必須の環境変数のチェック
        if not self.token:
            raise ValueError(
                "Discord bot token is not set. Please set the DISCORD_TOKEN environment variable."
            )
        if not self.user_id:
            raise ValueError(
                "Discord user ID is not set. Please set the DISCORD_USER_ID environment variable."
            )


env = Environment()
