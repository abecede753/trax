from tracks.models import Laptime
from vehicles.models import Vehicle


class EventCar:
    user = None
    vehicle_pk = None
    stock = None
    seconds_per_km = None
    user_entry = None  # is this a user created entry? (or broughy?)

    def __init__(self, user=None, vehicle_pk=None, stock=None,
                 seconds_per_km=None, user_entry = None, name=None):
        self.user = user
        self.vehicle_pk = vehicle_pk
        self.stock = stock
        self.seconds_per_km = seconds_per_km
        self.user_entry = user_entry
        if not name:
            self.name = Vehicle.objects.get(pk=vehicle_pk).name
        else:
            self.name = name
        self.slug = '{0}.{1}.{2}'.format(self.vehicle_pk,
                                         self.user_entry and 1 or 0,
                                         self.stock and 1 or 0)

    @property
    def display_name(self):
        result = self.name
        if self.stock:
            result += ' (stock)'
        result += ' - {:.2f} sec/km'.format(self.seconds_per_km)

        return result


def get_eventcar(user=None, vehicle_pk=None, user_entry=None, stock=None):
    """returns an EventCar object based on the input given."""
    if user_entry == True:
        raise NotImplementedError
    v = Vehicle.objects.get(pk=vehicle_pk)
    seconds_per_km = stock and v.lsgp_seconds_per_km_stock or v.lsgp_seconds_per_km
    return EventCar(user=user, vehicle_pk=v.pk,
                    stock=stock, seconds_per_km=seconds_per_km,
                    user_entry=user_entry, name=v.name)


def get_eventcar_by_slug(user, slug):
    vehicle_pk, user_entry, stock = slug.split('.')
    return get_eventcar(user, int(vehicle_pk), bool(int(user_entry)),
                        bool(int(stock)))


def get_car_list(user, vehicle_class):
    result = []

    for lsgpstockvehicle in Vehicle.objects.filter(
            classes__in=[vehicle_class,],
            lsgp_seconds_per_km_stock__isnull=False,
    ):
        result.append(EventCar(
            user=user, vehicle_pk=lsgpstockvehicle.pk, stock=True,
            seconds_per_km=lsgpstockvehicle.lsgp_seconds_per_km_stock
        ))
    for lsgpvehicle in Vehicle.objects.filter(
        classes__in=[vehicle_class,],
            lsgp_seconds_per_km__isnull=False):
        result.append(EventCar(
            user=user, vehicle_pk=lsgpvehicle.pk, stock=False,
            seconds_per_km=lsgpvehicle.lsgp_seconds_per_km
        ))


    sorted_result = sorted(result, key=lambda x: x.display_name)

    # create three parts for better display
#    rowcount = int(len(sorted_result) / 3)

#    p1 = sorted_result[:rowcount]
#    p2 = sorted_result[rowcount:rowcount*2]
#    p3 = sorted_result[rowcount*2:]
#    return [p1, p2, p3]
    rowcount = int(len(sorted_result) / 2)

    p1 = sorted_result[:rowcount]
    p2 = sorted_result[rowcount:]
    return [p1, p2]


#    userstocks = Laptime.objects.filter(
#        player=user, vehicle__classes__name__contains=vehicle_class,
#        untuned=True)
#    usercustoms = Laptime.objects.filter(
#        player=user, vehicle__classes__name__contains=vehicle_class,
#        untuned=False)
