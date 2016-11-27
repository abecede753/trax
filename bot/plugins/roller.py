from random import randrange
from bot.settings import CHANNEL, CLIENT


class Roller:
    """Roll some dice!"""
    cmd = 'roll '
    help_text = 'roll a die! e.g. 2d6 for two six-sided dice.'

    def __init__(self, parent):
        self.parent = parent

    def process(self, event):
        params = event.message.split()
        verbose = False
        msg_target = CHANNEL
        if '-v' in params:
            params.remove('-v')
            verbose = True
        if '-p' in params:
            params.remove('-p')
            msg_target = CLIENT
        response = []
        for roll in params:
            line = roll
            rolls = []
            num, eyes = roll.split('d')
            num = int(num)
            eyes = int(eyes)
            for idx in range(num):
                rolls.append(randrange(1, eyes + 1))
            line += ': {0}'.format(sum(rolls))
            if verbose:
                line += ' ({0})'.format(', '.join([str(x) for x in rolls]))
            response.append(line)
        return (msg_target, '\n'.join(response))


        # self.parent.send_channel_message("cannot parse your input. sorry.")
