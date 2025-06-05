"""
Discord クライアントモジュール
Discord Bot の認証とメッセージ送信機能を提供
"""

import asyncio
import logging

import discord
from discord.ext import commands

from .config import DiscordConfig

logger = logging.getLogger(__name__)


class DiscordClient:
    """Discord Bot クライアント"""

    def __init__(self, config: DiscordConfig):
        self.config = config
        self.bot: commands.Bot | None = None
        self._ready = False

    async def initialize(self) -> None:
        """Discord Bot を初期化"""
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.members = True

        self.bot = commands.Bot(command_prefix="!", intents=intents)

        @self.bot.event
        async def on_ready() -> None:
            if self.bot and self.bot.user:
                logger.info(f"Discord Bot logged in as {self.bot.user}")
            self._ready = True

        # Bot を起動
        await self.bot.login(self.config.discord_bot_token)

        # 非同期でBotを開始
        task = asyncio.create_task(self.bot.connect())
        # タスクの参照を保持(RUF006対応)
        self._connect_task = task

        # Bot が準備完了するまで待機
        while not self._ready:
            await asyncio.sleep(0.1)

    async def send_message(self, content: str) -> bool:
        """
        メッセージを送信

        Args:
            content: 送信するメッセージ内容

        Returns:
            bool: 送信成功時True、失敗時False
        """
        if not self.bot or not self._ready:
            logger.error("Discord Bot is not ready")
            return False

        try:
            # サーバー/チャンネルへの送信
            if self.config.discord_server_id and self.config.discord_channel_id:
                guild = self.bot.get_guild(int(self.config.discord_server_id))
                if not guild:
                    logger.error(f"Guild not found: {self.config.discord_server_id}")
                    return False

                channel = guild.get_channel(int(self.config.discord_channel_id))
                if not channel or not hasattr(channel, "send"):
                    logger.error(
                        f"Channel not found or not text channel: "
                        f"{self.config.discord_channel_id}"
                    )
                    return False

                await channel.send(content)
                logger.info(f"Message sent to channel {self.config.discord_channel_id}")
                return True

            # ユーザーへのDM送信
            elif self.config.discord_user_id:
                user = self.bot.get_user(int(self.config.discord_user_id))
                if not user:
                    # ユーザーがキャッシュにない場合はfetchを試行
                    try:
                        user = await self.bot.fetch_user(
                            int(self.config.discord_user_id)
                        )
                    except discord.NotFound:
                        logger.error(f"User not found: {self.config.discord_user_id}")
                        return False

                await user.send(content)
                logger.info(f"DM sent to user {self.config.discord_user_id}")
                return True

            else:
                logger.error("No valid target configured for message sending")
                return False

        except discord.Forbidden:
            logger.error("Bot does not have permission to send messages")
            return False
        except discord.HTTPException as e:
            logger.error(f"HTTP error while sending message: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error while sending message: {e}")
            return False

    async def close(self) -> None:
        """Discord Bot を終了"""
        if self.bot:
            await self.bot.close()
            self._ready = False
