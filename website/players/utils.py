import base64
from Crypto.Cipher import AES
import datetime
import numpy as np

from tracks.models import Laptime

AKEY = '8fwmn3tx8e..DS2y'
IV = b'e\xdbg\xf1\xcfT"\xc8\x96\xb4\xe2jC\'\xc8\xd1'


def encode(message):
    message = '{0}|{1}'.format(datetime.datetime.now().isoformat,
                               message)
    obj = AES.new(AKEY, AES.MODE_CFB, IV)
    return base64.urlsafe_b64encode(obj.encrypt(message.encode('utf-8')))


def decode(cipher):
    obj2 = AES.new(AKEY, AES.MODE_CFB, IV)
    message = obj2.decrypt(base64.urlsafe_b64decode(cipher)).decode('utf-8')
    return '|'.join(message.split('|')[1:])


def update_player_racing_stats(player, commit=True):
    # select all different vehicle/track combinations, keeping only the
    # fastest
    # if there are less than 8 entries, use standard schema.

    laptimes = list(Laptime.objects.filter(
        player=player).select_related(
        'vehicle').order_by('-recorded', '-created'))[:15]
    if len(laptimes) < 8:
        player.defaultspeedmultiplier = 1.0
    else:
        millpkm_user = 0
        millpkm_cc = 0
        allmultipliers = []
        for lt in laptimes:
            millpkm_user += lt.millis_per_km
            millpkm_cc += lt.vehicle.cc_millis_per_km
            allmultipliers.append(
                1 / lt.vehicle.cc_millis_per_km * lt.millis_per_km)

        clean_multipliers = remove_outliers(allmultipliers)

        # if someone is way too slow, make him "faster"
        player.defaultspeedmultiplier = min(1.06, (sum(clean_multipliers)
                                            / len(clean_multipliers)))
    if commit:
        player.save()


def is_outlier(points, thresh=3.5):
    """
    Returns a boolean array with True if points are outliers and False
    otherwise.

    Parameters:
    -----------
        points : An numobservations by numdimensions array of observations
        thresh : The modified z-score to use as a threshold. Observations with
            a modified z-score (based on the median absolute deviation) greater
            than this value will be classified as outliers.

    Returns:
    --------
        mask : A numobservations-length boolean array.

    References:
    ----------
        Boris Iglewicz and David Hoaglin (1993), "Volume 16: How to Detect and
        Handle Outliers", The ASQC Basic References in Quality Control:
        Statistical Techniques, Edward F. Mykytka, Ph.D., Editor.
    """
    if isinstance(points, list):
        points = np.array(points)
    if len(points.shape) == 1:
        points = points[:, None]
    median = np.median(points, axis=0)
    diff = np.sum((points - median)**2, axis=-1)
    diff = np.sqrt(diff)
    med_abs_deviation = np.median(diff)
    modified_z_score = 0.6745 * diff / med_abs_deviation
    return modified_z_score > thresh


def remove_outliers(lst):
    """
    returns a new list which has no outliers anymore.
    TODO: this is just copypasta... find some time to learn it and simplify
    the whole "remove_outliers/is_outlier" mumbojumbo.
    """
    clean_results = []
    outliers = is_outlier(lst)
    for x in range(len(lst)):
        if not outliers[x]:
            clean_results.append(lst[x])
    return clean_results
