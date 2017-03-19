import datetime
from collections import OrderedDict

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django import forms
from django.db.models import Count
from django.http import Http404
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.views.decorators.cache import cache_page
from django.views.decorators.gzip import gzip_page
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView

from players.models import Player
from .models import Track, Laptime
from vehicles.models import Vehicle
from .forms import TrackForm, SSRCreateForm


def track_detail(request, pk):
    try:
        t = Track.objects.get(pk=pk)
    except:
        return render(request, 'trax/not_on_this_platform.html')
    todaystring = datetime.date.today().strftime('%Y-%m-%d')
    ssrform = SSRCreateForm(initial={'track': t})

    if not t.creator:
        creator = None
    else:
        creator = t.creator.username
    can_edit = (request.user.username == creator) or \
               request.user.is_staff
    m, s = divmod(t.typical_laptime * 5, 60)
    h, m = divmod(m, 60)
    five_laps_duration = "%02d:%02d:%02d" % (h, m, s)


    return render(
        request, 'tracks/track_detail.html',
        context={'obj': t,
                 'form': LaptimeAddForm(initial={'recorded': todaystring}),
                 'can_edit': can_edit,
                 'ssrform': ssrform,
                 'five_laps_duration': five_laps_duration})


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

        # MAYBE TODO: change millis and millis_per_km to a float field?
        l.millis = round(millis)
        l.millis_per_km = round(millis / t.route_length_km)
        l.comment = request.POST.get('comment', '')
        l.link = request.POST.get('anylink', '')
        yy,mm,dd = request.POST.get('recorded').split('-')
        l.recorded = datetime.date(int(yy), int(mm), int(dd))
        l.created = datetime.datetime.now()
        l.save()
        messages.add_message(request, messages.SUCCESS,
                             "Okay, your laptime was saved.")
    redir = request.environ.get("HTTP_REFERER",
                                reverse('track_detail', args=(t.pk,)))
    return HttpResponseRedirect(redir)


class TrackList(ListView):
    model = Track

    def get_queryset(self):
        queryset = Track.objects.all().annotate(num_laptimes=Count('laptime'))
        return queryset



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

    def form_valid(self, form):
        """special permissions check
        NOTE: make nicer whenever time available for that."""
        if form.instance.creator:
            creator = form.instance.creator.username
        else:
            creator = None
        user = self.request.user

        if (creator == user.username) or user.is_staff:
            return super(TrackEdit, self).form_valid(form)
        raise Http404()


def laptime_json(request, track_pk):
    data = []
    for laptime in Laptime.objects.filter(
            track__pk=track_pk,
            recorded__isnull=False).select_related('vehicle', 'player'):
        classes = laptime.vehicle.classes.all()
        strclasses = ',' + ','.join([x.name for x in classes]) + ','
        data.append({
            # TODO this is a very ugly hack. pls improve
            'vehicle':'<a href="/v/s/{0}/">{1}</a>'.format( laptime.vehicle.pk, laptime.vehicle),
            'classes': strclasses,
            'duration': {'display': laptime.duration,
                         'millis': '{:020}'.format(laptime.millis)},
            'name':'<a href="/p/{0}/">{1}</a>'.format( laptime.player.pk, laptime.player),
            'date': {'display': laptime.recorded.strftime('%Y-%m-%d'),
                     'timestamp':laptime.recorded.strftime('%Y-%m-%d')},
            'comment': laptime.comment,
            'link': laptime.link
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


@login_required
def laptime_delete(request, lap_pk):
    laptime = get_object_or_404(Laptime, pk=lap_pk)
    if request.user.pk != laptime.player.pk:
        raise Http404
    laptime.delete()
    return JsonResponse({'data':'ok'})


def epsilon_detail(request):
    exclude_usernames = ['benimi', ]
    try:
        t = Track.objects.get(pk=117)
    except:
        return render(request, 'trax/not_on_this_platform.html')
    todaystring = datetime.date.today().strftime('%Y-%m-%d')

    if not t.creator:
        creator = None
    else:
        creator = t.creator.username

    ls = Laptime.objects.filter(
        track__id=117, link__isnull=False).exclude(
        link='').order_by('millis')
    players = {}
    for l in ls:
        if l.player.username in exclude_usernames:
            continue
        if players.get(l.player.username):
            players[l.player.username].append(l)
        else:
            players[l.player.username] = [l, ]
    od = list(OrderedDict(sorted(players.items(), key=lambda t: t[1][0].millis)).items())

    divisions = []
    for x in (0, 15, 30, 45):
        if len(od) >= x:
            divisions.append(od[x:x + 15])
        else:
            divisions.append([])
    if len(od) > 60:
        divisions.append(od[60:])
    else:
        divisions.append([])

    return render(
        request, 'tracks/epsilon_detail.html',
        context={'obj': t,
                 'form': LaptimeAddForm(initial={'recorded': todaystring}),
                 'divisions': divisions})


def grotti17_detail(request):
    exclude_usernames = []
    tables = ( ('Accepted',  22),
               ('Waiting list', 100),
             )
    try:
        t = Track.objects.get(pk=131)
    except:
        return render(request, 'trax/not_on_this_platform.html')
    todaystring = datetime.date.today().strftime('%Y-%m-%d')

    if not t.creator:
        creator = None
    else:
        creator = t.creator.username

    startdate = timezone.datetime(2017,3,18)
    ls = Laptime.objects.filter(
        track=t,
        created__gt=startdate,
        link__isnull=False).exclude(
        link='').order_by('millis')
    # ls = Laptime.objects.all().order_by('millis')  # XXX DEBUG
    players = {}
    for l in ls:
        if l.player.username in exclude_usernames:
            continue
        if players.get(l.player.username):
            players[l.player.username].append(l)
        else:
            players[l.player.username] = [l, ]
    od = list(OrderedDict(sorted(players.items(), key=lambda t: t[1][0].millis)).items())

    divisions = []
    last_pos = 0
    for title, x in tables:
        if len(od) >= last_pos:
            divisions.append(od[last_pos:last_pos + x])
            last_pos += x

    return render(
        request, 'tracks/grotti17_detail.html',
        context={'obj': t,
                 'form': LaptimeAddForm(initial={'recorded': todaystring}),
                 'divisions': divisions})
