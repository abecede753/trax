import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'trax.settings'

from teamspeak_bot import Bot

b = Bot()
b.run()
