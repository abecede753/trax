from captcha.fields import ReCaptchaField
from collections import OrderedDict

from django.contrib.auth import get_user_model, logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.forms import Form, ModelForm
from django import forms
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.contrib.auth.hashers import make_password

from players.models import Player
from tracks.models import Track, Laptime

_User = get_user_model()

# @method_decorator(login_required, name='dispatch')
class Homepage(TemplateView):
    template_name = "trax/homepage.html"

    def get_context_data(self, **kwargs):
        context = super(Homepage, self).get_context_data(**kwargs)
        tracks = Track.objects.all().order_by('-pk')[:10]
        context['tracks'] = tracks
        context['toplaps'] = self.get_top_laps()
        return context

    def get_top_laps(self, num_items=5):
        l = Laptime.objects.filter(
            vehicle__classes__name__in=('Sport', 'Super', 'Muscke')).order_by(
            'millis_per_km')
        tracks = {}
        for x in l:
            for cl in x.vehicle.classes.all():
                current_time = x.millis
                key = (x.track.pk, cl.pk)
                if (not tracks.get(key)) or (
                    current_time < tracks.get(key).millis):
                    tracks[key] = x
        ordered = OrderedDict(
            sorted(tracks.items(), key=lambda t: t[1].millis_per_km))
        return list(tracks.values())[:num_items]



class RegistrationForm(ModelForm):
    class Meta:
        model = Player
        fields = ['username']
    email = forms.EmailField(
        label=_("E-Mail"),
        help_text=_("You don't really need to enter an e-mail address. "
                    "Although it would help you in recovering your acccount "
                    "in case you should forget your password."),
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
        next_url = request.GET.get('next', '/')
        form = RegistrationForm()
        return render(request, self.template_name, {
            'form': form, 'next': next_url})

    def post(self, request, **kwargs):
        form = RegistrationForm(request.POST)
        next_url = request.POST.get('next', '/')
        if not form.is_valid():
            return render(request, self.template_name, {
                'form':form, 'next': next_url})
        user = Player(username=form.cleaned_data['username'],
                      email=form.cleaned_data['email'])
        user.set_password(form.cleaned_data['password1'])
        user.save()
        login(request, user)
        return HttpResponseRedirect(next_url)


@never_cache
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

def export_tables_as_sheets(request):
    qs = Laptime.objects.all().select_related('track', 'player', 'vehicle')
    column_names = ['pk', 'millis', 'millis_per_km', 'vehicle__name']
    return excel.make_response_from_query_sets(query_sets, column_names, 'xls',
                                               file_name="custom")




def timestamp_dev(request):
    """replacement for the little shell script returning the current datetime
    for the SSR creator."""
    from django.utils.timezone import now
    n = now()
    return HttpResponse('{0:.9f}'.format(n.timestamp()), content_type="text/plain")


