import pandas as pd
import numpy as np

# Weight of evidence (WOE)

def get_woe_dict(df, result, c, threshold=1e-03, n_min=100):

    mean_rate = df[result].mean()
    groups = df.groupby(by=c)
    dfx = pd.DataFrame()
    dfx['employees'] = groups.size()
    dfx['terminations'] = groups[result].sum()
    dfx['rate'] = dfx['terminations']/dfx['employees']
    dfx.loc[dfx['rate'] == 0, 'rate'] = threshold
    dfx['r'] = np.log(dfx['rate']/mean_rate)
    dfx['r_hat'] = dfx['r']*(dfx['employees']/n_min).clip_upper(1)
    d = dfx['r_hat'].to_dict()
    return d

def get_woe_series(df, c, d):
    return df[c].apply(lambda x: d.get(x, 0))
