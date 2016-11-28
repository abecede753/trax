from django.db import models
from django.forms import ModelForm

from .models import Track

class TrackForm(ModelForm):
    class Meta:
        model = Track
        fields = [
            'title', 'description', 'author', 'link', 'video', 'game_mode',
            'route_type', 'route_length_km', 'num_players', 'typical_laptime',
            'pit_lane', 'surface_street', 'surface_road', 'surface_highway',
            'surface_dirt', 'surface_flat', 'surface_stunt', 'surface_offroad',
            'elevation_changes', 'car_classes', 'platform'
        ]
