from captcha.fields import ReCaptchaField

from django.contrib.auth import get_user_model, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.forms import Form, ModelForm
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.contrib.auth.hashers import make_password
from players.models import Player, TSUId


from tracks.models import Track

_User = get_user_model()

# @method_decorator(login_required, name='dispatch')
class Homepage(TemplateView):
    template_name = "trax/homepage.html"

    def get_context_data(self, **kwargs):
        context = super(Homepage, self).get_context_data(**kwargs)
        tracks = Track.objects.all()
        context['tracks'] = tracks
        return context


class RegistrationForm(ModelForm):
    class Meta:
        model = Player
        fields = ['username']
    ts_uid = forms.CharField(
        label=_("Teamspeak UID"),
        help_text=_("Leave blank if you don't know what this is."),
        max_length=512,
        required=False)
    password1 = forms.CharField(label='Password',
                                max_length=100,
                                widget=forms.widgets.PasswordInput)
    password2 = forms.CharField(label='Password (again)',
                                max_length=100,
                                widget=forms.PasswordInput)
    captcha = ReCaptchaField()

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        if Player.objects.filter(username=username).count() != 0:
            raise forms.ValidationError(_('This username already exists here. You can send a Social Club message to "Abe.Cede" to solve the issue.'))
        return username

    def clean(self):
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")

        if p1 != p2:
            raise forms.ValidationError(
                _('Your passwords were not identical. Please try again.'))
        return self.cleaned_data


class Registration(TemplateView):
    template_name = "registration/register.html"

    def get(self, request, **kwargs):
        form = RegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, **kwargs):
        form = RegistrationForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {'form':form})
        user = Player(username=form.cleaned_data['username'])
        user.set_password(form.cleaned_data['password1'])
        user.save()
        ts_uid = form.cleaned_data.get('ts_uid', None)
        if ts_uid:
            ts_hash = make_password(ts_uid, salt=ts_uid[:5])
            ts = TSUId(player=user, ts_uid=ts_hash)
            ts.save()
        return HttpResponseRedirect('/')


def logout_view(request):
    logout(request)
    resp = HttpResponseRedirect('/')
    resp.set_cookie('username', '-')
    return resp


class TraxAuthenticationForm(AuthenticationForm):
    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        return username



def login_view(request):
    resp = auth_views.login(request, authentication_form=TraxAuthenticationForm)
    if request.user.is_authenticated():
        resp.set_cookie('username', request.user.username)
    return resp

