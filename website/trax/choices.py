from django.utils.translation import ugettext_lazy as _

GAME_MODES = (
    ('stunt', _('stunt race')),
    ('land', _('land race')),
)

ROUTE_TYPES = (
    ('l', _('laps')),
    ('p', _('point to point')),
)

PLATFORM_CHOICES = (
    ('pc', _('PC')),
    ('ps4', _('PS 4')),
    ('xb1', _('XBox One')),
    ('ps3', _('PS 3')),
    ('xb3', _('XBox 360')),
)


class _Rs:
    planning = 'p'
    initializing = 'i'
    running = 'r'
    finished = 'f'

    def __init__(self):
        self.choices = (
            (self.planning, _('planning')),
            (self.initializing, _('initializing')),
            (self.running, _('running')),
            (self.finished, _('finished')),
        )


RACE_STATES = _Rs()
