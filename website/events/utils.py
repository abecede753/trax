from tracks.models import Laptime
from vehicles.models import Vehicle


class EventCar:
    user = None
    vehicle = None
    stock = None
    millis_per_km = None
    user_entry = None  # is this a user created entry? (or broughy?)

    def __init__(self, user=None, vehicle=None, stock=None,
                 millis_per_km=None, user_entry = None, name=None):
        self.user = user
        self.vehicle = vehicle
        self.stock = stock
        self.millis_per_km = millis_per_km
        self.user_entry = user_entry
        if not name:
            self.name = self.vehicle.name
        else:
            self.name = name
        self.slug = '{0}.{1}.{2}'.format(self.vehicle.pk,
                                         self.user_entry and 1 or 0,
                                         self.stock and 1 or 0)

    @property
    def display_name(self):
        result = self.name
        if self.stock:
            result += ' (stock)'
        result += ' - {:.3f} sec/km'.format(self.millis_per_km/1000.0)

        return result


def get_user_car_list(user, vehicle_class):
    """a participant can choose from these cars when joining an event.
    also split into two lists for better html display."""
    result = []

    for lsgpstockvehicle in Vehicle.objects.filter(
            classes__in=[vehicle_class,],
            lsgp_millis_per_km_stock__isnull=False,
    ):
        result.append(EventCar(  # TODO XXX NOTE NOW
            user=user, vehicle=lsgpstockvehicle, stock=True,
            millis_per_km=lsgpstockvehicle.lsgp_millis_per_km_stock
        ))
    for lsgpvehicle in Vehicle.objects.filter(
        classes__in=[vehicle_class,],
            lsgp_millis_per_km__isnull=False):
        result.append(EventCar(
            user=user, vehicle=lsgpvehicle, stock=False,
            millis_per_km=lsgpvehicle.lsgp_millis_per_km
        ))
    sorted_result = sorted(result, key=lambda x: x.display_name)
    rowcount = int(len(sorted_result)/2)
    p1 = sorted_result[:rowcount]
    p2 = sorted_result[rowcount:]
    return [p1, p2]
