from enum import Enum
from pydantic import BaseModel, Field


class DiscordTools(str, Enum):
    SEND_MESSAGE = "send_message"
    ASK_TO_USER = "ask_to_user"

class DiscordSendMessage(BaseModel):
    content: str = Field(..., description="The content of the message to send")

class DiscordAskToUser(BaseModel):
    content: str = Field(..., description="The content of the message to send to the user")
    timeout_seconds: int = Field(
        default=60,
        description="The timeout in seconds for waiting for a response",
        ge=1,  # Ensure timeout is at least 1 second
        le=3600  # Ensure timeout does not exceed 1 hour
    )
