from fastmcp import FastMCP

mcp = FastMCP("Robot Controller")

import tools.movement
import tools.head
import tools.expression
import tools.vision

if __name__ == "__main__":
    mcp.run(host="0.0.0.0", port=8000, transport="sse")