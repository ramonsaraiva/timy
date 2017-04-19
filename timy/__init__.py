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

    def __init__(self, ident=timy_config.DEFAULT_IDENT, include_sleep=True):
        self.ident = ident
        self.start = 0
        self.end = 0
        self.include_sleep = include_sleep

    def __enter__(self):
        if self.include_sleep:
            self.start = time.perf_counter()
        else:
            self.start = time.process_time()
        return self

    def __exit__(self, type, value, traceback):
        output(self.ident, '{:f}'.format(self.elapsed))

    @property
    def elapsed(self):
        if self.include_sleep:
            self.end = time.perf_counter()
        else:
            self.end = time.process_time()
        return self.end - self.start

    def track(self, name='track'):
        output(self.ident, '({}) {:f}'.format(name, self.elapsed))


def timer(ident=timy_config.DEFAULT_IDENT, loops=1, include_sleep=True):
    def _timer(function, *args, **kwargs):
        if not timy_config.tracking:
            return function

        def wrapper(*args, **kwargs):
            times = []
            for _ in range(loops):

                if include_sleep:
                    start = time.perf_counter()
                else:
                    start = time.process_time()
                result = function(*args, **kwargs)
                if include_sleep:
                    end = time.perf_counter()
                else:
                    end = time.process_time()
                times.append(end - start)

            _times = 'times' if loops > 1 else 'time'
            output(ident, 'executed ({}) for {} {} in {:f} seconds'.format(
                function.__name__, loops, _times, sum(times)))
            output(ident, 'best time was {:f} seconds'.format(min(times)))
            return result

        return wrapper
    return _timer
