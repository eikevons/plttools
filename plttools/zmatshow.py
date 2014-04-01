from matplotlib.backend_bases import cursors as _cursors

def install_toolbar_message(canvas, msgfunc):
    toolbar = canvas.toolbar
    def my_on_mouse_move(event):
        if not event.inaxes or not toolbar._active:
            if toolbar._lastCursor != _cursors.POINTER:
                toolbar.set_cursor(_cursors.POINTER)
                toolbar._lastCursor = _cursors.POINTER
        else:
            if toolbar._active=='ZOOM':
                if toolbar._lastCursor != _cursors.SELECT_REGION:
                    toolbar.set_cursor(_cursors.SELECT_REGION)
                    toolbar._lastCursor = _cursors.SELECT_REGION
            elif (toolbar._active=='PAN' and
                  toolbar._lastCursor != _cursors.MOVE):
                toolbar.set_cursor(_cursors.MOVE)

                toolbar._lastCursor = _cursors.MOVE

        # if event.inaxes and event.inaxes.get_navigate():
        if event.inaxes:
            try:
                msg = msgfunc(event)
            except ValueError: pass
            except OverflowError: pass
            else:
                if len(toolbar.mode):
                    toolbar.set_message('%s, %s' % (toolbar.mode, msg))
                else:
                    toolbar.set_message(msg)
        else: toolbar.set_message(toolbar.mode)

    event_type = 'motion_notify_event'
    # Heuristically disconnect the old motion_notify_event to reduce
    # flickering
    # if [4] == canvas.callbacks.callbacks[event_type].keys():
        # print "disconnecting old '%s' callback" % event_type
        # canvas.mpl_disconnect(4)
    # and install our function.
    canvas.mpl_connect(event_type, my_on_mouse_move)


def mk_mat_toolbar_message(mat):
    def msgfunc(event):
        x = int(round(event.xdata))
        y = int(round(event.ydata))
        s = mat.shape
        if 0 <= x < s[1] and 0 <= y < s[0]:
            z = mat[y, x]
            msg = "x=%d  y=%d  z=%-12g" % (x, y, z)
        else:
            msg = "x=%d  y=%d" % (x, y)

        return msg
    return msgfunc


def zmatshow(A, msgfunc=None, ax=None, **kwargs):
    """Call `pyplot.matshow` and install an improved toolbar message function."""
    if ax is None:
        from matplotlib import pyplot
        ax = pyplot.gca()
    aimg = ax.matshow(A, **kwargs)

    if msgfunc is None:
        print "Setting default toolbar message"
        msgfunc = mk_mat_toolbar_message(A)
    install_toolbar_message(aimg.figure.canvas, msgfunc)
    return aimg
