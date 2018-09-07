from urllib.parse import urlparse
from easy_thumbnails.fields import ThumbnailerImageField
from threadlocals.threadlocals import get_current_request
from trax.choices import GAME_MODES, ROUTE_TYPES, PLATFORM_CHOICES
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from embed_video.fields import EmbedVideoField

from trax.utils import get_object_by_string


class TrackQueryset(models.query.QuerySet):
    def my(self):
        request = get_current_request()
        if request and request.user.is_authenticated():
            return self.filter(creator=request.user)
        return self.all()


class TrackManager(models.Manager):
    def get_queryset(self):
        default_platforms = 'pc ps4 xb1'
        qs = TrackQueryset(self.model, using=self._db)
        request = get_current_request()
        if request:
            platforms = request.COOKIES.get('traxpf', default_platforms)
            platforms = platforms.replace("%20", " ").split()
            if not platforms:
                platforms = default_platforms.split()
            qs = qs.filter(platform__in=platforms)
        return qs

    def my(self):
        return self.get_queryset().my()


class Track(models.Model):
    objects = TrackManager()

    title = models.CharField(unique=True, max_length=256)
    description = models.TextField(blank=True, default='')
    author = models.CharField(max_length=64, default='', null=False)
    creator = models.ForeignKey("players.Player", null=True)
    link = models.URLField(null=True)
    video = EmbedVideoField(null=True, blank=True)
    game_mode = models.CharField(max_length=8, choices=GAME_MODES,
                                 default=GAME_MODES[0][0])
    route_type = models.CharField(max_length=1, choices=ROUTE_TYPES,
                                  default=ROUTE_TYPES[0][0])
    route_length_km = models.FloatField(null=True)
    num_players = models.PositiveSmallIntegerField(null=True)
    typical_laptime = models.IntegerField(
        help_text=_('How many seconds does it typically take for a fully '
                    'customized car to finish a lap with no major issues?'),
        null=True)
    pit_lane = models.BooleanField(
        help_text=_('Does the track have a pit lane with repair icons?'),
        default=False)
    surface_street = models.SmallIntegerField(
        help_text=_('Typical streets in Los Santos'), default=0)
    surface_road = models.SmallIntegerField(
        help_text=_('Tarmac roads e.g. Blaine County'), default=0)
    surface_dirt = models.SmallIntegerField(
        help_text=_('Non-tarmac dirt roads e.g. in Sandy Shores'), default=0)
    surface_flat = models.SmallIntegerField(
        help_text=_('Tarmac and concrete surface at LS airport, Fort '
                    'Zancudo and similar areas. Highways as well.'), default=0)
    surface_stunt = models.SmallIntegerField(
        help_text=_('Surfaces made with stunt props.'), default=0)
    surface_offroad = models.SmallIntegerField(
        help_text=_('Anything offroad e.g. forests, fields, grasslands, '
                    'desert'), default=0)
    elevation_changes = models.SmallIntegerField(
        help_text=_("From airport-flat (0), to Tongva Hills (50) to "
                    "rollercoastery ups and downs (100)."),
        default=0)
    car_classes = models.ManyToManyField('vehicles.VehicleClass')
    platform = models.CharField(max_length=8,
                                choices=PLATFORM_CHOICES, default='pc')
    reference_track = models.BooleanField(
        default=False, help_text=_("Is this a reference track for laptimes?"))
    image = ThumbnailerImageField(upload_to='trackimages', blank=True)
    num_hairpins = models.SmallIntegerField(default=0)
    num_slow_turns = models.SmallIntegerField(default=0)
    num_fast_turns = models.SmallIntegerField(default=0)
    num_slow_chicanes = models.SmallIntegerField(default=0)
    num_fast_chicanes = models.SmallIntegerField(default=0)
    include_in_halloffame = models.BooleanField(default=True)

    @property
    def terrains(self):
        return [
            {'type': _('Street'), 'perc': self.surface_street, 'class': 'st'},
            {'type': _('Road'), 'perc': self.surface_road, 'class': 'ro'},
            {'type': _('Dirt'), 'perc': self.surface_dirt, 'class': 'di'},
            {'type': _('Flat'), 'perc': self.surface_flat, 'class': 'fl'},
            {'type': _('Stunt'), 'perc': self.surface_stunt, 'class': 's'},
            {'type': _('Offroad'), 'perc': self.surface_offroad, 'class': 'of'},
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('track_detail', args=[str(self.pk)])

    @property
    def duration(self):
        minu, seco = divmod(self.typical_laptime, 60)
        return "{0}:{1:02}".format(int(minu), int(seco))

    @property
    def route_length(self, unit='km'):
        return "{:.02f}".format(self.route_length_km)


def get_track_by_string(s):
    """returns a track object, if something with a score > 70 could be found."""
    return get_object_by_string(s, Track, 'title')


class Laptime(models.Model):
    track = models.ForeignKey("tracks.Track")
    player = models.ForeignKey("players.Player")
    created = models.DateTimeField(auto_now_add=True)
    recorded = models.DateField(null=True)
    vehicle = models.ForeignKey("vehicles.Vehicle")
    millis = models.IntegerField(default=0)
    millis_per_km = models.IntegerField(default=0)
    comment = models.TextField(default='', null=True, blank=True)
    video = EmbedVideoField(null=True)
    link = models.URLField(null=True)
    pc_60fps = models.BooleanField(default=False)

    class Meta:
        ordering=['-pk', ]

    def __str__(self):
        return '{0} {1}'.format(self.player.username,
                                self.vehicle.name)

    @property
    def duration(self):
        seco, mill = divmod(self.millis, 1000)
        minu, seco = divmod(seco, 60)
        return "{0}:{1:02}.{2:03}".format(int(minu), int(seco), int(mill))


    @property
    def km_per_h(self):
        if self.millis_per_km != 0:
            return '{:.3f}'.format(
                (1.0 / self.millis_per_km ) * 1000 * 3600
            )
        return '?'

    @property
    def linktype(self):
        """returns "l" for generic link, "v" for videolink, "" if no link at all"""
        hostname = urlparse(self.link).hostname
        if not hostname:
            return ""
        for hostpart in VIDEOSITES:
            if hostname.startswith(hostpart):
                return "v"
        return "l"




