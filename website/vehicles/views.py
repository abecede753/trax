# from django.shortcuts import render
from django.views.generic import (CreateView, UpdateView,
                                  DetailView, ListView)

from .models import Vehicle


class VehicleList(ListView):
    model = Vehicle


class VehicleDetail(DetailView):
    model = Vehicle


class VehicleCreate(CreateView):
    model = Vehicle


class VehicleUpdate(UpdateView):
    model = Vehicle
