import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker


def stacked_bar_chart(sr, normalise=True, ascending=True, index=None, ax=None):
    '''
    The point of this function is to create a chart similar to a pie chart 
    but linearly.
    This will create a stacked bar chart with values placed on top of 
    eachother in ascending or descending order, and annotate according to 
    the sr.index value or the index value if passed.
    
        sr : input series
        normalise : whether to normalise the values of sr such that they add to 100
                    default is True
        ascending : whether to sort the values of the sr in ascending or descending order
                    default is True
        index : use this value as the index for the sr. If sr is a list then this is used otherwise
                it will default to range(len(sr))
    '''
    
    sr = pd.Series(sr)
    if index:
        sr.index = index
    if ax is None:
        plt.figure()
        ax = plt.gca()
    sr = sr.sort_values(ascending=ascending)
    if normalise:
        sr *= 100. / sr.sum()
    ax = sr.to_frame().T.plot.bar(stacked=True, legend=False, ax=ax)
    yloc = 0.
    xloc = 0.25
    xloc_diff = 0.1
    yloc_diff = 0.25
    text_height = 5 * sr.sum() / 100.
    ytext = 0.
    for name, value in sr.iteritems():
        yloc += value/2.
        ytext = max(ytext + text_height, yloc)
        if normalise:
            s = '{:.0f}% {}'.format(value, name)
        else:
            s = '{:.2f} {}'.format(value, name)
        ax.annotate(s, xy=(xloc, yloc), xytext=(xloc + xloc_diff, ytext),
                arrowprops=dict(headwidth=3, facecolor='black', shrink=0.002, width=2),
                verticalalignment='center'
                )
        yloc += value/2.
    plt.xlim(0., 1)
    return ax


def plot_dt(x, y, start_time, end_time, *args, plot_jump_loc=True, **kwargs):
    x = pd.to_datetime(pd.Series(x))
    time = x - x.dt.normalize()
    ind = (time >= start_time) & (time <= end_time)
    x = x[ind]
    y = y[ind]
    time = time[ind]

    epoch = pd.Timestamp('19700101')
    jump_timedelta = start_time - end_time + pd.Timedelta(hours=24)

    jump_locations = time.diff().dt.total_seconds() < 0
    jump_counts = jump_locations.cumsum()
    x_ = x - jump_counts * jump_timedelta

    day_jumps = x_.diff().fillna(0).dt.total_seconds() // (24*60*60)
    x_ = x_ - pd.Timedelta(days=1) * day_jumps.cumsum()

    xp = mdates.date2num(x_)
    fp = mdates.date2num(x)

    def custom_date_format(val, pos):
        f_val = np.interp(val, xp, fp)
        d_val = mdates.num2date(f_val)
        return d_val.strftime('%Y-%m-%d %H:%M')

    formatter = matplotlib.ticker.FuncFormatter(custom_date_format)
    ax = plt.gca()
    ax.xaxis.set_major_formatter(formatter)
    plt.xticks(rotation=45, ha='right')
    plt.plot(x_, y, *args, **kwargs)
    if plot_jump_loc:
        x_day_jumps = x_[day_jumps.shift(-1) > 0]
        ylim = plt.ylim()
        for t in x_[jump_locations.shift(-1).fillna(False)]:
            if t in x_day_jumps.tolist():
                color = 'k'
            else:
                color = 'r'
            plt.plot([t]*2, ylim, color + '--')
