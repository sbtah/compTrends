import time
from random import randint
from utilites.logger import logger


def random_sleep_small():
    """Custom sleep function that sleeps from 3 to 6 seconds"""

    value = randint(3, 5)
    logger.info(f"Random sleep for: {value} seconds.")
    return time.sleep(value)
