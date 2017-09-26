import time
import logging

from .settings import (
    timy_config,
    TrackingMode
)

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def output(ident, text):
    if not timy_config.tracking:
        return

    message = '{} {} seconds'.format(ident, text)

    if timy_config.tracking_mode == TrackingMode.PRINTING:
        print(message)
    elif timy_config.tracking_mode == TrackingMode.LOGGING:
        logger.info(message)


class Timer(object):

    def __init__(self, ident=timy_config.DEFAULT_IDENT,
                 include_sleeptime=True):
        self.ident = ident
        self.start = 0
        if include_sleeptime:
            self.time_func = time.perf_counter
        else:
            self.time_func = time.process_time

    def __enter__(self):
        self.start = self.time_func()
        return self

    def __exit__(self, type, value, traceback):
        output(self.ident, '{:f}'.format(self.elapsed))

    @property
    def elapsed(self):
        return self.time_func() - self.start

    def track(self, name='track'):
        output(self.ident, '({}) {:f}'.format(name, self.elapsed))


def timer(ident=timy_config.DEFAULT_IDENT, loops=1, include_sleeptime=True):
    if include_sleeptime:
        time_func = time.perf_counter
    else:
        time_func = time.process_time

    def _timer(function, *args, **kwargs):
        if not timy_config.tracking:
            return function

        def wrapper(*args, **kwargs):
            times = []
            for _ in range(loops):
                start = time_func()
                result = function(*args, **kwargs)
                end = time_func()
                times.append(end - start)

            _times = 'times' if loops > 1 else 'time'
            output(ident, 'executed ({}) for {} {} in {:f}'.format(
                function.__name__, loops, _times, sum(times)))
            output(ident, 'best time was {:f}'.format(min(times)))
            return result

        return wrapper
    return _timer
