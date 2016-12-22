import json

from django.core.management.base import BaseCommand
from vehicles.models import VehicleClass, Vehicle

TRANS = {'Compacts': 'Compact', 'Coupes': 'Coupe',
         'Motorcycles': 'Motorcycle', 'Muscle': 'Muscle',
         'Off-Road': 'Offroad', 'Sedans': 'Sedan',
         'Sports': 'Sport', 'Sports Classics': 'Sports_Classic',
         'Supers': 'Super', 'SUVs': 'SUV', 'Vans': 'Van'}


class Command(BaseCommand):
    help = 'Imports the vehicle txt files.'

    def handle(self, *args, **options):

        with open('vehicles/management/commands/'
                  'cars_classes_millis_stockinfo.json', 'r') as f:
            js = json.load(f)

        for car in js:
            clsname = TRANS.get(car['vclass'], car['vclass'])
            vc, created = VehicleClass.objects.get_or_create(name=clsname)
            if created:
                vc.save()
            print(car['name'])
            if car['name'].endswith(' (stock)'):
                car['name'] = car['name'][:-8]
            v, c = Vehicle.objects.get_or_create(name=car['name'])
            if car.get('stock'):
                v.cc_millis_per_km_stock = convert_millis_lap(car['time'])
            else:
                v.cc_millis_per_km = convert_millis_lap(car['time'])
            v.save()
            v.classes.add(vc)

        # delete cirrus stuff
        Vehicle.objects.filter(name='Picador (Cirrus5005)').delete()


def convert_millis_lap(n):
    n = n / 2.59
    # n = n / 1000.0
    return n
