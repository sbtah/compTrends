import time
from utilities.logger import logger


def calculate_time(func):
    def inner(*args, **kwargs):
        begin = time.time()

        func(*args, **kwargs)

        end = time.time()
        total = end - begin
        logger.info(
            f"Total time taken for: {func.__name__} was {total} seconds.",
        )

    return inner
