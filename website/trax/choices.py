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
)

SSR_ALGORITHMS = (
    ('SA', _("Slow Assist")),
    ('PF', _("Photo Finish")),
    ('SO', _("Standard Only")),
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

class _Ple:
    pitstop="p"
    comment="c"
    yellowflag="y"
    greenflag="g"

    def __init__(self):
        self.choices = (
            (self.pitstop, _('pitstop')),
            (self.comment, _('comment')),
            (self.yellowflag, _('yellow flag')),
            (self.greenflag, _('green flag')),
        )

PITLOGENTRIES = _Ple()
