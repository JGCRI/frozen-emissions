"""
Rename frozen gridded emissions checksum files produced by CEDS gridding module.

Example
--------
Default filename
    NOx-em-anthro_input4MIPs_emissions_CMIP_CEDS-2020-03-10_gn_201001-201412.csv
    
Updated filename:
    NOx-em-anthro_input4MIPs_emissions_CEDS-2017-05-18-frozen-US-EF_gn_201001-201412.csv

Matt Nicholson
12 Mar 2020
"""
from __future__ import print_function
import os
import sys
import re

print("*****************************************************************************")
print("*           Updating Frozen Emissions Gridded Checksum Filenames            *")
print("*****************************************************************************")

ROOT_DIR = sys.argv[1]
print('Changing working directory to {}'.format(ROOT_DIR))
os.chdir(ROOT_DIR)

species_pattern = re.compile(r'^(\w{2,5})-em')
dates_pattern = re.compile(r'gn_(\d{6}-\d{6})\.csv$')
fnames = {'anthro' : '{}-em-anthro_input4MIPs_emissions_CEDS-2017-05-18-frozen-US-EF_gn_{}.csv',
          'biofuel': '{}-em-SOLID-BIOFUEL-anthro_input4MIPs_emissions_CEDS-2017-05-18-frozen-US-EF-supplemental-data_gn_{}.csv'
          }

# Get the names of every file in the current directory with the '.csv' extension
grid_files = [f for f in os.listdir(os.getcwd()) if os.path.isfile(f) and f.endswith('.csv')]

for grid_file in grid_files:
    match1 = species_pattern.search(grid_file)
    match2 = dates_pattern.search(grid_file)
    if match1 and match2:
        species = match1.group(1)
        dates = match2.group(1)
        if 'BIOFUEL' in grid_file:
            new_fname = fnames['biofuel']
        else:
            new_fname = fnames['anthro']
        new_fname = new_fname.format(species, dates)
        print('{} --> {}'.format(grid_file, new_fname))
        os.rename(grid_file, new_fname)
