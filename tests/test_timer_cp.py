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


@mock.patch('timy.output')
def test_cp(p_output):
    _timer = Timer()

    with mock.patch.object(_timer, 'time_func') as p_time_func:
        p_time_func.return_value = 1
        with _timer as timer:
            pass
        assert _timer.start == 1

    p_output.assert_called_once_with(_timer.ident, '0.000000')
