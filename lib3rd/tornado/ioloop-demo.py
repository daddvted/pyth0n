import errno
import functools
import socket

import tornado.ioloop
from tornado.ioloop import IOLoop
from tornado.iostream import IOStream



def callback(fd, events):
    print(f"fd: {fd}")
    print(f"events: {events}")

if __name__ == '__main__':
    # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    # sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # sock.setblocking(0)
    # sock.bind(("", 6666))
    # sock.listen(128)

    f0 = open("hehe.txt", "a")
    print(f0.fileno())
    # f1 = open("heheda.txt", "a")
    # print(f1.fileno())

    loop = tornado.ioloop.IOLoop.current()
    loop.start()
    loop.add_handler(f0.fileno(), callback, loop.READ)
    loop.add_handler(f0.fileno(), callback, loop.WRITE)
    # io_loop.start()
