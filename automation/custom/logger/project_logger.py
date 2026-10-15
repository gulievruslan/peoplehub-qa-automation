"""Project-wide logging configuration using Loguru."""

import logging
import os
import sys

from loguru import logger


LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG").upper()

LOG_FORMAT = (
    "{time:YYYY-MM-DD HH:mm:ss} | "
    "{level: <8} | "
    "{file.name}:{line} | "
    "{message}"
)

logger.remove()

logger.add(
    sys.stderr,
    level=LOG_LEVEL,
    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{file.name}:{line}</cyan> | "
        "<level>{message}</level>"
    ),
    colorize=True,
    backtrace=False,
    diagnose=False,
)

logging.getLogger("urllib3").setLevel(logging.WARNING)