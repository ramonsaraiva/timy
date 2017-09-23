import time

from unittest import mock

from timy import Timer
from timy.settings import timy_config


def test_init():
    timer = Timer()
    assert timer.ident == timy_config.DEFAULT_IDENT
    assert timer.start == 0
    assert timer.time_func == time.perf_counter


def test_init_sleeptime():
    timer = Timer(include_sleeptime=False)
    assert timer.time_func == time.process_time
