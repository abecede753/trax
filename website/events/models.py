from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

RACE_STATES = (
    ('p', _('planning')),
    ('i', _('initializing')),
    ('r', _('running')),
    ('f', _('finished')),
)

class StaggeredStartRace(models.Model):
    track = models.ForeignKey('tracks.Track')
    vehicle_class = models.ForeignKey('vehicles.VehicleClass', null=True)
    laps = models.PositiveSmallIntegerField(default=1)
    host = models.ForeignKey('players.Player')
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=RACE_STATES,
                              default=RACE_STATES[0][0])
    hosting_date = models.DateTimeField(null=True)
    link = models.URLField(
        null=True, help_text=_("could be a screenshot URL of the results"))
    comment = models.TextField(default="")

    def __str__(self):
        hosting_date = self.hosting_date and \
                       self.hosting_date.strftime('%Y-%m-%d') or \
                       'not defined'
        return '{0} by {1} ({2})'.format(
            self.track.title, self.host.username,
            hosting_date)

    def get_absolute_url(self):
        return reverse_lazy('staggeredstartrace_detail',
                            kwargs={'pk': self.pk})

# TBD
# class Playlist(models.Model):
#     title = models.CharField(max_length=256)
#     creator = models.ForeignKey('players.Player')
#     created = models.DateTimeField(auto_now_add=True)
#     tracks = models.ManyToManyField('tracks.Track')
