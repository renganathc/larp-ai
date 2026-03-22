from instances import mcp
import hardware.servos as servos



def log(action):
    print(f"[HEAD] {action}")



@mcp.tool()
def head_up():
    """Move robot head upward"""
    log("up")
    servos.head_up()
    return {"status": "head up"}

@mcp.tool()
def head_down():
    """Move robot head downward"""
    log("down")
    servos.head_down()
    return {"status": "head down"}

@mcp.tool()
def head_left():
    """Move robot head left"""
    log("left")
    servos.head_left()
    return {"status": "head left"}

@mcp.tool()
def head_right():
    """Move robot head right"""
    log("right")
    servos.head_right()
    return {"status": "head right"}



@mcp.tool()
def head_center():
    """Center the robot head"""
    log("center")
    servos.head_center()
    return {"status": "head centered"}




@mcp.tool()
def nod_yes():
    """Make the robot nod yes"""
    log("nod yes")
    servos.nod_yes()
    return {"status": "nodded yes"}

@mcp.tool()
def nod_no():
    """Make the robot nod no"""
    log("nod no")
    servos.nod_no()
    return {"status": "nodded no"}