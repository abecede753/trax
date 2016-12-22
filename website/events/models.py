import datetime
from trax.choices import PLATFORM_CHOICES, RACE_STATES
from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _


class StaggeredPlaylist(models.Model):
    title = models.CharField(max_length=256)
    creator = models.ForeignKey('players.Player')
    created = models.DateTimeField(auto_now_add=True)
    platform = models.CharField(max_length=8,
                                choices=PLATFORM_CHOICES, default='pc')


class StaggeredStartRace(models.Model):
    track = models.ForeignKey('tracks.Track')
    vehicle_class = models.ForeignKey('vehicles.VehicleClass', null=True)
    laps = models.PositiveSmallIntegerField(default=1)
    host = models.ForeignKey('players.Player')
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=RACE_STATES,
                              default=RACE_STATES[1][0])
    hosting_date = models.DateTimeField(null=True)
    link = models.URLField(
        null=True, help_text=_("could be a screenshot URL of the results"))
    comment = models.TextField(default="")
    start_timestamp = models.DateTimeField(null=True, default=None)
    per_overtake_deficit_millis = models.IntegerField(null=True, default=600)
    staggeredplaylist = models.ForeignKey('StaggeredPlaylist', null=True)
    number_in_playlist = models.PositiveSmallIntegerField(default=0)

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


class SSRParticipation(models.Model):
    player = models.ForeignKey("players.Player")
    vehicle = models.ForeignKey("vehicles.Vehicle")
    untuned = models.BooleanField(default=False,
                                  help_text="is this in an untuned car?")
    staggeredstartrace = models.ForeignKey('StaggeredStartRace')
    estimated_net_millis = models.IntegerField(
        null=True, help_text='according to calculations the estimated '
                             'total racing net time for the whole race.')
    laptime = models.ForeignKey("tracks.Laptime", null=True)
    start_timestamp = models.DateTimeField(null=True)

    class Meta:
        ordering = ('start_timestamp', 'player__username')

    @property
    def start_in_millis(self):
        tdobj = self.start_timestamp - datetime.datetime.now(
            tz=self.start_timestamp.tzinfo)
        return int(tdobj.total_seconds() * 1000)
