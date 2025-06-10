from typing import Literal
from pydantic import BaseModel


class SendMessageResult(BaseModel):
    status: Literal["success", "error"]
    destination: str

async def send_message(content: str) -> SendMessageResult:
    return SendMessageResult(status="success", destination="12345678")
