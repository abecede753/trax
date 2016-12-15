from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager
from django.db import models
from django.utils.translation import ugettext_lazy

from trax.utils import get_object_by_string

class PlayerNotFound(Exception):
    pass

class TSUId(models.Model):
    ts_uid = models.CharField(max_length=512)
    player = models.ForeignKey("Player", null=True)

    def __str__(self):
        return self.ts_uid

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
    current_client_id = None  # for teamspeak. volatile.
    username = models.CharField(max_length=256, unique=True,
                                help_text=ugettext_lazy(
                                    "Please use your RSC name."))
    nickname = models.CharField(max_length=512, default='')  # TS nickname
    communication = models.TextField(null=True, default='')  # current TS communication. the plugin takes care of the content.
    is_staff = models.BooleanField(default=False)
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'username'

    objects = UserManager()

    def __str__(self):
        if self.username:
            return self.username
        return self.nickname


def find_player_by_dict(d):
    """Returns a player object based on a teamspeak event dict.
    If nothing fitting was found, it's just an
    in-memory Player object with the available data."""

    player = get_object_by_string(d['invokeruid'], Player,
                                  'ts_uid', score_cutoff=99) or \
             get_object_by_string(d['invokername'], Player,
                                  'nickname', score_cutoff=70)

    if not player:
        player = Player()
        player.is_authenticated = False
        player.username = ''
        player.nickname = d['invokername']
        player.ts_uid = d['invokeruid']

    player.current_client_id = d['invokerid']
    return player


def register(self, rscname, nickname, ts_uid):
    player = Player(rscname=rscname, nickname=nickname,
                    ts_uid=ts_uid)
    player.save()

def get_volatile_player(nickname, client_id):
    p = Player(nickname=nickname)
    p.current_client_id = client_id
    return p
