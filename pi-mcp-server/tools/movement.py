from mcp_instance import mcp

def log(action):
    print(f"[MOVEMENT] {action}")

@mcp.tool()
def move_forward():
    """Move the robot forward"""
    log("forward")
    return {"status": "moving forward"}

@mcp.tool()
def move_backward():
    """Move the robot backward"""
    log("backward")
    return {"status": "moving backward"}

@mcp.tool()
def turn_left():
    """Turn the robot left"""
    log("left")
    return {"status": "turning left"}

@mcp.tool()
def turn_right():
    """Turn the robot right"""
    log("right")
    return {"status": "turning right"}

@mcp.tool()
def turn_180():
    """Turn the robot 180 degrees"""
    log("180 turn")
    return {"status": "turning 180"}

@mcp.tool()
def turn_360():
    """Turn the robot 360 degrees"""
    log("360 turn")
    return {"status": "turning 360"}