from django import forms
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView
from .raceplayermatrix import create_grid


class RacelistForm(forms.Form):
    MAX_RACES = 30  # TODO - make dynamic according to randomizer/data/*json
    players = forms.CharField(widget=forms.Textarea())
    num_races = forms.IntegerField()
    player_list = None

    def clean_players(self):
        self.player_list = []
        for line in self.cleaned_data.get('players', '').splitlines():
            content = line.strip()
            if content:
                self.player_list.append(content)
        if not self.player_list:
            raise forms.ValidationError(
                _("Please enter at least two names.")
            )
        return '\n'.join(self.player_list)

    def clean_num_races(self):
        try:
            num_races = int(self.cleaned_data.get('num_races'))
        except:
            raise forms.ValidationError(
                _("please enter a number from 2 to {0}".format(self.MAX_RACES))
            )
        if num_races < 2 or num_races > self.MAX_RACES:
            raise forms.ValidationError(
                _("please enter a number from 2 to {0}".format(self.MAX_RACES))
            )
        return num_races


class Racelist(TemplateView):
    template_name = "randomizer/racelist.html"

    def get(self, request, **kwargs):
        form = RacelistForm()
        return render(request, self.template_name,
                      {'form': form, 'grids':None})

    def post(self, request, **kwargs):
        form = RacelistForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name,
                          {'form':form, 'grids': None})
        grids = create_grid(form.cleaned_data['num_races'], form.player_list)
        return render(request, self.template_name,
                      {'form': form, 'grids': grids})
