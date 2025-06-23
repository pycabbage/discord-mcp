import click
import logging
import sys
from .server import serve
import asyncio

@click.command()
@click.option("-v", "--verbose", count=True)
def main(verbose: bool) -> None:
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
    logger.info("Starting Discord MCP server")
    
    try:
        asyncio.run(serve())
    except Exception as e:
        logger.error(f"Error running Discord MCP server: {e}")
        raise

if __name__ == "__main__":
    main()
