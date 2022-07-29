import logging


def create_logger(name):
    logger = logging.getLogger(name)
    formatter = logging.Formatter("| %(asctime)s | [%(levelname)s]:: %(message)s")
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.setLevel(logging.INFO)

    return logger
