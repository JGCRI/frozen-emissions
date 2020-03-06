"""
Plot total emissions for a given species, sector, fuel, & iso

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
f_template = '{}_total_CEDS_emissions.csv'

f_frozen  = f_template.format(species)
f_frozen  = os.path.join(frozen_dir, f_frozen)

f_cmip6  = f_template.format(species)
f_cmip6  = os.path.join(cmip6_dir, f_cmip6)

em_df     = pd.read_csv(f_frozen, sep=',', header=0)
frozen_em = em_df.loc[(em_df['sector'] == sector) &
                      (em_df['fuel'] == fuel) &
                      (em_df['iso'] == iso)].to_numpy()
                      
em_df    = pd.read_csv(f_cmip6, sep=',', header=0)
cmip6_em = em_df.loc[(em_df['sector'] == sector) &
                     (em_df['fuel'] == fuel) &
                     (em_df['iso'] == iso)].to_numpy()

frozen_em = frozen_em[0][4:]
cmip6_em  = cmip6_em[0][4:]

if len(frozen_em) != len(cmip6_em) or len(frozen_em) != len(years):
    raise ValueError('Length of emissions factors and years arrays are not equal')

# plt.style.use('ggplot')
fig, ax = plt.subplots()
frozen_line, = ax.plot(years, frozen_em, label='Frozen')
cmip6_line,  = ax.plot(years, cmip6_em, label='CMIP6')
lines = [frozen_line, cmip6_line]
if zoom:
    # ax.set_ylim(0, 0.09)
    ax.set_xlim(1940, 2020)
ax.set(xlabel='Year', ylabel='Emissions Factor',
       title='Total Emissions - {}, {}, {}, {}'.format(species, iso, sector, fuel))
ax.grid()
plt.legend(lines, [l.get_label() for l in lines])
plt.show()
