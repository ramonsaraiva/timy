class TrackingMode(object):
    PRINTING, LOGGING = range(0,2)

TRACKING = True
TRACKING_MODE = TrackingMode.PRINTING

class TimyConfig(object):
    DEFAULT_IDENT = 'Timy'

    def __init__(self, tracking=TRACKING, tracking_mode=TRACKING_MODE):
        self.tracking = tracking
        self.tracking_mode = tracking_mode

timy_config = TimyConfig()
