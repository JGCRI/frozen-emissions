"""
Rename frozen gridded emissions netcdf files & checksum files produced by CEDS
gridding module.

Example
--------
Default filename
    NOx-em-anthro_input4MIPs_emissions_CMIP_CEDS-2020-03-10_gn_201001-201412.csv
    
Updated filename:
    NOx-em-anthro_input4MIPs_emissions_CEDS-2017-05-18-frozen-US-EF_gn_201001-201412.csv

Matt Nicholson
20 April 2020
"""
from __future__ import print_function
import os
import sys
import re

print("*****************************************************************************")
print("*           Updating Frozen Emissions Gridded Sub-VOC Filenames             *")
print("*****************************************************************************")

ROOT_DIR = sys.argv[1]
print('Changing working directory to {}'.format(ROOT_DIR))
os.chdir(ROOT_DIR)

# --- Gridded files -----------------------------------------------------------
# Get the names of every file in the current directory with the '.nc' extension
grid_files = [f for f in os.listdir(os.getcwd()) if os.path.isfile(f) and f.endswith('.nc')]

for grid_file in grid_files:
    new_fname = grid_file.replace('CMIP_CEDS-2020-04-20', 'CEDS-2017-05-18-frozen-US-EF')
    print('{} --> {}'.format(grid_file, new_fname))
    os.rename(grid_file, new_fname)
    
# --- Checksum files ----------------------------------------------------------
# Get the names of every file in the current directory with the '.csv' extension
grid_files = [f for f in os.listdir(os.getcwd()) if os.path.isfile(f) and f.endswith('.csv')]

for grid_file in grid_files:
    new_fname = grid_file.replace('CMIP_CEDS-2020-04-20', 'CEDS-2017-05-18-frozen-US-EF')
    print('{} --> {}'.format(grid_file, new_fname))
    os.rename(grid_file, new_fname)
