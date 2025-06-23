import click
import logging

from discord_mcp.models import ServerType
from .server import serve
import asyncio


@click.command()
@click.option("-v", "--verbose", count=True)
@click.option(
    "-t",
    "--type",
    type=ServerType,
    default=ServerType.STDIO,
    help="Type of server to run",
)
@click.option(
    "-p",
    "--port",
    type=int,
    default=8080,
    help="Port number for SSE or HTTP server (default: 8080)",
)
def main(verbose: bool, type: ServerType, port: int) -> None:
    """MCP Discord Bot Server."""

    logging_level = logging.WARN
    if verbose == 1:
        logging_level = logging.INFO
    elif verbose >= 2:
        logging_level = logging.DEBUG

    logging.basicConfig(
        level=logging_level,
        format="[%(asctime)s] [%(levelname)-5s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        # stream=sys.stderr,
        filename="discord_mcp.log",
    )

    logger = logging.getLogger(__name__)
    logger.info(f"Starting Discord MCP server with type={type.value}, port={port}")

    try:
        asyncio.run(serve(type, port=port))
    except Exception as e:
        logger.error(f"Error running Discord MCP server: {e}")
        raise


if __name__ == "__main__":
    main()
