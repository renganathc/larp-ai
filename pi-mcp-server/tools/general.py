from instances import mcp
from anim_eyes.utils.moods_utils import DEFAULT
import hardware.shared as shared

def get_eyes():
    if shared.eyes is None:
        raise RuntimeError("Eyes not initialized yet")
    return shared.eyes

@mcp.tool()
def reset_bot_activity():
    """Reset the bot's activity and clear all queued tasks."""

    eyes_obj = get_eyes()
    eyes_obj.set_mood(DEFAULT)

    # Clear queue safely
    with shared.playback_queue.mutex:
        shared.playback_queue.queue.clear()

    # Stop speech process properly
    if shared.speech_process is not None:
        shared.speech_process.terminate()
        shared.speech_process.join()
        shared.speech_process = None

    return {"status": "success"}