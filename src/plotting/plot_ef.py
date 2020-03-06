"""
Plot emissions factors

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

year_start = 1750
year_end   = 2014
years      = [yr for yr in range(year_start, year_end + 1)]

# dir = r'C:\Users\nich980\code\frozen-emissions\output'
dir = r'C:\Users\nich980\data\e-freeze\CMIP6-emissions\intermediate-output'
f_template = 'H.{}_total_EFs_extended.csv'

f_in  = f_template.format(species)
f_abs = os.path.join(dir, f_in)

ef_df  = pd.read_csv(f_abs, sep=',', header=0)
ef_row = ef_df.loc[(ef_df['sector'] == sector) &
                   (ef_df['fuel'] == fuel) &
                   (ef_df['iso'] == iso)].to_numpy()

ef_row = ef_row[0][4:]

if len(ef_row) != len(years):
    raise ValueError('Length of emissions factors and years arrays are not equal')
    
fig, ax = plt.subplots()
ax.plot(years, ef_row)

ax.set(xlabel='Year', ylabel='Emissions Factor',
       title='CMIP6 Emissions Factors - {}, {}, {}, {}'.format(species, iso, sector, fuel))
ax.grid()

plt.show()


