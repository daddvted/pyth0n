import logging
import logging.config


logging.config.fileConfig('logging_conf.ini')

LOG = logging.getLogger()
# LOG = logging.getLogger('simpleExample')

LOG.info("hehe")
