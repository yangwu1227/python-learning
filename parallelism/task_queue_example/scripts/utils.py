import logging
import sys


def setup_logger(name: str) -> logging.Logger:
    """
    Set up a logger instance.

    Parameters
    ----------
    name : str
        The name of the logger.

    Returns
    -------
    logging.Logger
        A logger instance for the module.
    """
    logger = logging.getLogger(name=name)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        fmt="%(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    # No matter how many processes we spawn, we only want one StreamHandler attached to the logger
    if not any(
        isinstance(handler, logging.StreamHandler) for handler in logger.handlers
    ):
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger
