"""
Plot emissions factors for a given species, sector, fuel, & iso

Matt Nicholson
6 Mar 2020
"""
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

species = 'SO2'
sector  = '1A1a_Electricity-public'
fuel    = 'hard_coal'
iso     = 'usa'
zoom    = True

year_start = 1750
year_end   = 2014
years      = [yr for yr in range(year_start, year_end + 1)]

frozen_dir = r'C:\Users\nich980\code\frozen-emissions\output'
cmip6_dir  = r'C:\Users\nich980\data\e-freeze\CMIP6-emissions\intermediate-output'
f_template = 'H.{}_total_EFs_extended.csv'

f_frozen  = f_template.format(species)
f_frozen  = os.path.join(frozen_dir, f_frozen)

f_cmip6  = f_template.format(species)
f_cmip6  = os.path.join(cmip6_dir, f_cmip6)

ef_df  = pd.read_csv(f_frozen, sep=',', header=0)
frozen_ef = ef_df.loc[(ef_df['sector'] == sector) &
                      (ef_df['fuel'] == fuel) &
                      (ef_df['iso'] == iso)].to_numpy()
                      
ef_df  = pd.read_csv(f_cmip6, sep=',', header=0)
cmip6_ef = ef_df.loc[(ef_df['sector'] == sector) &
                     (ef_df['fuel'] == fuel) &
                     (ef_df['iso'] == iso)].to_numpy()

frozen_ef = frozen_ef[0][4:]
cmip6_ef  = cmip6_ef[0][4:]

if len(frozen_ef) != len(cmip6_ef) or len(frozen_ef) != len(years):
    raise ValueError('Length of emissions factors and years arrays are not equal')
    
fig, ax = plt.subplots()
frozen_line, = ax.plot(years, frozen_ef, label='Frozen EF')
cmip6_line,  = ax.plot(years, cmip6_ef, label='CMIP6 EF')
lines = [frozen_line, cmip6_line]
if zoom:
    ax.set_ylim(0, 0.09)
    ax.set_xlim(1920, 2020)
ax.set(xlabel='Year', ylabel='Emissions Factor',
       title='Emissions Factors - {}, {}, {}, {}'.format(species, iso, sector, fuel))
ax.grid()
plt.legend(lines, [l.get_label() for l in lines])
plt.show()


