import os
print(os.getcwd())
import pandas as pd
import numpy as np
from python_utils.aggregate import calc_cumsum_hist
from python_utils.aggregate import pd_summary

def test_calc_cumsum_hist():
    # check example
    arr = [0, 0, 0, 2, 3, 4, 4]
    l = len(arr)
    res = pd.Series(index=[0, 2, 3, 4], data=[3/l, 1/l, 1/l, 2/l]).cumsum()
    fun_res = calc_cumsum_hist(arr)
    assert np.allclose(res, calc_cumsum_hist(arr)), 'Values are not correct'
    assert np.allclose(fun_res.index, res.index), 'Index is not correct'

    # check edge case of single length
    assert np.allclose(1, calc_cumsum_hist([0]))

def test_pd_summary():
    df = pd.DataFrame(data=np.arange(12).reshape([3, 4]))
    kwargs = {'max': max, 'min': min}
    df_describe = df.describe()
    df_custom = pd_summary(df, kwargs)
    print(df_describe)
    print(df_custom)
    for i_row, row in df_custom.iterrows():
        assert np.allclose(df_describe.loc[i_row], row), 'Error vs .describe method'
