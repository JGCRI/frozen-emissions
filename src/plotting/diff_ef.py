"""
Compare two EF files

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

dir_a = r'C:\Users\nich980\code\frozen-emissions\output'
dir_b = r'C:\Users\nich980\data\e-freeze\frozen-emissions\2020-02-21\from-pic\intermediate-output'
f_template = 'H.{}_total_EFs_extended.csv'

# -- Organic frozen EF file --------------------------
f_a = f_template.format(species)
f_a = os.path.join(dir_a, f_a)
df_a = pd.read_csv(f_a, sep=',', header=0)
ef_a = df_a.loc[(df_a['sector'] == sector) &
                (df_a['fuel'] == fuel) &
                (df_a['iso'] == iso)].to_numpy()
ef_a = ef_a[0][4:]

# -- Frozen EF file used in gridding on PIC ----------
f_b = f_template.format(species)
f_b = os.path.join(dir_b, f_b)               
df_b = pd.read_csv(f_b, sep=',', header=0)
ef_b = df_b.loc[(df_b['sector'] == sector) &
                (df_b['fuel'] == fuel) &
                (df_b['iso'] == iso)].to_numpy()
ef_b = ef_b[0][4:]

# -- Sanity Check ------------------------------------
if len(ef_a) != len(ef_b) or len(ef_a) != len(years):
    raise ValueError('Length of emissions factors and years arrays are not equal')

# -- Plotting ---------------------------------------
fig, ax = plt.subplots()
line_a, = ax.plot(years, ef_a, label='Organic')
line_b, = ax.plot(years, ef_b, label='PIC')
lines = [line_a, line_b]
if zoom:
    ax.set_ylim(0, 0.09)
    ax.set_xlim(1920, 2020)
ax.set(xlabel='Year', ylabel='Emissions Factor',
       title='Frozen Emissions Factors - {}, {}, {}, {}'.format(species, iso, sector, fuel))
ax.grid()
plt.legend(lines, [l.get_label() for l in lines])
plt.show()