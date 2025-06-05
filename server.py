"""
MCP サーバーメインモジュール
Discord Bot メッセージ送信機能を提供するMCPサーバー
"""
import asyncio
import logging

from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    TextContent,
    Tool,
)
from pydantic import BaseModel

from .config import DiscordConfig, get_config
from .discord_client import DiscordClient

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SendMessageArgs(BaseModel):
    """discord_send_message ツールの引数"""
    message: str


class DiscordMCPServer:
    """Discord MCP サーバー"""

    def __init__(self) -> None:
        self.server: Server = Server("discord-mcp-server")
        self.config: DiscordConfig | None = None
        self.discord_client: DiscordClient | None = None

        # ツールハンドラーを登録
        self.server.list_tools = self.list_tools  # type: ignore[assignment]
        self.server.call_tool = self.call_tool  # type: ignore[assignment]

    async def initialize(self) -> None:
        """サーバーを初期化"""
        try:
            # 設定を読み込み
            self.config = get_config()
            logger.info("Configuration loaded successfully")

            # Discord クライアントを初期化
            self.discord_client = DiscordClient(self.config)
            await self.discord_client.initialize()
            logger.info("Discord client initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize server: {e}")
            raise

    async def list_tools(self, request: ListToolsRequest) -> ListToolsResult:
        """利用可能なツールのリストを返す"""
        tools = [
            Tool(
                name="discord_send_message",
                description=(
                    "Discord Bot を使用してメッセージを送信します。"
                    "環境変数で設定されたチャンネルまたはユーザーにメッセージを送信できます。"
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": (
                                "送信するメッセージの内容。"
                                "Discord のマークダウン記法が使用できます。"
                            ),
                        }
                    },
                    "required": ["message"],
                },
            )
        ]
        return ListToolsResult(tools=tools)

    async def call_tool(self, request: CallToolRequest) -> CallToolResult:
        """ツールを実行"""
        if request.params.name == "discord_send_message":
            return await self._handle_send_message(request)
        else:
            raise ValueError(f"Unknown tool: {request.params.name}")

    async def _handle_send_message(self, request: CallToolRequest) -> CallToolResult:
        """discord_send_message ツールを処理"""
        try:
            # 引数を検証
            args = SendMessageArgs(**request.params.arguments or {})

            if not self.discord_client:
                return CallToolResult(
                    content=[
                        TextContent(
                            type="text",
                            text="Error: Discord client is not initialized"
                        )
                    ],
                    isError=True
                )

            # メッセージを送信
            success = await self.discord_client.send_message(args.message)

            if success:
                target_info = ""
                if (
                    self.config
                    and self.config.discord_server_id
                    and self.config.discord_channel_id
                ):
                    target_info = (
                        f"server {self.config.discord_server_id}, "
                        f"channel {self.config.discord_channel_id}"
                    )
                elif self.config and self.config.discord_user_id:
                    target_info = f"user {self.config.discord_user_id} (DM)"

                return CallToolResult(
                    content=[
                        TextContent(
                            type="text",
                            text=f"Message sent successfully to {target_info}"
                        )
                    ]
                )
            else:
                return CallToolResult(
                    content=[
                        TextContent(
                            type="text",
                            text="Failed to send message. Check logs for details."
                        )
                    ],
                    isError=True
                )

        except Exception as e:
            logger.error(f"Error in discord_send_message: {e}")
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"Error: {e!s}"
                    )
                ],
                isError=True
            )

    async def run(self) -> None:
        """サーバーを実行"""
        await self.initialize()

        # MCP サーバーを開始
        from mcp.server.stdio import stdio_server

        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="discord-mcp-server",
                    server_version="0.1.0",
                    capabilities=self.server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={}
                    )
                )
            )

    async def close(self) -> None:
        """サーバーを終了"""
        if self.discord_client:
            await self.discord_client.close()


async def main() -> None:
    """メイン関数"""
    server = DiscordMCPServer()
    try:
        await server.run()
    except KeyboardInterrupt:
        logger.info("Server interrupted by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise
    finally:
        await server.close()


if __name__ == "__main__":
    asyncio.run(main())

