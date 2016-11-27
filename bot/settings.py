from .local_settings import *

BOT_INVOCATION = '.bot '

CLIENT = '1'
CHANNEL = '2'


from .plugins.roller import Roller
from .plugins.car import Car

PLUGINS = [Roller, Car]

