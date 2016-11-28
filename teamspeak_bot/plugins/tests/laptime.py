from django.test import TestCase

from teamspeak_bot.plugins import car
from teamspeak_bot import settings
from teamspeak_bot import get_volatile_player, Event
from tracks.management.commands import create_tracks
from vehicles.management.commands import create_vehicle_data
from django.core.management import call_command


edict = {'invokeruid':'adsf',
         'invokername': 'Nick1',
         'invokerid': 'invokerid',
         'targetmode': settings.CHANNEL}
class Parent:
    def get_channel_players(self):
        return [ get_volatile_player('Nick1', 'clid1'),
                 get_volatile_player('Nick2', 'clid2')]


class TC(TestCase):
    def setUp(self):
        call_command('create_tracks')
        call_command('create_vehicle_data')

    def test_car(self):
        mycar = car.Car(Parent())
        event = dict(edict)
        event['msg'] = 'sports'

        channel, output = mycar.process(Event(event))
        assert output.startswith(' \n| Name   | Fahrzeug') is True
        assert 'Nick1' in output
        assert 'Nick2' in output
        assert len(output.splitlines()) == 5
        assert channel == '2'
