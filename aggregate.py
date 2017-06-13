import pandas as pd

def calc_cumsum_hist(arr):
    sr = pd.Series(arr)
    return sr.value_counts().sort_index().cumsum() / sr.shape[0]

def pd_summary(df, kwargs):
    return (df.groupby(lambda x: 0)
            .agg({col: kwargs for col in df.columns})
            .iloc[0].unstack().T)
