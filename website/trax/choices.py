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

RACE_STATES = (
    ('p', _('planning')),
    ('i', _('initializing')),
    ('r', _('running')),
    ('f', _('finished')),
)
