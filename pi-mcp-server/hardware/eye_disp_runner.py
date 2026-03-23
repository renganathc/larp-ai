import threading
import pygame
from anim_eyes.main import create_eyes

eyes = None


def _run_loop():
    global eyes

    try:
        while eyes.is_running():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            eyes.update()

    finally:
        eyes.quit()


def start():
    global eyes

    if eyes is not None:
        return eyes  # already started

    eyes = create_eyes()

    thread = threading.Thread(target=_run_loop, daemon=True)
    thread.start()

    return eyes