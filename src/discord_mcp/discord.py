import asyncio
import logging
from typing import Any, Callable, Coroutine, Literal, TypeVar
from discord import Client, Forbidden, Intents, VoiceClient
from discord.http import Route
from pydantic import BaseModel

VoiceClient.warn_nacl = False

from .env import env

T = TypeVar('T')
Coro = Coroutine[Any, Any, T]
CoroT = TypeVar('CoroT', bound=Callable[..., Coro[Any]])

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
        async def on_ready(): # type: ignore
            logger.info(f'Logged in as {self.client.user}')
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

class SendMessageResult(BaseModel):
    status: Literal["success", "error"]
    destination: str

async def send_message(content: str, retry_count: int = 0) -> SendMessageResult:
    # Make sure client is ready
    if not container.ready.is_set():
        try:
            await container.start()
        except Exception as e:
            logger.error(f"Failed to start Discord client: {e}")
            return SendMessageResult(status="error", destination=f"Failed to initialize Discord client: {e}")

    try:
        user = await container.client.fetch_user(int(env.user_id))
        if not user:
            return SendMessageResult(status="error", destination=f"User {env.user_id} not found")
        logger.info(f"Sending message to user {env.user_id}: {content}")

        channel = user.dm_channel
        if channel is None:
            logger.info(f"Creating DM channel with user {env.user_id}")
            channel = await user.create_dm()
        if not channel:
            return SendMessageResult(status="error", destination=f"Failed to create DM channel with user {env.user_id}")
        logger.info(f"DM channel: {channel}")

        try:
            await channel.send(content)
        except Forbidden as e:
            # send friend request
            await container.client.http.request(
                Route(
                    "PUT",
                    "/users/@me/relationships/{user_id}",
                    user_id=env.user_id
                ),
                # context_properties=0,
                # payload={}
            )
            if retry_count >= 3:
                logger.error(f"Failed to send message after 3 retries: {e}")
                return SendMessageResult(status="error", destination=f"Failed to send message: {e}")
            return await send_message(content, retry_count + 1)

        return SendMessageResult(status="success", destination=f"DM to user {env.user_id}")
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        return SendMessageResult(status="error", destination=str(e))
