import pandas as pd
import numpy as np
import os
from os.path import dirname as up

root_dir = up(up(up(os.path.abspath(__file__))))

# Check emission factors
f_cmip  = os.path.join(root_dir, 'input', 'cmip6', 'H.SO2_total_EFs_extended.csv')
cmip_df = pd.read_csv(f_cmip, sep=',', header=0)

f_frzn  = os.path.join(root_dir, 'output', 'H.SO2_total_EFs_extended.csv')
frzn_df = pd.read_csv(f_frzn, sep=',', header=0)

meta_cols = ['iso', 'sector', 'fuel', 'units']
yr_strs = ['X{}'.format(yr) for yr in range(1750, 1970)]
cols = meta_cols + yr_strs

cmip_df = cmip_df[cols]
frzn_df = frzn_df[cols]

print(cmip_df[0:3] == frzn_df[0:3])
# comp = (cmip_df == frzn_df).all(axis='columns')
# idx = np.where(comp == False)

# print(frzn_df.iloc[idx])
# print(cmip_df.iloc[idx])