from warnings import warn
import numpy as np
from matplotlib.patches import Polygon
from .tools import axes_helper

def log_hist(x, bins=20, axes=None, histtype="step", **hist_args):
    """Make a histogram with log-spaced binning.

    Wrapper around `pyplot.hist()` to make log-scale binned histogramming
    easier. (This is not equivalent to `pyplot.hist()`'s `log=True` keyword.

    See also
    --------
    pyplot.hist

    Parameters
    ----------
    x : array-like
        Data passed to `pyplot.hist`.
    bins : int, array-like, optional
        The number of bins or the binning edges.
    axes : optional
        The matplotlib `Axes` to plot to.
    histtype : str
        The histogram type.
    hist_args : optional
        Passed directly through to `pyplot.hist()`.

    Returns
    -------
    n, bins, patches :
        The return values of `pyplot.hist()`.
    """
    x = np.asarray(x)
    axes = axes_helper(axes)
    if type(bins) == int:
        # Fix numerical(?) issue with the binning edges.
        x0 = x.min() * (1-1e-9)
        x1 = x.max() * (1+1e-9)
        bins = np.logspace(np.log10(x0), np.log10(x1),
                           bins + 1)
    return axes.hist(x, bins, histtype=histtype, **hist_args)


def uoflow_hist(x, low=None, high=None, axes=None, *args, **kwargs):
    """Make histogram with under-/overflow bins.

    See also
    --------
    pyplot.hist

    Parameters
    ----------
    x : array-like
        Data passed to `pyplot.hist`.
    low, high : float, optional
        The under-/overflow limits.
    axes : optional
        The matplotlib `Axes` to plot to.
    hist_args : optional
        Passed directly through to `pyplot.hist()`.

    Returns
    -------
    n, bins, patches :
        The return values of `pyplot.hist()`.
    """
    if low is None and high is None:
        warn("Calling bounded_hist without bounds.")
    if kwargs.get("normed", False):
        warn("Normed bounded histograms not implemented!")

    axes = axes_helper(axes)

    n_under = 0
    n_over = 0
    i_low = True
    i_high = True

    if low is not None:
        i_low = low <= x
        n_under = (~i_low).sum()

    if high is not None:
        i_high = x < high
        n_over = (~i_high).sum()

    idx = i_low & i_high
    n, edges, patches = axes.hist(x[idx], *args, **kwargs)

    if n_under:
        width = edges[1] - edges[0]
        poly = Polygon([[low-width, 0],
                        [low-width, n_under],
                        [low, n_under],
                        [low, 0]],
                       closed=False
                       )
        poly.update_from(patches[-1])
        axes.add_patch(poly)
    if n_over:
        width = edges[-1] - edges[-2]
        poly = Polygon([[high, 0],
                        [high, n_over],
                        [high + width, n_over],
                        [high + width, 0]],
                       closed=False
                       )
        poly.update_from(patches[-1])
        axes.add_patch(poly)

    return n, edges, patches
