from itertools import repeat, cycle
import warnings
import numpy as np
import matplotlib


# Helper for plotting routines

def axes_helper(axes):
    """Return the current matplotlib axes if `axes` is `None`.

    Example
    -------
    >>> def my_plot_routine(data, ax=None):
    ...     ax = axes_helper(ax)
    ...     # [...]
    """
    if axes is None:
        from matplotlib import pyplot
        return pyplot.gca()
    return axes


def kw_helper(defaults, other=None):
    """Merge keyword arguments from `defaults` and `other`. `other` takes precedence."""
    d = defaults.copy()
    if other:
        d.update(other)
    return d


def share_axis(axes, sharex=False, sharey=False):
    """Share x- and/or y-axis for a list of Axes."""
    if not sharex and not sharey:
        warnings.warn("calling share_axis with sharex==False and sharey==False")
        return

    # Ensure that the axis are shared.
    sx = axes[0].get_shared_x_axes()
    sy = axes[0].get_shared_y_axes()
    for ax in axes[1:]:
        if sharex:
            sx.join(axes[0], ax)
            ax._sharex = axes[0]
        if sharey:
            sy.join(axes[0], ax)
            ax._sharey = axes[0]


def discretize_colormap(cmap, N):
    """Return a discrete colormap from the continuous colormap cmap.

    Parameters
    ----------
    cmap :
        colormap instance, eg. cm.jet.
    N : int
        Number of colors.

    Example
    -------
    >>> x = resize(arange(100), (5,100))
    >>> djet = discretize_colormap(cm.jet, 5)
    >>> imshow(x, cmap=djet)

    See
    ---
    http://www.scipy.org/Cookbook/Matplotlib/ColormapTransformations
    """
    # N colors
    colors_i = np.concatenate((np.linspace(0, 1., N), (0.0, 0.0, 0.0, 0.0)))
    colors_rgba = cmap(colors_i)
    # N+1 indices
    indices = np.linspace(0, 1., N+1)
    cdict = {}
    for ki, key in enumerate(('red','green','blue')):
        cdict[key] = [(indices[i], colors_rgba[i-1, ki], colors_rgba[i, ki]) for i in xrange(N+1)]
    # Return colormap object.
    return matplotlib.colors.LinearSegmentedColormap('discrete_colormap', cdict, 1024)


def repeat_dictentries(d):
    """Generate dictionaries repeating the entries in `d`.

    For each key-value pair in `d` a generator is created. If the value is a
    list or tuple it is cycled, otherwise the same value is repeated all the
    time.
    """
    gens = {}
    for k, v in d.items():
        if type(v) in (list, tuple):
            gens[k] = cycle(v)
        else:
            gens[k] = repeat(v)
    while True:
        yield {k: v.next() for k, v in gens.items()}
