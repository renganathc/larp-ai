from instances import mcp
from hardware.eye_disp_runner import start
from anim_eyes.utils.moods_utils import DEFAULT, SAD, EXCITED, ANGRY
import threading

eyes = start()


def log(expression):
    print(f"[EYES] {expression}")


reset_timer = None

def reset_after_delay(delay=5):
    global reset_timer

    if reset_timer:
        reset_timer.cancel()  # cancel previous reset

    def reset():
        eyes.set_mood(DEFAULT)
        log("reset to default")

    reset_timer = threading.Timer(delay, reset)
    reset_timer.start()


@mcp.tool()
def happy_eyes():
    """Display happy and cute eyes"""
    log("happy eyes")
    eyes.set_mood(EXCITED)
    reset_after_delay()
    return {"emotion": "happy"}


@mcp.tool()
def anger_eyes():
    """Display angry eyes"""
    log("angry")
    eyes.set_mood(ANGRY)
    reset_after_delay()
    return {"emotion": "angry"}


@mcp.tool()
def sad_eyes():
    """Display sad eyes"""
    log("sad")
    eyes.set_mood(SAD)
    reset_after_delay()
    return {"emotion": "sad"}