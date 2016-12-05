import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django import forms
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView

from players.models import Player
from .models import Track, Laptime
from vehicles.models import Vehicle
from .forms import TrackForm


def track_detail(request, pk):
    t = Track.objects.get(pk=pk)
    todaystring = datetime.date.today().strftime('%Y-%m-%d')
    return render(
        request, 'tracks/track_detail.html',
        context={
            'obj': t, 'form': LaptimeAddForm(
                initial={'recorded': todaystring})})


class LaptimeAddForm(forms.ModelForm):
    anylink = forms.URLField(required=False)
    humantime = forms.CharField()

    class Meta:
        model = Laptime
        fields = ['vehicle', 'untuned',
                  'comment', 'recorded']


def laptime_add(request, lap_pk):
    if request.method == 'POST':
        try:
            t = Track.objects.get(pk=lap_pk)
            l = Laptime()
            l.track = t
            l.player = request.user
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
            messages.add_message(request, messages.SUCCESS,
                                 "Okay, your laptime was saved.")
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

def laptime_json(request, track_pk):
    data = []
    for laptime in Laptime.objects.filter(track__pk=track_pk).select_related('vehicle', 'player'):
        data.append({
            'vehicle': str(laptime.vehicle),
            'duration': {'display': laptime.duration,
                         'seconds': float(laptime.seconds) },
            'name': str(laptime.player),
            'date': {'display': laptime.recorded.strftime('%d %m %Y'),
                     'timestamp':laptime.recorded.strftime('%Y-%m-%d')}
        })
    return JsonResponse({'data': data})
