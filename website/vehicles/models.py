from django.db import models


class VehicleClass(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    name = models.CharField(max_length=256)
    classes = models.ManyToManyField("vehicles.VehicleClass")
    lsgp_millis_per_km = models.IntegerField(null=True)
    lsgp_millis_per_km_stock = models.IntegerField(null=True)

    class Meta:
        ordering=['classes__name', 'name']
    def __str__(self):
        return self.full_name()

    def full_name(self):
        return '{0} ({1})'.format(
            self.name,
            ', '.join([x.name for x in self.classes.all()]))

