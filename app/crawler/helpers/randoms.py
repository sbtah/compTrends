import time
from random import randint
from utilities.logger import logger


def random_sleep_small():
    """Custom sleep function that sleeps from 3 to 6 seconds"""

    value = randint(10, 15)
    logger.info(f"Random sleep for: {value} seconds.")
    return time.sleep(value)
