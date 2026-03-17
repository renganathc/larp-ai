from fastmcp import FastMCP

mcp = FastMCP("Robot Controller")

if __name__ == "__main__":
    mcp.run(transport="sse")