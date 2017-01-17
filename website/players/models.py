from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager
from django.db import models
from django.utils.translation import ugettext_lazy
from .utils import update_player_racing_stats

from trax.utils import get_object_by_string

class PlayerNotFound(Exception):
    pass

class PlayerManager(UserManager):
    def _create_user(self, username, password, **extra_fields):
        """
        Creates and saves a User with the given username, password.
        """
        if not username:
            raise ValueError('The given username must be set')
        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)


class Player(AbstractBaseUser):
    username = models.CharField(max_length=256, unique=True,
                                help_text=ugettext_lazy(
                                    "Please use your RSC name."))
    nickname = models.CharField(max_length=512, default='')  # alternative form
    is_staff = models.BooleanField(default=False)
    email = models.EmailField(null=True)
    defaultspeedmultiplier = models.FloatField(default=1.0)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'username'
    objects = UserManager()

    def __str__(self):
        return self.nickname or self.username


def register(self, rscname, nickname, email):
    player = Player(rscname=rscname, nickname=nickname,
                    email=email)
    player.save()


class PlayerVehicle(models.Model):
    player = models.ForeignKey("players.Player")
    vehicle = models.ForeignKey("vehicles.Vehicle")
    multiplier = models.FloatField(default=1.0)


from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from tracks.models import Laptime

@receiver(post_save, sender=Laptime)
def lt_save_update_racing_stats(sender, instance=None, **kwargs):
    if instance:
        player = Player.objects.get(username=instance.player.username)
        update_player_racing_stats(player)


@receiver(post_delete, sender=Laptime)
def lt_save_delete_racing_stats(sender, instance=None, **kwargs):
    if instance:
        player = Player.objects.get(username=instance.player.username)
        update_player_racing_stats(player)

