import datetime
import json
import os

from django.conf import settings
from django.db import models
from django.urls import reverse_lazy
# from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from trax.choices import PLATFORM_CHOICES, RACE_STATES, SSR_ALGORITHMS

#class StaggeredPlaylist(models.Model):
#    title = models.CharField(max_length=256)
#    creator = models.ForeignKey('players.Player')
#    created = models.DateTimeField(auto_now_add=True)
#    platform = models.CharField(max_length=8,
#                                choices=PLATFORM_CHOICES, default='pc')


class StaggeredStartRace(models.Model):
    track = models.ForeignKey('tracks.Track')
    vehicle_class = models.ForeignKey('vehicles.VehicleClass', null=True)
    laps = models.PositiveSmallIntegerField(default=5)
    host = models.ForeignKey('players.Player')
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=RACE_STATES.choices,
                              default=RACE_STATES.planning)
    hosting_date = models.DateTimeField(null=True)
    link = models.URLField(
        null=True, help_text=_("could be a screenshot URL of the results"))
    comment = models.TextField(default="", blank=True)
    start_timestamp = models.DateTimeField(null=True, default=None)
    per_overtake_deficit_millis = models.IntegerField(null=True, default=600)
#    staggeredplaylist = models.ForeignKey('StaggeredPlaylist', null=True)
#    number_in_playlist = models.PositiveSmallIntegerField(default=0)
    algorithm = models.CharField(max_length=2, choices=SSR_ALGORITHMS,
                                 default='SA')

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

    @property
    def json_url(self):
        return os.path.join(
            settings.STATIC_URL, 'ssr',
            '{0}.json'.format(self.pk))

    def update_json(self):
        """saves the current whole json state for faster access"""
        players = []
        current_index = -1
        racetime = 0

        for s in self.ssrparticipation_set.all().order_by('-estimated_laptime'):
            current_index += 1
            if current_index == 0:
                racetime = s.estimated_laptime * self.laps
            start_after_first = datetime.timedelta(
                milliseconds=racetime - (s.estimated_laptime * self.laps))
            minutes = int(start_after_first.seconds / 60)
            seconds = int(start_after_first.seconds % 60)
            millis = int(start_after_first.microseconds / 1000)
            startafterstr = '{0:02d}:{1:02d}.{2:03d}'.format(
                minutes, seconds, millis)
            newdict = {'username': s.player.username,
                            'pk': s.player.pk,
                            'vehicle': s.vehicle.name,
                            'estimated_laptime': s.estimated_laptime,
                            'start_after_first': startafterstr,
                            }
            if s.start_timestamp:
                newdict['timestamp'] = int(s.start_timestamp.timestamp()*1000)
            players.append(newdict)
        dct = {'status': self.status,
                             'players': players}
        filename = os.path.join(
            settings.STATIC_ROOT, 'ssr',
            '{0}.json'.format(self.pk))
        with open(filename, 'w') as f:
            f.write(json.dumps({'data': dct}, separators=(',', ':')))


class SSRParticipation(models.Model):
    player = models.ForeignKey("players.Player")
    vehicle = models.ForeignKey("vehicles.Vehicle")
    staggeredstartrace = models.ForeignKey('StaggeredStartRace')
    estimated_laptime = models.IntegerField(
        null=True, help_text='according to calculations the estimated '
                             'total racing net time for one lap.')
    laptime = models.ForeignKey("tracks.Laptime", null=True)
    start_timestamp = models.DateTimeField(null=True)

    class Meta:
        ordering = ('start_timestamp', 'player__username')

    @property
    def start_in_millis(self):
        # tdobj = self.start_timestamp - now()
        tdobj = self.start_timestamp - datetime.datetime.now(
            tz=self.start_timestamp.tzinfo)
        return int(tdobj.total_seconds() * 1000)
