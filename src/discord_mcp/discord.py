from typing import Any, Callable, Coroutine, Literal, TypeVar
from discord import Client, Intents
from pydantic import BaseModel

from .env import env

T = TypeVar('T')
Coro = Coroutine[Any, Any, T]
CoroT = TypeVar('CoroT', bound=Callable[..., Coro[Any]])

class DiscordClientContainer:
    def __init__(self):
        intents = Intents.default()
        intents.message_content = True
        self.client = Client(intents=intents)

        @self.client.event
        async def on_ready(): # type: ignore
            print(f'logged in as {self.client.user}')

        self.client.run(env.token)

    # def with_client(self, func: CoroT, /) -> CoroT:
    #     async def wrapper(*args, **kwargs): # type: ignore
    #         return await func(self.client, *args, **kwargs)
    #     return wrapper # type: ignore

container = DiscordClientContainer()

class SendMessageResult(BaseModel):
    status: Literal["success", "error"]
    destination: str

async def send_message(content: str) -> SendMessageResult:
    # send message
    # container.client
    return SendMessageResult(status="success", destination="12345678")
