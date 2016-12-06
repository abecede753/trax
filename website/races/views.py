from django.shortcuts import render
from django import forms
from .models import Race

# Create your views here.

class RaceCreateForm(forms.ModelForm)
    class Meta:
        model = Race
        fields = ['track', 'laps', 'comment',]


def RaceCreate(CreateView):
    model = Race
    form_class=RaceCreateForm
