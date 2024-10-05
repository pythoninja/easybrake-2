import sys

from loguru import logger


def init_logger():
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="{time:YYYY-MM-DD at HH:mm:ss} - <level>{level}</level> - {message}")
