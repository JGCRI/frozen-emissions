"""
Adjust final SO2 emissions for 1A1bc_Other-transformation sector to 
counteract mass balance adjustments

Matt Nicholson
23 Mar 2020
"""
import os
import pandas as pd
from pathlib import Path

# Get root project directory based on the location of the script
ROOT = str(Path(os.path.abspath(__file__)).parents[3])

# Read the frozen & CMIP6 SO2 total emissions
frzn_so2 = os.path.join(ROOT, 'output', 'SO2_total_CEDS_emissions.csv')
cmip_so2 = os.path.join(ROOT, 'input', 'cmip6', 'final-emissions', 'SO2_total_CEDS_emissions.csv')
print('Reading frozen SO2 emissions from {}'.format(frzn_so2))
print('Reading CMIP6 SO2 emissions from {}'.format(cmip_so2))

frzn_df = pd.read_csv(frzn_so2, sep=',', header=0)
cmip_df = pd.read_csv(cmip_so2, sep=',', header=0)

cols = ['X{}'.format(yr) for yr in range(1750, 1971)]

# Get a subset of the CMIP6 SO2 emissions for the 1A1bc_Other-transformation sector
# for years 1750-1970
cmip_so2 = cmip_df.loc[cmip_df['sector'] == '1A1bc_Other-transformation']
cmip_so2 = cmip_so2[cols].copy()

# Write the iso, sector, & fuel of frozen SO2 rows being modified to file
print('Writing diagnostic output...')
rows = cmip_so2.iloc[:, 0:3]
rows.to_csv('adjust_so2.log', sep=',', header=True, index=False)

# Overwrite the frozen SO2 emissions with CMIP6 emissions for the 1A1bc_Other-transformation sector
# for years 1750-1970
frzn_df.update(cmip_so2)
print('Writing frozen SO2 emissions to {}'.format(frzn_so2))
frzn_df.to_csv(frzn_so2, sep=',', header=True, index=False)
