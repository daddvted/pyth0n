import os
import cmd
import signal
import time


freqency = 1

def handler(signum, frame):
    print("caught CTRL+C in worker process")

    global freqency
    freqency += 1 


def work():
    signal.signal(signal.SIGINT, handler)
    while True:
        print(f'[pid: {os.getpid()}] {"work~ " * freqency}')
        time.sleep(1)
