
import logging
from logging.handlers import RotatingFileHandler
import os
import sys

def _init_logger(log_level, namespace, maxBytes=5*1024*1024, backupCount=5):
    log_file = os.path.expanduser(
            '~/.config/deepin_remote_assitance/%s.log' % namespace)
    dir_name = os.path.dirname(log_file)
    if not os.path.exists(dir_name):
        try:
            os.makedirs(dir_name)
        except Exception:
            sys.exit(1)
    logger = logging.getLogger(namespace)
    file_handler = RotatingFileHandler(log_file, maxBytes=maxBytes,
                                       backupCount=backupCount)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(log_level)
    return logger

server_log = _init_logger(logging.INFO, 'server')
client_log = _init_logger(logging.INFO, 'client')
