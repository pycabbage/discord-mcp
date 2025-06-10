import logging

from mcp import stdio_server
from mcp.server import Server
from mcp.types import (
    TextContent,
    Tool,
)

from .models import DiscordTools, DiscordSendMessage
from .discord import send_message

async def serve():
    logger = logging.getLogger(__name__)

    server = Server(
        "discord-mcp",
        "0.1.0",
        "A Discord bot that sends messages"
    )
    @server.list_tools()
    async def list_tools() -> list[Tool]: # type: ignore
        return [
            Tool(
                name=DiscordTools.SEND_MESSAGE,
                description="Send a message to a Discord channel / DM",
                inputSchema=DiscordSendMessage.model_json_schema(),
            )
        ]
    
    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]: # type: ignore
        match name:
            case DiscordTools.SEND_MESSAGE:
                args = DiscordSendMessage(**arguments) # type: ignore
                status = await send_message(args.content)
                if status.status == "error":
                    logger.error(f"Failed to send message: {status.destination}")
                    return [
                        TextContent(
                            type="text",
                            text=f"Error sending message to {status.destination}"
                        )
                    ]
                return [
                    TextContent(
                        type="text",
                        text=f"Sending message to {status.destination} success"
                    )
                ]
            case _:
                raise ValueError(f"Unknown tool: {name}")

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options, raise_exceptions=True)
