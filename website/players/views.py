# from django.conf import settings
from django.contrib import messages
# from django import forms
from django.contrib.auth.decorators import login_required
from django.forms import Form, CharField
from django.http import Http404
from django.http import HttpResponseRedirect
# from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView

from .models import Player
from .utils import encode, decode


@method_decorator(login_required, name='dispatch')
class PlayerDetail(DetailView):
    model = Player

    def get_context_data(self, **kwargs):
        context = super(PlayerDetail, self).get_context_data(**kwargs)
        if self.request.user.is_staff or \
                self.request.user.username == self.get_object().username:
            context['passwordlink'] = encode(self.get_object().username)
        return context


@method_decorator(login_required, name='dispatch')
class PlayerList(ListView):
    model = Player


class TrackForm(Form):
    password = CharField(max_length=100)


def change_password(request, hash):
    try:
        username = decode(hash)
        user = Player.objects.get(username=username)
    except:  # noqa
        raise Http404
    if request.method == 'POST':
        if request.POST.get('password'):
            user.set_password(request.POST.get('password'))
            user.save()
            messages.add_message(
                request, messages.INFO,
                'The password for user {0} has been changed.'
                ' You can login now.'.format(username))
            return HttpResponseRedirect(reverse('homepage'))
    return render(
        request, 'players/change_password.html',
        context={'username': username})
