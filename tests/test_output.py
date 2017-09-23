import logging

from unittest import mock

from io import StringIO

from timy import output
from timy.settings import (
    timy_config,
    TrackingMode)

logger = logging.getLogger('timy')


@mock.patch('sys.stdout', new_callable=StringIO)
def test_output_no_tracking(p_stdout):
    timy_config.tracking = False
    timy_config.tracking_mode = TrackingMode.PRINTING

    output('ident', 'text')
    assert p_stdout.getvalue() == ''


@mock.patch('sys.stdout', new_callable=StringIO)
def test_output_print_tracking(p_stdout):
    timy_config.tracking = True
    timy_config.tracking_mode = TrackingMode.PRINTING

    output('ident', 'text')
    assert p_stdout.getvalue() == 'ident text seconds\n'


def test_output_logger_tracking():
    timy_config.tracking = True
    timy_config.tracking_mode = TrackingMode.LOGGING

    with mock.patch.object(logger, 'info') as p_info:
        output('ident', 'text')
        p_info.assert_called_with('ident text seconds')
