import pandas as pd

from glue import custom_viewer
from glue.core.subset import RoiSubsetState, CategorySubsetState

timelines = pd.read_csv('timelines.csv').set_index(['run_id', 'time']).unstack()

mario = custom_viewer('Mario Plot',
                      time=(0, 1580),
                      run=(0, 110),
                      x='att(x)',
                      y='att(y)',
                      full_path=False)
mario.redraw_on_settings_change = False


@mario.setup
def setup(axes):
    from skimage.io import imread
    bg = imread('bg.png')
    axes.imshow(bg, origin='upper',
                extent=[0, bg.shape[1] / 16, bg.shape[0] / 16, 0])
    axes.set_aspect('equal', adjustable='datalim')


@mario.settings_changed
def settings_changed(axes, time, run):
    sub = timelines.iloc[run]
    axes.plot(sub.x, sub.y, 'r',
              [sub.x.values[time]], [sub.y.values[time]], 'ko',
              lw=3, ms=20)


@mario.plot_subset
def plot_subset(axes, x, y, style):
    axes.plot(x.values, y.values, mec='none', mfc=style.color,
              alpha=style.alpha, marker=style.marker,
              ms=style.markersize, ls='none')


@mario.make_selector
def make_selector(roi, full_path):
    if full_path:
        hit = roi.contains(timelines['x'], timelines['y']).any(axis=1)
        rids = timelines[hit].index.unique()
        return CategorySubsetState('run_id', rids)

    state = RoiSubsetState()
    state.xatt = 'x'
    state.yatt = 'y'
    state.roi = roi
    return state
