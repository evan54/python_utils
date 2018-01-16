import pandas as pd


def calc_cumsum_hist(arr):
    sr = pd.Series(arr)
    return sr.value_counts().sort_index().cumsum() / sr.shape[0]


def pd_summary(df, kwargs):
    return (df.groupby(lambda x: 0)
            .agg({col: kwargs for col in df.columns})
            .iloc[0].unstack().T)


def roll_multi(df, w, **kwargs):
    """
    Groupby multiple columns to allow apply function to be applied with multiple
    columns as inputs.
    
    Example:
    
    calculate the average of the open and the close.
    
        roll_multi(df, 2).apply(
            lambda x:
                (x['close'] * x['volume']).sum()
                / x['volume'].sum())
    """
    roll_array = np.dstack([df_t.values[i:i+w, :]
                            for i in range(len(df_t.index) - w + 1)]).T
    roll_array = roll_array.transpose([0, 2, 1]).reshape([-1, df_t.shape[1]])
    df_out = pd.DataFrame(roll_array,
                 index=pd.MultiIndex.from_product([df_t.index[w-1:], range(w)],
                                     names=[df_t.index.name, 'roll']),
                 columns=df_t.columns).head(10)
    return df_out.groupby(level=0, **kwargs)
