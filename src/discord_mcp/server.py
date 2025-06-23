import logging

from mcp import stdio_server
from mcp.server import Server
from mcp.types import (
    TextContent,
    Tool,
)

from .models import DiscordTools, DiscordSendMessage, DiscordAskToUser
from .discord import send_message, ask_to_user, container

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
        ),
        Tool(
            name=DiscordTools.ASK_TO_USER,
            description="Send a message to a user and wait for their response",
            inputSchema=DiscordAskToUser.model_json_schema(),
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
                        text=f"Error sending message: {status.destination}"
                    )
                ]
            return [
                TextContent(
                    type="text",
                    
                    text=f"Message sent to {status.destination} successfully"
                )
            ]
        case DiscordTools.ASK_TO_USER:
            args = DiscordAskToUser(**arguments) # type: ignore
            result = await ask_to_user(args.content, args.timeout_seconds)
            if result.status == "error":
                logger.error(f"Failed to ask user: {result.destination}")
                return [
                    TextContent(
                        type="text",
                        text=f"Error asking user: {result.destination}"
                    )
                ]
            elif result.status == "timeout":
                return [
                    TextContent(
                        type="text",
                        text=f"Timeout: {result.destination}"
                    )
                ]
            return [
                TextContent(
                    type="text",
                    text=f"User response: {result.response}"
                )
            ]
        case _:
            raise ValueError(f"Unknown tool: {name}")

async def initialize():
    # Initialize Discord client but don't block
    try:
        await container.setup()
        logger.info("Discord client initialized")
    except Exception as e:
        logger.error(f"Error initializing Discord client: {e}")

async def serve():
    # Initialize Discord without blocking
    await initialize()

    # Run MCP server
    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options, raise_exceptions=True)
