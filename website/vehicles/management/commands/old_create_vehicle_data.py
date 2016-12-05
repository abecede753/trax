import os

from django.core.management.base import BaseCommand, CommandError
from vehicles.models import VehicleClass, Vehicle

class Command(BaseCommand):
    help = 'Imports the vehicle txt files.'


    def handle(self, *args, **options):
        directory = "vehicles/management/commands/autodata"

        for fname in os.listdir(directory):
            if fname.endswith(".txt"):
                vc, created = VehicleClass.objects.get_or_create(name=fname[:-4])
                if created:
                    vc.save()
                with open(os.path.join(directory, fname)) as f:
                    for line in f:
                        v, c = Vehicle.objects.get_or_create(name=line.strip())
                        if c:
                            v.save()
                        v.classes.add(vc)


