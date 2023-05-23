import os
import signal
from multiprocessing import Process

from demo.worker import work

def handler(signum, frame):
    print("caught CTRL+C in main process")

signal.signal(signal.SIGINT, handler)



if __name__ == '__main__':
    print(f'main pid: {os.getpid()}')
    w = Process(target=work)
    w.start()