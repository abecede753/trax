from django.db import models
from django.urls import reverse


class VehicleClass(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    name = models.CharField(max_length=256)
    classes = models.ManyToManyField("vehicles.VehicleClass")
    cc_laptime_millis = models.IntegerField(null=True)
    cc_millis_per_km = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering=['name', ]

    def __str__(self):
        return self.full_name()

    def save(self, *a, **k):
        if self.cc_laptime_millis:
            self.cc_millis_per_km = self.cc_laptime_millis / 2.59
        super(Vehicle, self).save(*a, **k)

    def full_name(self):
        return '{0} ({1})'.format(
            self.name,
            ', '.join([x.name for x in self.classes.all()]))

    @property
    def secs_per_km(self):
        if self.cc_millis_per_km != 0:
            return '{:.3f}'.format(self.cc_millis_per_km/1000.0)
        return ''

    @property
    def km_per_h(self):
        if self.cc_millis_per_km != 0:
            return '{:.3f}'.format(
                (1.0 / self.cc_millis_per_km ) * 1000 * 3600
            )
        return '?'

    def get_absolute_url(self):
        return reverse('vehicle_detail', args=[str(self.pk)])
