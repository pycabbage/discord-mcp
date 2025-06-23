import asyncio
import logging
from typing import (
    Any,
    Callable,
    Coroutine,
    Literal,
    TypeVar,
    Optional,
    Union,
    TypedDict,
)
from discord import Client, Intents, VoiceClient, Message
from pydantic import BaseModel
from datetime import datetime

from .env import env

VoiceClient.warn_nacl = False

T = TypeVar("T")
Coro = Coroutine[Any, Any, T]
CoroT = TypeVar("CoroT", bound=Callable[..., Coro[Any]])

logger = logging.getLogger(__name__)


class DiscordClientContainer:
    def __init__(self):
        self.client: Client
        self.ready = asyncio.Event()

    async def setup(self):
        # if self.client is not None:
        #     return

        intents = Intents.default()
        intents.message_content = True
        self.client = Client(intents=intents)

        @self.client.event
        async def on_ready():  # type: ignore
            logger.info(f"Logged in as {self.client.user}")
            self.ready.set()

    async def start(self):
        await self.setup()
        if not self.client:
            raise RuntimeError("Discord client not initialized")

        # Start the client in a background task
        loop = asyncio.get_event_loop()
        loop.create_task(self._run_client())

        # Wait for the client to be ready
        await self.ready.wait()

    async def _run_client(self):
        if not self.client:
            raise RuntimeError("Discord client not initialized")
        try:
            await self.client.start(env.token)
        except Exception as e:
            logger.error(f"Error running Discord client: {e}")


container = DiscordClientContainer()


class SendMessageResultSuccess(BaseModel):
    status: Literal["success"]
    destination: str
    created_at: datetime


class SendMessageResultError(BaseModel):
    status: Literal["error"]
    destination: str


SendMessageResult = Union[SendMessageResultSuccess, SendMessageResultError]


class AskToUserResult(BaseModel):
    status: Literal["success", "error", "timeout"]
    response: Optional[str] = None
    destination: str


async def send_message(content: str, retry_count: int = 0) -> SendMessageResult:
    # Make sure client is ready
    if not container.ready.is_set():
        try:
            await container.start()
        except Exception as e:
            logger.error(f"Failed to start Discord client: {e}")
            return SendMessageResultError(
                status="error", destination=f"Failed to initialize Discord client: {e}"
            )

    try:
        user = await container.client.fetch_user(int(env.user_id))
        if not user:
            return SendMessageResultError(
                status="error", destination=f"User {env.user_id} not found"
            )
        logger.info(f"Sending message to user {env.user_id}: {content}")

        channel = user.dm_channel
        if channel is None:
            logger.info(f"Creating DM channel with user {env.user_id}")
            channel = await user.create_dm()
        if not channel:
            return SendMessageResultError(
                status="error",
                destination=f"Failed to create DM channel with user {env.user_id}",
            )
        logger.info(f"DM channel: {channel}")

        sent_message = await channel.send(content)
        return SendMessageResultSuccess(
            status="success",
            destination=f"DM to user {env.user_id}",
            created_at=sent_message.created_at,
        )
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        return SendMessageResultError(status="error", destination=str(e))


async def ask_to_user(content: str, timeout_seconds: int = 60) -> AskToUserResult:
    # まずメッセージを送信
    send_result = await send_message(content)
    if send_result.status == "error":
        return AskToUserResult(status="error", destination=send_result.destination)

    # 返答を待つ
    try:
        user_id = int(env.user_id)

        def check_message(message: Message) -> bool:
            # DMチャンネルで、対象ユーザーからのメッセージかチェック
            # かつ、送信後のメッセージのみを受け付ける
            return (
                message.author.id == user_id
                and hasattr(message.channel, "type")
                and str(message.channel.type) == "private"
                and not message.author.bot
                and message.created_at > send_result.created_at
            )

        # wait_forを使用して返答を待つ
        try:
            response_message = await asyncio.wait_for(
                container.client.wait_for("message", check=check_message),
                timeout=timeout_seconds,
            )
            if response_message.content.startswith("Error "):
                return AskToUserResult(
                    status="error",
                    response=response_message.content,
                    destination=f"DM from user {env.user_id}",
                )
            return AskToUserResult(
                status="success",
                response=response_message.content,
                destination=f"DM from user {env.user_id}",
            )
        except asyncio.TimeoutError:
            return AskToUserResult(
                status="timeout",
                destination=f"Timeout waiting for response from user {env.user_id} after {timeout_seconds} seconds",
            )
    except Exception as e:
        logger.error(f"Error waiting for user response: {e}")
        return AskToUserResult(status="error", destination=str(e))


class MessageHistoryItem(TypedDict):
    id: str
    author: str
    author_id: str
    content: str
    created_at: str
    is_bot: bool


async def get_dm_message_history(limit: int = 10) -> list[MessageHistoryItem]:
    """DMチャンネルのメッセージ履歴を取得する"""
    # Make sure client is ready
    if not container.ready.is_set():
        try:
            await container.start()
        except Exception as e:
            logger.error(f"Failed to start Discord client: {e}")
            return []

    try:
        user = await container.client.fetch_user(int(env.user_id))
        if not user:
            logger.error(f"User {env.user_id} not found")
            return []

        channel = user.dm_channel
        if channel is None:
            logger.info(f"Creating DM channel with user {env.user_id}")
            channel = await user.create_dm()
        if not channel:
            logger.error(f"Failed to create DM channel with user {env.user_id}")
            return []

        # メッセージ履歴を取得
        messages: list[MessageHistoryItem] = []
        async for message in channel.history(limit=limit):
            messages.append(
                MessageHistoryItem(
                    id=str(message.id),
                    author=message.author.name,
                    author_id=str(message.author.id),
                    content=message.content,
                    created_at=message.created_at.isoformat(),
                    is_bot=message.author.bot,
                )
            )

        # 古い順にソート
        messages.reverse()
        return messages

    except Exception as e:
        logger.error(f"Error getting message history: {e}")
        return []
