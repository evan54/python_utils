import pandas as pd
from matplotlib import pyplot as plt

def stacked_bar_chart(sr, normalise=True, ascending=True, index=None, ax=None):
    '''
    The point of this function is to create a chart similar to a pie chart but linearly
    This will create a stacked bar chart with values placed on top of eachother in ascending
    or descending order, and annotate according to the sr.index value or the index value if 
    passed.
    
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
