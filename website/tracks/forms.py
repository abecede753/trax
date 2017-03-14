from django.forms import ModelForm, ModelMultipleChoiceField, \
    CheckboxSelectMultiple

from easy_thumbnails.widgets import ImageClearableFileInput
from events.models import StaggeredStartRace
from vehicles.models import VehicleClass
from .models import Track, Laptime


class TrackForm(ModelForm):
    car_classes = ModelMultipleChoiceField(widget=CheckboxSelectMultiple,
                                           required=True, queryset=VehicleClass.objects.all(),
                                           )
    class Meta:
        model = Track
        fields = [
            'title', 'description', 'author', 'link', 'video', 'game_mode',
            'route_type', 'route_length_km', 'num_players', 'typical_laptime',
            'pit_lane', 'surface_street', 'surface_road',
            'surface_dirt', 'surface_flat', 'surface_stunt', 'surface_offroad',
            'elevation_changes', 'car_classes', 'platform',
            'image',
        ]
        widgets = {
            'image': ImageClearableFileInput(),
        }



class SSRCreateForm(ModelForm):
    class Meta:
        model = StaggeredStartRace
        fields = ["vehicle_class", "algorithm", "laps", "track", "comment"]
