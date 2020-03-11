import logging
import logging.handlers

def setup_logger():
    '''
    logger method for custom logger
    '''
    log_format = "%(asctime)s [%(levelname)s]: %(filename)s(%(funcName)s:%(lineno)s) >> %(message)s"
    logging.basicConfig(level=logging.INFO,format=log_format)
    logger = logging.getLogger()
    return logger
