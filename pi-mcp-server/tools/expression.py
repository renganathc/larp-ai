from mcp_instance import mcp

def log(expression):
    print(f"[EYES] {expression}")

@mcp.tool()
def happy_eyes():
    """Display happy eyes"""
    log("happy")
    return {"emotion": "happy"}

@mcp.tool()
def anger_eyes():
    """Display angry eyes"""
    log("angry")
    return {"emotion": "angry"}

@mcp.tool()
def sad_eyes():
    """Display sad eyes"""
    log("sad")
    return {"emotion": "sad"}

@mcp.tool()
def cute_eyes():
    """Display cute eyes"""
    log("cute")
    return {"emotion": "cute"}