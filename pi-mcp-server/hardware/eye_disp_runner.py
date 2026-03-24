import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame
import sys
from anim_eyes.main import create_eyes

def run():
    eyes = create_eyes()

    # expose globally for tools
    import hardware.shared
    hardware.shared.eyes = eyes

    try:
        while eyes.is_running():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            eyes.update()

    finally:
        eyes.quit()