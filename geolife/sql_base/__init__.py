import logging

LOG_HANDLE = None
logger = None
def log_init():
    global logger
    if(logger == None):
        logger = logging.getLogger("root.sql")
    return logger
log_init()