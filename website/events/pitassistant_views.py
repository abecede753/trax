import os

from django.conf import settings
from django.contrib import messages
from django import forms
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, render
from django.views.decorators.cache import never_cache
from django.views.generic import CreateView, DetailView

from trax.choices import RACE_STATES
from .models import PitAssistant


class PitACreateForm(forms.ModelForm):
    class Meta:
        model = PitAssistant
        fields = ['title', 'description', 'pitstop_seconds']

@method_decorator(login_required, name='dispatch')
class PitAssistantCreator(CreateView):
    model = PitAssistant
    form_class = PitACreateForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.save()
        self.init_filesystem(form.instance)
        return super().form_valid(form)

    def init_filesystem(self, instance):

        dirname = os.path.abspath(
            os.path.join(
                settings.MEDIA_ROOT, 'pitassistant',
                '{0}'.format(instance.pk)
            ))
        os.makedirs(dirname, mode=0o755, exist_ok=True)


@method_decorator(login_required, name='dispatch')
class PitAssistantDetail(DetailView):
    model = PitAssistant

