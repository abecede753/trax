from fuzzywuzzy import fuzz, process
from random import choice
from tabulate import tabulate

from vehicles.models import VehicleClass, Vehicle
from bot.settings import CHANNEL, CLIENT


class Car:
    """choose a random car"""
    cmd = 'car '
    help_text = 'Choose a random car for everyone in the channel. Use with "car coupes|sports"'

    def __init__(self, parent):
        self.parent = parent
        self.all_vehicles = {}
        self.all_vehicle_class_names = []
        for c in VehicleClass.objects.all():
            self.all_vehicle_class_names.append(c.name)
            self.all_vehicles[c.name] = [ x.name for x in c.vehicle_set.all()]

    def process(self, event):

        vehicle_class, certainty = process.extractOne(
            event.message, self.all_vehicle_class_names,
            scorer=fuzz.token_set_ratio, score_cutoff=80)

        table = []
        players = self.parent.get_channel_players()

        for c in players:
            table.append((c.nickname, choice(self.all_vehicles[vehicle_class])))
        headers = ["Name", "Fahrzeug"]
        return (CHANNEL, ' \n{0}'.format(
            tabulate(table, headers, tablefmt="orgtbl")))


