import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django import forms
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.gzip import gzip_page
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView

from players.models import Player
from .models import Track, Laptime
from vehicles.models import Vehicle
from .forms import TrackForm, SSRCreateForm


def track_detail(request, pk):
    t = Track.objects.get(pk=pk)
    todaystring = datetime.date.today().strftime('%Y-%m-%d')
    ssrform = SSRCreateForm(initial={'track': t})
    return render(
        request, 'tracks/track_detail.html',
        context={'obj': t,
                 'form': LaptimeAddForm(initial={'recorded': todaystring}),
                 'ssrform': ssrform})


class LaptimeAddForm(forms.ModelForm):
    anylink = forms.URLField(required=False)
    humantime = forms.CharField()

    class Meta:
        model = Laptime
        fields = ['vehicle', 'comment', 'recorded']
    def __init__(self, *a, **k):
        super(LaptimeAddForm, self).__init__(*a, **k)
        self.fields['vehicle'].empty_label = ''


@login_required
def laptime_add(request, lap_pk):
    if request.method == 'POST':
        vehicle = get_object_or_404(Vehicle, pk=request.POST.get('vehicle'))
        t = Track.objects.get(pk=lap_pk)
        l = Laptime()
        l.track = t
        l.player = request.user
        l.vehicle = vehicle
        try:
            parts = request.POST.get('seconds')
            m, rest = parts.split(':')
            millis = 1000 * (int(m)*60 + float(rest))
        except:
            messages.add_message(
                request, messages.ERROR,
                'I did not understand your laptime input. Please use the format MM:SS.milli')
            return HttpResponseRedirect(reverse('track_detail', args=(t.pk,)))

        l.millis = millis
        l.millis_per_km = millis / t.route_length_km
        l.comment = request.POST.get('comment', '')
        yy,mm,dd = request.POST.get('recorded').split('-')
        l.recorded = datetime.date(int(yy), int(mm), int(dd))
        l.created = datetime.datetime.now()
        l.save()
        messages.add_message(request, messages.SUCCESS,
                             "Okay, your laptime was saved.")
    return HttpResponseRedirect(reverse('track_detail', args=(t.pk,)))


class TrackList(ListView):
    model = Track


@method_decorator(login_required, name='dispatch')
class TrackCreate(CreateView):
    model = Track
    form_class = TrackForm

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super(TrackCreate, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class TrackEdit(UpdateView):
    model = Track
    form_class = TrackForm


def laptime_json(request, track_pk):
    data = []
    for laptime in Laptime.objects.filter(
            track__pk=track_pk,
            recorded__isnull=False).select_related('vehicle', 'player'):
        data.append({
            # TODO this is a very ugly hack. pls improve
            'vehicle':'<a href="/v/s/{0}/">{1}</a>'.format( laptime.vehicle.pk, laptime.vehicle),
            'duration': {'display': laptime.duration,
                         'millis': laptime.millis},
            'name': str(laptime.player),
            'date': {'display': laptime.recorded.strftime('%Y-%m-%d'),
                     'timestamp':laptime.recorded.strftime('%Y-%m-%d')}
        })
    return JsonResponse({'data': data},
                        json_dumps_params={'separators':(',', ':')})


@cache_page(60 * 0.2)
@gzip_page
def tracks_json(request):
    data = []
    print("UNCACHED")
    for t in Track.objects.all().extra(
            select={'laptime_count':
                    'SELECT COUNT(*) FROM tracks_laptime '
                    'WHERE tracks_laptime.track_id = tracks_track.id'},):
        data.append({
            'pk': t.pk,
            'title': t.title,
            'author': t.author,
            'platform': t.platform,
            'laptime_count':t.laptime_count,
            'game_mode': t.game_mode,
            'route_type': t.route_type,
            'typical_laptime': t.typical_laptime,
            'num_players': t.num_players,
            'pit_lane': t.pit_lane and 'Y' or 'N',
            'route_length_km': t.route_length_km, })

    return JsonResponse({'data': data},
                        json_dumps_params={'separators':(',', ':')})

