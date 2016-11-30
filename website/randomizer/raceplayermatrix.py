import json
import os
from random import shuffle

_DATADIR = os.path.dirname(__file__)

def create_grid(num_races, playerlist):
    if num_races < 2 or num_races > 30:
        raise NotImplementedError('racelist only from 2 to 30 races possible.')

    try:
        with open(os.path.join(_DATADIR,
                               'data',
                               '{0}.json'.format(num_races)), 'r') as f:
            matrix = json.load(f)
    except:  # TODO (better exception handling)
        raise NotImplementedError('could not open the json matrix file.')

    grids = matrix.get('{0}'.format(len(playerlist)), None)
    if not grids:
        raise NotImplementedError('players only from 2 to 30 available.')

    shuffle(grids)
    shuffle(playerlist)
    result = []
    for grid in grids:
        result.append( [playerlist[x] for x in grid])
    return result
