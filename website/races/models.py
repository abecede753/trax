from django.db import models
from django.utils.translation import ugettext_lazy as _

RACE_STATES = (
    ('p', _('planning')),
    ('i', _('initializing')),
    ('r', _('running')),
    ('f', _('finished')),
)

class Race(models.Model):
    track = models.ForeignKey('tracks.Track')
    laps = models.PositiveSmallIntegerField(default=1)
    host = models.ForeignKey('players.Player')
    created = models.DateTimeField(auto_created=True)
    status = models.CharField(max_length=1, choices=RACE_STATES,
                              default=RACE_STATES[0][0])
    hosting_date = models.DateTimeField(null=True)
    laptimes = models.ManyToManyField('tracks.Laptime')
    link = models.URLField(
        null=True, help_text=_("could be a screenshot URL of the results"))
    comment = models.TextField(default="")

    def __str__(self):
        return '{0} by {1} ({2})'.format(
            self.track.title, self.host.username,
            self.hosting_date.strftime('%Y-%m-%d'))


# TBD
# class Playlist(models.Model):
#     title = models.CharField(max_length=256)
#     creator = models.ForeignKey('players.Player')
#     created = models.DateTimeField(auto_created=True)
#     tracks = models.ManyToManyField('tracks.Track')
