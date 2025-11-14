import logging

LOG_FORMAT = '[%(asctime)s] %(levelname)s in %(name)s: %(message)s'
LOG_LEVEL = logging.DEBUG

# You can change filename to log to a file instead of console
LOG_FILE = None  # e.g. 'scraper.log'


def setup_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    formatter = logging.Formatter(LOG_FORMAT)
    if LOG_FILE:
        handler = logging.FileHandler(LOG_FILE)
    else:
        handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    if not logger.hasHandlers():
        logger.addHandler(handler)
    return logger
