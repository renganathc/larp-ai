from mcp_instance import mcp

def log(action):
    print(f"[HEAD] {action}")

@mcp.tool()
def head_up():
    """Move robot head upward"""
    log("up")
    return {"status": "head up"}

@mcp.tool()
def head_down():
    """Move robot head downward"""
    log("down")
    return {"status": "head down"}

@mcp.tool()
def head_center():
    """Center the robot head"""
    log("center")
    return {"status": "head centered"}

@mcp.tool()
def nod_yes():
    """Make the robot nod yes"""
    log("nod yes")
    return {"status": "nodded yes"}