import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView

from players.models import Player
from .models import Track, Laptime
from vehicles.models import Vehicle
from .forms import TrackForm


def track_detail(request, pk):
    t = Track.objects.get(pk=pk)
    vehicles = list(Vehicle.objects.all())
    return render(
        request, 'tracks/track_detail.html',
        context={'obj': t,
                 'vehicles': vehicles})

class LaptimeAddForm(ModelForm):
    class Meta:
        model = Laptime
        fields = ['vehicle', 'untuned', 'comment', 'recorded']

def laptime_add(request, lap_pk):
    if request.method == 'POST':
        try:
            t = Track.objects.get(pk=lap_pk)
            l = Laptime()
            l.track = t
            l.player = Player.objects.all()[0]
            l.vehicle = Vehicle.objects.get(pk=request.POST.get('vehicle'))
            parts = request.POST.get('seconds')
            m, rest = parts.split(':')
            seconds = int(m)*60 + float(rest)
            l.seconds = seconds
            l.seconds_per_km = seconds / t.route_length_km
            l.comment = request.POST.get('comment', '')
            yy,mm,dd = request.POST.get('recorded').split('-')
            l.recorded = datetime.date(int(yy), int(mm), int(dd))
            l.created = datetime.datetime.now()
            l.save()
        except:  # TODO
            messages.add_message(
                request, messages.ERROR,
                'There was an error, and the programmer was too lazy to check which exactly it was. Try again with some valid input.')
    return HttpResponseRedirect(reverse('track_detail', args=(t.pk,)))


@method_decorator(login_required, name='dispatch')
class TrackCreate(CreateView):
    model = Track
    form_class = TrackForm
    success_url = '/'

#    def form_valid(self, form):
#        # This method is called when valid form data has been POSTed.
#        # It should return an HttpResponse.
#        # form.send_email()
#        return super(TrackView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class TrackEdit(UpdateView):
    model = Track
    form_class = TrackForm
    success_url = '/'
