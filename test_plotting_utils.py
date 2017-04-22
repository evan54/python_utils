import pandas as pd
from matplotlib import pyplot as plt

import unittest

from plotting_utils import stacked_bar_chart

class TestPlotUtils(unittest.TestCase):

    def test_list(self):
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
            self.assertEqual(rec_list.get_xy(), rec_series.get_xy(), 
                    'values equal')

if __name__ == '__main__':
    unittest.main()
