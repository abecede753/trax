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
from django.views.generic import ListView, DetailView

from tracks.models import Laptime
from vehicles.models import Vehicle
from .models import Player


@method_decorator(login_required, name='dispatch')
class PlayerDetail(DetailView):
    model = Player


@method_decorator(login_required, name='dispatch')
class PlayerList(ListView):
    model = Player
