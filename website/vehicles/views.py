# from django.shortcuts import render
from django.forms import ModelMultipleChoiceField, CheckboxSelectMultiple, \
    modelform_factory
from django.urls import reverse_lazy
from django.views.generic import (CreateView, UpdateView,
                                  DetailView, ListView)

from .models import Vehicle, VehicleClass


class ModelFormWidgetMixin(object):
    def get_form_class(self):
        return modelform_factory(self.model, fields=self.fields,
                                 widgets=self.widgets)


class VehicleList(ListView):
    model = Vehicle
    template_name = 'vehicles/vehicle_list.html'

    def get_queryset(self):
        through = Vehicle.classes.through
        return through.objects.all()


class VehicleDetail(DetailView):
    model = Vehicle


class VehicleCreate(ModelFormWidgetMixin, CreateView):
    model = Vehicle
    fields = ["name", "cc_millis_per_km", "description", "classes"]
    widgets = {"classes": CheckboxSelectMultiple }
    success_url = reverse_lazy('vehicle_list')


class VehicleUpdate(ModelFormWidgetMixin, UpdateView):
    model = Vehicle
    fields = ["name", "cc_millis_per_km", "description", "classes"]
    widgets = {"classes": CheckboxSelectMultiple }
    success_url = reverse_lazy('vehicle_list')


