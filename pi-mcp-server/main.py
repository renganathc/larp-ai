from fastmcp import FastMCP
from mcp_instance import mcp

import tools.movement
import tools.head
import tools.expression
import tools.vision

@mcp.tool()
def turn_left():
    """Turn the robot left"""
    return {"status": "turning left"}

if __name__ == "__main__":
    mcp.run(host="0.0.0.0", port=8000, transport="sse")