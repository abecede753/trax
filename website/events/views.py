from django import forms
from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DetailView

from tracks.models import Laptime
from .models import StaggeredStartRace, RACE_STATES

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
                       args=(5,))
        context['invite_url'] = url
        return context


def participants_list(request, pk=None):
    ssr = get_object_or_404(StaggeredStartRace, pk=pk)
    result = []
    for lt in ssr.laptimes.all():
        if lt.untuned:
            vehicle = '%s (stock)'.format(lt.vehicle)
        else:
            vehicle = lt.vehicle
        result.append([lt.player, vehicle])
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
