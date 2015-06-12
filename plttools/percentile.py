import numpy as np
from .tools import axes_helper, kw_helper, repeat_dictentries

def percentile_plot(x, y, q=None, axes=None, labels=False, label_props=None, label_pos='plot', **line_kwargs):
    """Plot percentile lines for data `y`.

    The percentiles are calculated with np.percentile.

    Paramteters
    -----------
    x : 1dim ndarray, None
        If not `None`, the x-values used for plotting.
    y : 2dim ndarray
        The data. The percentiles are calculated along the second axis
        (axis=1). If `x` is not `None` `x` and `y` must have the same first
        dimension.
    q : list of floats, optional
        The percentiles to plot. Default is to plot the 5%, 50% and 95% percentiles, i.e. `q = [5, 50, 95]`.
    axes : optional
        The matplotlib `Axes` to plot to.
    labels : bool or list, optional
        If `True` add a text label indicating the percentile to each line.
        If a `list` it contains the label text (must have the same length as
        `q`).
    label_props : dict, optional
        If given, it is passed to `Axes.annotate()`. The special key
        "xscale" can be used to control the x-position of the labels.
    label_pos : str, optional
        Where to put the labels::
            'plot' : annotate the lines in the plot (default)
            'legend' : in the legend box
            'both' : both
    line_kwargs : optional
        kwargs that are passed to matplotlib.plot. Each argument can be a
        list or tuple to define different styles for each percentile line.

    Examples
    --------
    >>> y = np.random.randn(20, 1000)

    # Plot 5%, 50% and 95% lines without labels.
    >>> percentile_plot(None, y=y)

    # Plot 20% and 80% lines with labels.
    >>> percentile_plot(None, y=y, q=(20, 80), labels=True)

    # Plot 20% and 80% lines with custom labels at the center of the x-axis.
    >>> percentile_plot(None, y=y, q=(20, 80), labels=('low', 'high'),
    ...                 label_props={'xscale' : 0.5, 'horizontalalignment' : 'center'})

    # Plot 20% and 80% lines with dashed magenta lines but different line widths.
    >>> percentile_plot(None, y=y, q=(20, 80), labels=('low', 'high'),
    ...                 linestyle='--', color='m', linewidth=[2, 6])
    """
    axes = axes_helper(axes)
    if q is None:
        q = [5, 50, 95]
    if x is not None and x.shape[0] != y.shape[0]:
        raise ValueError("x and y must have the same first dimension")
    elif x is None:
        x = np.arange(y.shape[0])

    if labels is True:
        labels = ["{0}".format(qi) for qi in q]
    if labels:
        label_props = kw_helper({"xscale":0.1}, label_props)
        i_label = int(label_props["xscale"] * y.shape[0])
        del label_props["xscale"]

    ps = np.percentile(y, q, axis=1)

    line_kwargs = repeat_dictentries(line_kwargs)
    for i, (p, kw) in enumerate(zip(ps, line_kwargs)):
        if label_pos in ('legend', 'both') and labels:
            axes.plot(x, p, label=labels[i], **kw)
        else:
            axes.plot(x, p, **kw)

        if label_pos in ('plot', 'both') and labels:
            axes.annotate(labels[i], (x[i_label], p[i_label]), **label_props)
