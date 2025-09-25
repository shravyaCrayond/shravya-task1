import logging


def configure_logging():
    LOG_FORMAT = "%(asctime)s - %(name)s -" " " "%(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


logger = logging.getLogger("fastapi_app")
