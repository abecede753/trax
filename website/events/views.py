import random
import datetime

from django.conf import settings
from django.contrib import messages
from django import forms
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import never_cache
from django.views.generic import CreateView, DetailView

from trax.choices import RACE_STATES
from tracks.models import Laptime
from vehicles.models import Vehicle
from .models import StaggeredStartRace, SSRParticipation
from .utils import get_user_car_list


class SSREditForm(forms.ModelForm):
    class Meta:
        model = StaggeredStartRace
        fields = ['track', 'vehicle_class', 'laps', 'comment', ]


class SSRCreateForm(forms.ModelForm):
    class Meta:
        model = StaggeredStartRace
        fields = ['track', 'laps', 'vehicle_class', 'comment']


@method_decorator(login_required, name='dispatch')
class StaggeredStartRaceCreator(CreateView):
    model = StaggeredStartRace
    form_class = SSRCreateForm

    def get(self, request, *a, **k):
        raise Http404()

    def form_valid(self, form):
        form.instance.host = self.request.user
        form.instance.save()
        form.instance.update_json()
        return super(StaggeredStartRaceCreator, self).form_valid(form)


# OLD STUFF


@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name='dispatch')
class StaggeredStartRaceDetail(DetailView):
    model = StaggeredStartRace

    def get_context_data(self, **kwargs):
        context = super(StaggeredStartRaceDetail,
                        self).get_context_data(**kwargs)
        url = settings.SERVER_NAME
        url += reverse('staggeredstartrace_detail',
                       args=(self.object.pk,))
        context['invite_url'] = url
        context['vehicle_list'] = get_user_car_list(
            user=self.request.user,
            vehicle_class=self.object.vehicle_class, )

        return context

    def get(self, *a, **k):
        obj = self.get_object()
        if obj.status == RACE_STATES.planning:
            obj.status = RACE_STATES.initializing
            obj.save()
        if self.request.GET.get('start_in_secs'):

            nowplus = random.randrange(0, 6)
            nowplus += int(self.request.GET.get('start_in_secs'))
            start_timestamp = datetime.datetime.now() + \
                              datetime.timedelta(milliseconds=nowplus*1000)
            self.object = self.get_object()
            self.object.start_timestamp = start_timestamp
            self.object.status = RACE_STATES.running

            overtake_deficit = None
            try:
                overtake_deficit = int(self.request.GET.get('per_overtake_deficit_millis'))
            except:
                pass
            self.object.per_overtake_deficit_millis = overtake_deficit

            self.object.save()

            #            self.race_km = self.object.track.route_length_km * self.object.laps
            self.calculate_players_start_timestamps()
            self.object.update_json()

        return super(StaggeredStartRaceDetail, self).get(*a, **k)

    def post(self, *a, **k):
        if self.request.POST.get('personal_laptime'):
            timestr = self.request.POST.get('personal_laptime')
            minu, seco = timestr.split(':')
            millis = int(minu) * 60 * 1000 + float(seco) * 1000
            event = self.get_object()
            particip = SSRParticipation.objects.get(
                staggeredstartrace=event,
                player__username=self.request.user.username)
            lt = Laptime(
                track=event.track,
                player=self.request.user,
                recorded=datetime.date.today(),
                vehicle=particip.vehicle,
                millis=millis,
                millis_per_km=millis / event.track.route_length_km,
                comment='participation in a staggered start race',
            )
            lt.save()
            particip.laptime = lt
            particip.save()
            messages.add_message(
                self.request, messages.SUCCESS,
                'Thanks! (a nicer page will follow later. Maybe.)')
            return HttpResponseRedirect('/')

        return super(StaggeredStartRaceDetail, self).get(*a, **k)

    def calculate_players_start_timestamps(self):
        parts = list(self.object.ssrparticipation_set.all().order_by(
            '-estimated_laptime'))
        for p in parts:
            p.estimated_net_millis = p.estimated_laptime * self.object.laps
        total_millis = parts[0].estimated_net_millis
        previous_racestart_dt = this_racestart_dt = self.object.start_timestamp
        raceend_dt = self.object.start_timestamp + datetime.timedelta(
            milliseconds=total_millis)
        for idx, p in enumerate(parts):
            this_racestart_dt = max(
                raceend_dt -datetime.timedelta(
                    milliseconds=p.estimated_net_millis) - datetime.timedelta(
                    milliseconds=self.object.per_overtake_deficit_millis * idx),
                previous_racestart_dt
            )
            p.start_timestamp = this_racestart_dt
            p.save()
            previous_racestart_dt = this_racestart_dt


#        laptimes = list(self.object.laptime_set.all())
#        for lt in laptimes:
#            lt.eventcar = get_eventcar(
#                user=lt.player, vehicle_pk=lt.vehicle.pk,
#                race_km=self.race_km)
#        result = sorted(laptimes, key=lambda x: x.eventcar.total_millis)
#        return result


def participants_list(request, pk=None):
    ssr = get_object_or_404(StaggeredStartRace, pk=pk)
    result = []
    for lt in ssr.ssrparticipation_set.all():
        vehicle = str(lt.vehicle)
        result.append([lt.player.username, vehicle])
    return JsonResponse({'data': result})


class ParticipationForm(forms.ModelForm):
    class Meta:
        model = Laptime
        fields = ['vehicle',]


# class SSRParticipationView(CreateView):
#     model = Laptime
#     form_class=ParticipationForm
#
#     def form_valid(self, form):  # TODO
#         form.instance.host = self.request.user
#         return super(StaggeredStartCreator, self).form_valid(form)

@login_required
def enlist(request, pk, vehicle_pk):
    ssr = get_object_or_404(StaggeredStartRace, pk=pk)

    vehicle = Vehicle.objects.get(pk=vehicle_pk)
    estimated_laptime = (vehicle.cc_millis_per_km *
                         ssr.track.route_length_km *
                         request.user.defaultspeedmultiplier)


    defaults = {'vehicle': vehicle,
                'estimated_laptime': estimated_laptime}
    participation, created = SSRParticipation.objects.get_or_create(
        player=request.user, staggeredstartrace=ssr, defaults=defaults)
    if not created:
        participation.vehicle = vehicle
        participation.estimated_laptime = estimated_laptime
        participation.save()
    ssr.update_json()
    return JsonResponse({'result': 'OK'})


@method_decorator(login_required, name='dispatch')
class StaggeredStartRaceStatus(DetailView):
    model = StaggeredStartRace

    def get(self, *a, **k):
        obj = self.get_object()
        players = []
        for s in obj.ssrparticipation_set.all().order_by('player__username'):
            players.append({'username': s.player.username,
                            'pk': s.player.pk,
                            'vehicle': s.vehicle.name,
                            'start_time': 0})
        return JsonResponse({'result': self.get_object().status,
                             'players': s})

    def get_players(self):
        s = self.get_object()
        return s.ssrparticipation_set.all()[0].player.username
