import csv
import datetime
from collections import OrderedDict

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django import forms
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic.edit import (CreateView, UpdateView)
from django.views.generic import DetailView

from tracks.models import Track
from .models import Hotlapping, HotlappingLaptime
from tracks.models import Laptime
from vehicles.models import Vehicle


@method_decorator(login_required, name='dispatch')
class HlCreator(CreateView):
    model = Hotlapping
    fields = ['title', 'description', 'track', 'vehicles', 'start_date',
              'end_date', 'divisions_text']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(HlCreator, self).form_valid(form)



@method_decorator(login_required, name='dispatch')
class HlEditor(UpdateView):
    model = Hotlapping
    fields = ['title', 'description', 'track', 'vehicles', 'start_date',
              'end_date', 'divisions_text']

    def dispatch(self, request, *args, **kwargs):
        o = self.get_object()
        if o.owner.pk != request.user.pk:
            raise Http404
        return super(HlEditor, self).dispatch(request, *args, **kwargs)


class HlLaptimeAddForm(forms.ModelForm):
    anylink = forms.URLField(required=False)
    humantime = forms.CharField()

    class Meta:
        model = Laptime
        fields = ['vehicle', ]
    def __init__(self, *a, **k):
        super(HlLaptimeAddForm, self).__init__(*a, **k)
        self.fields['vehicle'].empty_label = ''


@login_required
def hllaptime_add(request, hl_pk):
    if request.method == 'POST':
        vehicle = get_object_or_404(Vehicle, pk=request.POST.get('vehicle'))
        hl = Hotlapping.objects.get(pk=hl_pk)
        t = hl.track
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
            return HttpResponseRedirect(reverse('hl_detail', args=(hl.pk,)))

        l.millis = round(millis)
        l.millis_per_km = round(millis / t.route_length_km)
        l.comment = ''
        l.link = request.POST.get('anylink', '')
        l.recorded = datetime.datetime.now()
        l.created = datetime.datetime.now()
        l.save()
        HotlappingLaptime.objects.create(laptime=l, hotlapping=hl)
        messages.add_message(request, messages.SUCCESS,
                             "Okay, your laptime was saved.")
    redir = request.environ.get("HTTP_REFERER",
                                reverse('hl_detail', args=(hl.pk,)))
    return HttpResponseRedirect(redir)


class HlDetail(DetailView):
    model = Hotlapping


    def get_context_data(self, **kwargs):
        o = self.get_object()
        laptimes = self.get_best_laptimes(o)

        tables_plus = []
        current_start_pos = 0
        current_place = 1
        for line in o.divisions_text.splitlines():
            parts = line.split(':')
            num_laptimes = int(parts[0])
            title = ':'.join(parts[1:])

            contents = [{'place': None, 'laptime':None }]
            if len(laptimes) >= current_start_pos:
                contents = []
                for l in laptimes[current_start_pos:current_start_pos + num_laptimes]:
                    contents.append({'place': current_place, 'laptime':l})
                    current_place += 1
            tables_plus.append(
                (title, contents)
            )
            current_start_pos += num_laptimes

        todaystring = datetime.date.today().strftime('%Y-%m-%d')

        laptimeaddform = HlLaptimeAddForm(initial={'recorded': todaystring})
        laptimeaddform.fields['vehicle'].queryset = o.vehicles.all()


        context={'object': o,
                 'form': laptimeaddform,
                 'entry_possible': timezone.now() < o.end_date,
                 'divisions': tables_plus}
        return context

    def get_best_laptimes(self, o):
        hls = o.hotlappinglaptime_set.all().order_by('laptime__millis')
        result = []
        used_names = []
        for hl in hls:
            l = hl.laptime
            if l.player.username in used_names:
               continue
            used_names.append(l.player.username)
            result.append(l)
        return result

    def get_all_positions(self, o):
        real_laptimes = self.get_best_laptimes(o)
        pass


def hl_download_csv(request, pk):
    print (pk)
    o = get_object_or_404(Hotlapping, pk=pk)
    if o.owner.pk != request.user.pk:
        raise Http404

    laptimes = HlDetail().get_best_laptimes(o)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = \
        'attachment; filename="{0}.csv"'.format(o.title)

    writer = csv.writer(response)
    writer.writerow(['User', 'Vehicle', 'Link', 'Date', 'Milliseconds', 'Laptime'])
    for line in laptimes:
        writer.writerow([line.player.username,
                        line.vehicle.name,
                        line.link,
                        line.created.strftime("%Y-%m-%d %H:%M"),
                        line.millis,
                        line.duration])

    return response
