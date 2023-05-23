import threading
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)-4s] (%(threadName)-9s) %(message)s',
                    datefmt = "%H:%M:%S",)


def wait_for_event(e: threading.Event):
    lock.acquire()
    logging.debug(e.is_set())
    logging.debug('waiting')
    time.sleep(2)
    logging.debug('done')
    lock.release()


def wait_for_event_timeout(e, t):
    while not e.isSet():
        logging.debug('wait_for_event_timeout starting')
        event_is_set = e.wait(t)
        logging.debug('event set: %s', event_is_set)
        if event_is_set:
            logging.debug('processing event')
        else:
            logging.debug('doing other things')


if __name__ == '__main__':
    e = threading.Event()
    lock = threading.Lock()

    e.set()
    for i in range(2):
        t1 = threading.Thread(name='th-{}'.format(i),
                          target=wait_for_event,
                          args=(e,))
        t1.start()
        # e.set()

    logging.debug('Waiting before calling Event.set()')
    time.sleep(3)
    e.set()
    logging.debug('Event is set')