import time
import logging

from .settings import (
    timy_config,
    TrackingMode
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def output(ident, text):
    if not timy_config.tracking:
        return

    message = '{} {} seconds'.format(ident, text)

    if timy_config.tracking_mode == TrackingMode.PRINTING:
        print(message)
    elif timy_config.tracking_mode == TrackingMode.LOGGING:
        logger.info(message)


class Timer(object):

    def __init__(self, ident=timy_config.DEFAULT_IDENT):
        self.ident = ident
        self.start = 0

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, type, value, traceback):
        output(self.ident, '{:f}'.format(self.elapsed))

    @property
    def elapsed(self):
        return time.time() - self.start

    def track(self, name='track'):
        output(self.ident, '({}) {:f}'.format(name, self.elapsed))


def timer(ident=timy_config.DEFAULT_IDENT, loops=1):
    def _timer(function, *args, **kwargs):
        if not timy_config.tracking:
            return function

        def wrapper(*args, **kwargs):
            times = []
            for _ in range(loops):
                start = time.time()
                result = function(*args, **kwargs)
                end = time.time()
                times.append(end - start)

            _times = 'times' if loops > 1 else 'time'
            output(ident, 'executed ({}) for {} {} in {:f} seconds'.format(
                function.__name__, loops, _times, sum(times)))
            output(ident, 'best time was {:f} seconds'.format(min(times)))
            return result

        return wrapper
    return _timer
