import random
import datetime

from django import forms
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DetailView

from tracks.models import Laptime
from vehicles.models import Vehicle
from .models import StaggeredStartRace, RACE_STATES
from .utils import get_car_list, get_eventcar_by_slug, get_eventcar


# Create your views here.

class RaceCreateForm(forms.ModelForm):
    class Meta:
        model = StaggeredStartRace
        fields = ['track', 'vehicle_class', 'laps', 'comment',]


class StaggeredStartCreator(CreateView):
    model = StaggeredStartRace
    form_class=RaceCreateForm

    def form_valid(self, form):
        form.instance.host = self.request.user
        return super(StaggeredStartCreator, self).form_valid(form)


class StaggeredStartRaceInvite(DetailView):
    model = StaggeredStartRace


@method_decorator(login_required, name='dispatch')
class StaggeredStartRaceDetail(DetailView):
    model = StaggeredStartRace

    def get_context_data(self, **kwargs):
        context = super(StaggeredStartRaceDetail, self).get_context_data(**kwargs)
        if self.request.is_secure():
            proto = 'https'
        else:
            proto = 'http'
        url = proto + '://' + self.request.META['HTTP_HOST']
        url += reverse('staggeredstartrace_invite',
                       args=(self.object.pk,))
        context['invite_url'] = url
        context['vehicle_list'] = get_car_list(user=self.request.user,
                                           vehicle_class=self.object.vehicle_class,)

        return context

    def post(self, *a, **k):
        if self.request.POST.get('start_in_secs'):
            nowplus = random.randrange(0,6)
            nowplus += int(self.request.POST.get('start_in_secs'))
            start_dt = datetime.datetime.now() + \
                       datetime.timedelta(milliseconds=nowplus*1000)
            self.object = self.get_object()
            self.object.start_dt = start_dt
            self.object.status = 'r'  # TODO make cleaner
            self.object.save()

            self.race_km = self.object.track.route_length_km * self.object.laps
            self.calculate_players_start_dts()

        return super(StaggeredStartRaceDetail, self).get(*a, **k)

    def calculate_players_start_dts(self):
        laptimes = list(self.object.laptime_set.all())
        for lt in laptimes:
            lt.eventcar = get_eventcar(
                user=lt.player, vehicle_pk=lt.vehicle.pk,
                stock=lt.untuned, race_km=self.race_km)
        result = sorted(laptimes, key=lambda x: x.eventcar.total_millis)
        return result


## def get_eventcar(user=None, vehicle_pk=None, user_entry=None, stock=None):

def participants_list(request, pk=None):
    ssr = get_object_or_404(StaggeredStartRace, pk=pk)
    result = []
    for lt in Laptime.objects.filter(staggeredstartevent=ssr):
        if lt.untuned:
            vehicle = '{0} (stock)'.format(lt.vehicle.name)
        else:
            vehicle = str(lt.vehicle)
        result.append([lt.player.username, vehicle])
    return JsonResponse({'data': result})


class ParticipationForm(forms.ModelForm):
    class Meta:
        model = Laptime
        fields = ['vehicle', 'untuned']


class SSRParticipation(CreateView):
    model = Laptime
    form_class=ParticipationForm

    def form_valid(self, form):  # TODO
        form.instance.host = self.request.user
        return super(StaggeredStartCreator, self).form_valid(form)

@login_required
def enlist(request, pk):
    ssr = get_object_or_404(StaggeredStartRace, pk=pk)

    eventcar = get_eventcar_by_slug(request.user, request.GET.get('slug'))

    defaults = {'vehicle': Vehicle.objects.get(pk=eventcar.vehicle_pk),
                'untuned': eventcar.stock}
    l, created = Laptime.objects.get_or_create(
        track=ssr.track, player=request.user,
        staggeredstartevent=ssr, defaults=defaults)
    if not created:
        l.vehicle = Vehicle.objects.get(pk=eventcar.vehicle_pk)
        l.untuned = eventcar.stock
        l.save()
    return JsonResponse({'result': 'OK'})
