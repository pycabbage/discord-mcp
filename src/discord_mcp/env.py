from pydantic_settings import BaseSettings, SettingsConfigDict

class Environment(BaseSettings):
    token: str = ""
    user_id: str = ""

    model_config = SettingsConfigDict(env_prefix='discord_')

    def __init__(self):
        super().__init__(_env_file='.env', _env_file_encoding='utf-8')
        if not self.token:
            raise ValueError("Discord bot token is not set. Please set the DISCORD_TOKEN environment variable.")
        if not self.user_id:
            raise ValueError("Discord user ID is not set. Please set the DISCORD_USER_ID environment variable.")

env = Environment()
