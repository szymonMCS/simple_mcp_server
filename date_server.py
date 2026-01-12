from mcp.server.fastmcp import FastMCP
from date import GetDateInput

mcp = FastMCP("date_mcp")

@mcp.tool()
async def get_current_date(format: str = "%Y-%m-%d") -> str:
    """Gets the current date in the specified format.

    Args:
        format: Date format string (strftime format).
                Examples: '%Y-%m-%d' for '2025-01-08',
                         '%B %d, %Y' for 'January 08, 2025',
                         '%d/%m/%Y' for '08/01/2025'

    Returns:
        str: Formatted date
    """
    date_input = GetDateInput(format=format)
    return date_input.get_current_date()

if __name__ == "__main__":
    mcp.run()
