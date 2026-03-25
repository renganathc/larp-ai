import asyncio
import threading
import subprocess
import edge_tts
import hardware.shared as shared

from anim_eyes.utils.moods_utils import DEFAULT, SAD, CUTE, ANGRY
from instances import mcp
from hardware.shared import playback_queue, speech_process



def get_eyes():
    if shared.eyes is None:
        raise RuntimeError("Eyes not initialized yet")
    return shared.eyes

def get_playback_queue():
    return playback_queue

def apply_eye_expression(expression):
    try:
        if expression is None:
            return

        eyes = get_eyes()

        if expression == "DEFAULT":
            eyes.set_mood(DEFAULT)
        elif expression == "SAD":
            eyes.set_mood(SAD)
        elif expression == "CUTE":
            eyes.set_mood(CUTE)
        elif expression == "ANGRY":
            eyes.set_mood(ANGRY)
        else:
            print({expression})

    except Exception as e:
        print({e})


def playback_worker():

    global speech_process

    while True:
        item = playback_queue.get()

        audio_file = item["file"]
        expression = item["expression"]

        apply_eye_expression(expression)

        speech_process = subprocess.Popen(["afplay", audio_file])
        speech_process.wait()

        playback_queue.task_done()


# Start playback thread
threading.Thread(target=playback_worker, daemon=True).start()


async def generate_and_queue(text, expression):
    if not text:
        return

    output_file = f"/tmp/speech_{abs(hash(text))}.mp3"

    communicate = edge_tts.Communicate(text, "en-GB-RyanNeural")
    await communicate.save(output_file)

    playback_queue.put({
        "file": output_file,
        "expression": expression
    })


def run_async(coro):
    try:
        loop = asyncio.get_event_loop()

        if loop.is_running():
            asyncio.create_task(coro)
        else:
            loop.run_until_complete(coro)

    except RuntimeError:
        asyncio.run(coro)


@mcp.tool()
def speak(text: str = "", eye_expression: str = None):
    """
    Convert text into speech with synced eye expressions.
    Expressions: DEFAULT, SAD, CUTE, ANGRY
    """

    run_async(generate_and_queue(text, eye_expression))

    return {
        "status": "queued",
        "message": text,
        "eye_expression": eye_expression
    }