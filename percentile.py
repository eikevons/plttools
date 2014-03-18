from tools import axes_helper, kw_helper, repeat_dictentries
import numpy as np

def percentile_plot(x, y, q=None, axes=None, labels=False, label_props=None, **line_kwargs):
    """Plot percentile lines for data `y`.

    Paramteters
    -----------
    x : 1dim ndarray, None
        If not `None`, the x-values used for plotting.
    y : 2dim ndarray
        The data. The percentiles are calculated along the second axis
        (axis=1). If `x` is not `None` `x` and `y` must have the same first
        dimension.
    q : list of floats, optional
        The percentiles to plot.
    axes : optional
        The matplotlib Axes to plot to.
    line_kwargs : optional
        kwargs that are passed to matplotlib.plot. Each argument can be a
        list or tuple to define different styles for each percentile line.
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
        label_props = kw_helper(label_props,
                {"xscale":0.1})
        i_label = int(label_props["xscale"] * y.shape[0])
        del label_props["xscale"]

    ps = np.percentile(y, q, axis=1)

    line_kwargs = repeat_dictentries(line_kwargs)
    for i, (p, kw) in enumerate(zip(ps, line_kwargs)):
        axes.plot(x, p, **kw)
        if labels:
            axes.annotate(labels[i], (x[i_label], p[i_label]), **label_props)
