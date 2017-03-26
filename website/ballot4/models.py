from django.db import models

class Ballot4(models.Model):
    """A ballot4 is used for TEPCOTT to decide on one of four racetracks."""
    title = models.CharField(unique=True, max_length=256)
    description = models.TextField(blank=True, default='')
    creator = models.ForeignKey("players.Player", null=True)
    created = models.DateField(auto_now_add=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    c1 = models.CharField(max_length=256)
    c2 = models.CharField(max_length=256)
    c3 = models.CharField(max_length=256)
    c4 = models.CharField(max_length=256)


class Vote4(models.Model):
    ballot4 = models.ForeignKey("Ballot4")
    user = models.ForeignKey("players.Player")
    c1 = models.SmallIntegerField()
    c2 = models.SmallIntegerField()
    c3 = models.SmallIntegerField()
    c4 = models.SmallIntegerField()
