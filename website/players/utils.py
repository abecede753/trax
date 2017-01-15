from tracks.models import Laptime

import numpy as np


def update_player_racing_stats(player, commit=True):
    # use only the most recent 10 races  TODO parametrize "8"

    laptimes = list(Laptime.objects.filter(
        player=player).select_related(
        'vehicle').order_by('-recorded', '-created'))[:8]
    if not laptimes:
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
        player.defaultspeedmultiplier = (sum(clean_multipliers)
                                         / len(clean_multipliers))
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
        points = points[:,None]
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
