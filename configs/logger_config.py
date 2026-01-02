import logging

LOG_FORMAT = '[%(asctime)s] %(levelname)s in %(name)s: %(message)s'
LOG_LEVEL = logging.INFO

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
    handler.setLevel(LOG_LEVEL)
    handler.setFormatter(formatter)
    if not logger.hasHandlers():
        logger.addHandler(handler)
    # Suppress Selenium debug logs
    selenium_logger = logging.getLogger("selenium")
    selenium_logger.setLevel(logging.WARNING)
    # Suppress urllib3 and requests debug logs
    urllib3_logger = logging.getLogger("urllib3")
    urllib3_logger.setLevel(logging.WARNING)
    requests_logger = logging.getLogger("requests")
    requests_logger.setLevel(logging.WARNING)
    return logger
    