import sys
sys.path.append("")
from src.main import start_recording, stop_recording

import time

start_recording()

time.sleep(5)

stop_recording()