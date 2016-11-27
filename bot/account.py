from . import settings

WELCOME_MESSAGE = """
Hallo, wir kennen uns noch nicht, ich bin {0}, und wer bist du?
Schreib mir doch eine kurze Nachricht mit deinem SocialClub-Namen!
Tippe dazu folgendes ein:

account <DeinRSCName><ENTER>

(Wobei du anstelle von "<DeinRSCName>" natürlich deinen wirklichen
SocialClub Namen verwendest.)
Danach stehe ich dir gern stets zu Diensten!""".format(settings.BOT_NAME)

class Account:
    """Register"""
    cmd = '.account '
    help_text = '''Mit diesem Befehl kannst du dich bei mir registrieren,
damit ich dich später wiedererkennen kann.'''

    def __init__(self, parent):
        self.parent = parent

    def process(self, edict):
        txt = edict['msg']

        self.parent.send_channel_message(
            "Ergebnis: {0}{1}".format(sum(result), detail))

    def search_account(self, edict):
        pass


