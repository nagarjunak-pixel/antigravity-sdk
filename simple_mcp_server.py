# A simple MCP server using the mcp SDK
from mcp.server.fastmcp import FastMCP

# Create the MCP server instance
mcp = FastMCP("MathServer")

@mcp.tool()
def multiply_numbers(x: int, y: int) -> int:
    """Multiplies two integers and returns the result.

    Args:
        x: First integer.
        y: Second integer.
    """
    return x * y

@mcp.tool()
def format_message(message: str) -> str:
    """Formats a message in all uppercase.

    Args:
        message: The string message to format.
    """
    return f"*** {message.upper()} ***"

if __name__ == "__main__":
    mcp.run()
