from instances import mcp
from anim_eyes.utils.moods_utils import DEFAULT, SAD, CUTE, ANGRY
import threading
import sys
import hardware.shared as shared


def log(msg):
    print(f"[EYES] {msg}", file=sys.stderr)


def get_eyes():
    if shared.eyes is None:
        raise RuntimeError("Eyes not initialized yet")
    return shared.eyes


reset_timer = None

def reset_after_delay(delay=16):
    global reset_timer

    if reset_timer:
        reset_timer.cancel()

    def reset():
        get_eyes().set_mood(DEFAULT)
        log("reset to default")

    reset_timer = threading.Timer(delay, reset)
    reset_timer.start()


#@mcp.tool()
def happy_eyes():
    log("happy")
    get_eyes().set_mood(CUTE)
    reset_after_delay()
    return {"emotion": "happy"}


#@mcp.tool()
def anger_eyes():
    log("angry")
    get_eyes().set_mood(ANGRY)
    reset_after_delay()
    return {"emotion": "angry"}


#@mcp.tool()
def sad_eyes():
    log("sad")
    get_eyes().set_mood(SAD)
    reset_after_delay()
    return {"emotion": "sad"}

@mcp.tool()
def default_eyes():
    log("default")
    get_eyes().set_mood(DEFAULT)
    reset_after_delay()
    return {"emotion": "default"}