from enum import Enum
from pydantic import BaseModel


class DiscordTools(str, Enum):
    SEND_MESSAGE = "send_message"

class DiscordSendMessage(BaseModel):
    content: str
