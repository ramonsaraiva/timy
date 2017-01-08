import time

TIMY = 'Timy'
TRACKING = True

class Timer(object):

    def __init__(self, ident=TIMY):
        self.ident = ident
        self.start = 0

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, type, value, traceback):
        if TRACKING:
            self.show('{:f}'.format(self.elapsed))

    @property
    def elapsed(self):
        return time.time() - self.start

    def track(self, name='track'):
        if TRACKING:
            self.show('({}) {:f}'.format(name, self.elapsed))

    def show(self, text):
        print('{} {} seconds'.format(self.ident, text))


def timer(ident=TIMY, loops=1):
    def _timer(function, *args, **kwargs):
        if not TRACKING:
            return function

        def wrapper(*args, **kwargs):
            times = []
            for _ in range(loops):
                start = time.time()
                result = function(*args, **kwargs)
                end = time.time()
                times.append(end - start)

            print('{} executed ({}) for {} time(s) in {:f} seconds'.format(
                ident, function.__name__, loops, sum(times)))
            print('{} best time was {:f} seconds'.format(ident, min(times)))
            return result

        return wrapper
    return _timer
