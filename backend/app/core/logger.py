import logging
import sys


def setup_logger(name: str = "study_assistant") -> logging.Logger:
    """
    Creates and configures the application logger.
    """

    logger = logging.getLogger(name)

    # Prevent duplicate handlers during auto-reload
    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    logger.propagate = False

    return logger


logger = setup_logger()