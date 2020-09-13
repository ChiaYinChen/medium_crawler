"""Util function."""
import functools
import logging
import time

launch_logger = logging.getLogger('launch_crawlers_logger')


def timer(func):
    """Logging function run time."""
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        launch_logger.debug(
            f'Finished {func.__name__!r} in {run_time:.4f} secs'
        )
        return value
    return wrapper_decorator
