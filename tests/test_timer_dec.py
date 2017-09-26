from unittest import mock

from timy import timer
from timy.settings import timy_config


@mock.patch('timy.output')
def test_timer_no_tracking(p_output):
    timy_config.tracking = False

    @timer()
    def func():
        pass

    func()
    p_output.assert_not_called()


@mock.patch('timy.output')
@mock.patch('time.perf_counter')
def test_timer_include_sleeptime(p_perf_counter, p_output):
    timy_config.tracking = True

    @timer()
    def func():
        pass

    p_perf_counter.return_value = 1

    func()

    p_output.assert_has_calls([
        mock.call(
            timy_config.DEFAULT_IDENT,
            'executed (func) for 1 time in 0.000000'),
        mock.call(
            timy_config.DEFAULT_IDENT,
            'best time was 0.000000'),
    ])


@mock.patch('timy.output')
@mock.patch('time.process_time')
def test_timer_include_sleeptime_no(p_process_time, p_output):
    timy_config.tracking = True

    @timer(include_sleeptime=False)
    def func():
        pass

    p_process_time.return_value = 1

    func()

    p_output.assert_has_calls([
        mock.call(
            timy_config.DEFAULT_IDENT,
            'executed (func) for 1 time in 0.000000'),
        mock.call(
            timy_config.DEFAULT_IDENT,
            'best time was 0.000000'),
    ])


@mock.patch('timy.output')
@mock.patch('time.perf_counter')
def test_timer_with_loops(p_perf_counter, p_output):
    timy_config.tracking = True
    LOOPS = 4

    @timer(loops=LOOPS)
    def func():
        pass

    p_perf_counter.return_value = 1

    func()

    p_output.assert_has_calls([
        mock.call(
            timy_config.DEFAULT_IDENT,
            'executed (func) for {} times in 0.000000'.format(LOOPS)),
        mock.call(
            timy_config.DEFAULT_IDENT,
            'best time was 0.000000'),
    ])
