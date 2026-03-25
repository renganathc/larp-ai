from instances import mcp
import threading

import tools.speech
import tools.general
#import tools.movement

def run_mcp():
    mcp.run()


if __name__ == "__main__":
    
    threading.Thread(target=run_mcp, daemon=True).start()
    
    from hardware.eye_disp_runner import run
    run()