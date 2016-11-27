import django
django.setup()

from django.contrib.auth.models import AnonymousUser

# from argparse import ArgumentParser as _ArgumentParser
import time
from players.models import find_player_by_dict, get_volatile_player

from . import settings

import ts3

# class ArgumentParser(_ArgumentParser):
#     def exit(self, status=0, message=None):
#         return

class Event:
    """Creates a Python object based on a teamspeak event.
    player = a (possibly volatile) player
    command = the bot command issued
    msg = the message received. (without a possible ".bot ")
    target = settings.CLIENT or settings.CHANNEL
    session = the session for the player"""
    def __init__(self, tsevent):
        self.player = find_player_by_dict(tsevent)
        msg = tsevent['msg']
        if msg.startswith(settings.BOT_INVOCATION):
            msg = msg[len(settings.BOT_INVOCATION)-1:].strip()
        parts = msg.split()
        self.command = parts[0]
        self.message = parts[1:]
        self.target = tsevent['targetmode']


class BotError(Exception):
    pass

class Channel:
    channel_name = None
    cid = None

    def __init__(self, parent, name=None, cid=None):
        self.parent = parent
        if cid:
            self.cid = cid
            self.channel_name = self.info('channel_name')
        else:
            self.channel_name = name
            for channel in self.parent.connection.channellist():
                if channel['channel_name'] == name:
                    self.cid = channel['cid']
                    break
            if not self.cid:
                raise BotError("ERROR: Did not find channel {0}.".format(
                    settings.DEFAULT_CHANNEL))

    def info(self, property=None):
        cinfo = self.parent.connection.channelinfo(cid=self.cid)
        if property:
            return cinfo.get(property)
        else:
            return cinfo

    def _get_users(self):
        pass


class Input:
    """A nice python object containing player (Player object), target ("1","2"),
    text (the teamspeak message text), channel_id (Teamspeak cid),
    client_id (Teamspeak cid)
    """
    pass


class Output:
    """A text to return to Teamspeak Server, a target ("1", "2"), and
    message_mode to deliver ("1"=chat, "2"=poke)
    """
    target = None
    text = None
    message_mode = None


class Bot:
    """Das ist Martins BROBot."""
    connection = None
    def __init__(self):
        self.plugins = []
        for plugin in settings.PLUGINS:
            self.plugins.append(plugin(self))
        self.setup_connection()

    def __del__(self):
        if self.connection:
            self.connection.quit()

    def send_channel_message(self, msg):
        self.connection.sendtextmessage(msg=msg, targetmode=settings.CHANNEL,
                                        target=self.channel.cid)

    def send_private_message(self, client_id, msg):
        self.connection.sendtextmessage(msg=msg, targetmode=settings.CLIENT,
                                        target=client_id)

    def get_channel_players(self):
        """return volatile Player objects of all clients in the current channel."""
        playerlist = []
        for x in self.connection.clientlist():
            if x['client_nickname'] == settings.BOT_NAME:
                continue
            if x['cid'] != self.channel.cid:
                continue

            playerlist.append(get_volatile_player(x['client_nickname'],
                                                  x['clid']))
        # TODO sort playerlist
        return playerlist

    def run(self):
        current_user = None
        self.connection.servernotifyregister(event="textchannel",
                                             id_=self.channel.cid)
        self.connection.servernotifyregister(event="textprivate")
        do_loop = True
        while do_loop:
            tsevent = self.connection.wait_for_event(timeout=50)
            for edict in tsevent.parsed:  # may be multiple lines
                if edict['invokername'] == settings.BOT_NAME:
                    continue
                event = Event(edict)
                if event.message == '.halt':
                    self.send_channel_message("Bye bye.")
                    do_loop = False
                    continue
                for plugin in self.plugins:
                    if event.message.startswith(plugin.cmd):
                        event.message = event.message[len(plugin.cmd):]
                        target, msg = plugin.process(event)
                        if msg:
                            if target == settings.CLIENT:
                                self.send_private_message(
                                    event.player.current_clid, msg)
                            else:
                                self.send_channel_message(msg)


    def setup_connection(self):
        self.connection = ts3.query.TS3Connection(settings.SERVER)
        self.connection.use(sid=settings.SERVER_ID)
        self.connection.login(client_login_name=settings.BOT_NAME,
                              client_login_password=settings.BOT_PASSWORD)

        self.channel = None
        if settings.DEFAULT_CHANNEL:
            self.channel = Channel(self, name=settings.DEFAULT_CHANNEL)

        self.connection.clientupdate(client_nickname=settings.BOT_NAME)
        self.botuser = None
        for x in self.connection.clientlist():
            if x['client_nickname'] == settings.BOT_NAME:
                self.botuser = x
        if self.botuser is None:
            raise BotError("ERROR: Did not find myself in the userlist!")
        if settings.DEFAULT_CHANNEL:
            self.connection.clientmove(clid=self.botuser['clid'],
                                       cid=self.channel.cid)

