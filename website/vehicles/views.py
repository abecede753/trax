from django.forms import CheckboxSelectMultiple
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, UpdateView,
                                  DetailView, ListView)

from trax.utils import is_staff_required, ModelFormWidgetMixin
from .models import Vehicle


class VehicleList(ListView):
    model = Vehicle
    template_name = 'vehicles/vehicle_list.html'

    def get_queryset(self):
        through = Vehicle.classes.through
        return through.objects.all()


class VehicleDetail(DetailView):
    model = Vehicle


@method_decorator(is_staff_required, name='dispatch')
class VehicleCreate(ModelFormWidgetMixin, CreateView):
    model = Vehicle
    fields = ["name", "cc_laptime_millis", "description", "classes",
              "cc_millis_per_km"]
    widgets = {"classes": CheckboxSelectMultiple }
    success_url = reverse_lazy('vehicle_list')


@method_decorator(is_staff_required, name='dispatch')
class VehicleUpdate(ModelFormWidgetMixin, UpdateView):
    model = Vehicle
    fields = ["name", "cc_laptime_millis", "description", "classes"]
    widgets = {"classes": CheckboxSelectMultiple }
    success_url = reverse_lazy('vehicle_list')


