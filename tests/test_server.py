# テスト用の設定では、セキュリティ警告を無視
# ruff: noqa: S106

"""
Discord MCP Server のテスト
"""
import pytest

from discord_mcp_server.config import DiscordConfig
from discord_mcp_server.discord_client import DiscordClient
from discord_mcp_server.server import DiscordMCPServer, SendMessageArgs


class TestDiscordConfig:
    """DiscordConfig のテスト"""

    def test_valid_server_channel_config(self):
        """サーバー/チャンネル設定のテスト"""
        config = DiscordConfig(
            discord_bot_token="test_token",
            discord_server_id="123456789",
            discord_channel_id="987654321",
            discord_user_id=None,
        )
        config.validate_config()  # 例外が発生しないことを確認

    def test_valid_user_config(self):
        """ユーザー設定のテスト"""
        config = DiscordConfig(
            discord_bot_token="test_token",
            discord_user_id="123456789",
            discord_channel_id=None,
            discord_server_id=None,
        )
        config.validate_config()  # 例外が発生しないことを確認

    def test_missing_token(self):
        """トークン未設定のテスト"""
        from pydantic import ValidationError
        
        with pytest.raises(ValidationError):  # Pydanticのバリデーションエラーをキャッチ
            config = DiscordConfig(
                discord_bot_token=None,
                discord_user_id=None,
                discord_channel_id=None,
                discord_server_id=None,
            )
            config.validate_config()

    def test_missing_target(self):
        """送信先未設定のテスト"""
        with pytest.raises(ValueError, match="Either .* must be provided"):
            config = DiscordConfig(
                discord_bot_token="test_token",
                discord_user_id=None,
                discord_channel_id=None,
                discord_server_id=None,
            )
            config.validate_config()

    def test_conflicting_targets(self):
        """送信先重複設定のテスト"""
        with pytest.raises(ValueError, match="Cannot specify both"):
            config = DiscordConfig(
                discord_bot_token="test_token",
                discord_server_id="123",
                discord_channel_id="456",
                discord_user_id="789",
            )
            config.validate_config()


class TestSendMessageArgs:
    """SendMessageArgs のテスト"""

    def test_valid_args(self):
        """有効な引数のテスト"""
        args = SendMessageArgs(message="Hello, World!")
        assert args.message == "Hello, World!"

    def test_empty_message(self):
        """空メッセージのテスト"""
        args = SendMessageArgs(message="")
        assert args.message == ""


@pytest.mark.asyncio
class TestDiscordClient:
    """DiscordClient のテスト"""

    async def test_initialization(self):
        """初期化のテスト"""
        config = DiscordConfig(
            discord_bot_token="test_token",
            discord_user_id="123456789",
            discord_channel_id=None,
            discord_server_id=None,
        )
        client = DiscordClient(config)
        assert client.config == config
        assert client.bot is None


@pytest.mark.asyncio
class TestDiscordMCPServer:
    """DiscordMCPServer のテスト"""

    async def test_list_tools(self):
        """ツールリストのテスト"""
        server = DiscordMCPServer()

        from mcp.types import ListToolsRequest

        request = ListToolsRequest(method="tools/list")

        result = await server.list_tools(request)

        assert len(result.tools) == 1
        assert result.tools[0].name == "discord_send_message"
        assert result.tools[0].description is not None
        assert "Discord Bot" in result.tools[0].description
        assert "message" in result.tools[0].inputSchema["properties"]
