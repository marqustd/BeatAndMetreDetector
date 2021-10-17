import logging


def config_logger(filename):
    logging.basicConfig(level=logging.INFO, filename=filename)
    logging.getLogger().addHandler(logging.StreamHandler())
