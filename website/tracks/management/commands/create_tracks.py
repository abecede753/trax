import os

from django.core.management.base import BaseCommand, CommandError
from tracks.models import Track

class Command(BaseCommand):
    help = 'Create some tracks.'


    def handle(self, *args, **options):
        t, created = Track.objects.get_or_create(
            title="Pier 400",
            defaults={
                'game_mode': 'stunt',
                'route_type': 'l',
                'route_length_km': 5.28,
                'num_players': 30,
                'median_laptime': 180,
                'pit_lane': True,
                'surface_street': 30,
                'surface_flat': 40,
                'surface_stunt': 30,
                'elevation_changes': 5,
                'car_classes': ['Sedans', ]})
        t.save()

        t, created = Track.objects.get_or_create(
            title="Zancudo Madness",
            defaults={
            'game_mode': 'stunt',
            'route_type': 'l',
            'route_length_km': 3.52,
            'num_players': 30,
            'median_laptime': 69,
            'pit_lane': True,
            'surface_street': 0,
            'surface_flat': 60,
            'surface_stunt': 40,
            'elevation_changes': 20,
            'car_classes': ['Sports',]})
        t.save()
