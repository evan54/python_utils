from python_utils.plotting_utils import stacked_bar_chart

import pandas as pd
from matplotlib import pyplot as plt

def test_list():
    index = ['a', 'b', 'c']
    l = range(3)
    sr = pd.Series(index=index, data=l)
    ax_list = stacked_bar_chart(l, index=index)
    recs_list = [x for x in ax_list.get_children()
            if isinstance(x, plt.Rectangle)]
    ax_series = stacked_bar_chart(sr)
    recs_series = [x for x in ax_series.get_children()
            if isinstance(x, plt.Rectangle)]
    for rec_list, rec_series in zip(recs_list, recs_series):
        # self.assertEqual(rec_list.get_xy(), rec_series.get_xy(), 
        #         'values equal')
        assert rec_list.get_xy() == rec_series.get_xy()
