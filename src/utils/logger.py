import logging

formatter = logging.Formatter("%(asctime)s  %(levelname)s: %(message)s")
logHandler = logging.StreamHandler()
logHandler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)
