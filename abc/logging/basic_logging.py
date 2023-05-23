import logging

# logging.basicConfig(format='[%(asctime)s][%(levelname)s]: %(message)s',
#                     datefmt='%Y-%m-%d %H:%M:%S',
#                     level=logging.INFO)

logging.basicConfig(level=logging.DEBUG)
logging.info("info")
logging.debug("debug")

def logger(name = 's1decar'):
    log = logging.getLogger(name)

    file_handler = logging.FileHandler('/tmp/s1decar.log')
    log_format = '[%(asctime)s] %(levelname)s [%(threadName)s]: %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    # formatter = logging.Formatter(fmt=log_format, datefmt=date_format)
    formatter = logging.Formatter(fmt=log_format)
    file_handler.setFormatter(formatter)
    # logging.basicConfig(format=log_format, datefmt=date_format)

    log.addHandler(file_handler)
    log.setLevel(logging.INFO)
    return log
