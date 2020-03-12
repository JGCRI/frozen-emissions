"""
Rename frozen gridded emissions files produced by CEDS gridding module.

Example
--------
Default filename
    NOx-em-anthro_input4MIPs_emissions_CMIP_CEDS-2020-03-10_gn_201001-201412.nc
    
Updated filename:
    NOx-em-anthro_input4MIPs_emissions_CEDS-2017-05-18-frozen-US-EF_gn_201001-201412.nc

Matt Nicholson
12 Mar 2020
"""
from __future__ import print_function
import os
import sys
import re

print("*****************************************************************************")
print("*            Updating Frozen Emissions Gridded NetCDF Filenames             *")
print("*****************************************************************************")

ROOT_DIR = sys.argv[1]
print('Changing working directory to {}'.format(ROOT_DIR))
os.chdir(ROOT_DIR)

species_pattern = re.compile(r'^(\w{2,5})-em')
fnames = {'anthro' : '{}-em-anthro_input4MIPs_emissions_CEDS-2017-05-18-frozen-US-EF_gn_201001-201412.nc',
          'biofuel': '{}-em-SOLID-BIOFUEL-anthro_input4MIPs_emissions_CEDS-2017-05-18-frozen-US-EF-supplemental-data_gn_196001-200912.nc'
          }

# Get the names of every file in the current directory with the '.nc' extension
grid_files = [f for f in os.listdir(os.getcwd()) if os.path.isfile(f) and f[-3:] == '.nc']

for grid_file in grid_files:
    match = species_pattern.search(grid_file)
    if match:
        species = match.group(1)
        if 'BIOFUEL' in grid_file:
            new_fname = fnames['biofuel']
        else:
            new_fname = fnames['anthro']
        new_fname = new_fname.format(species)
        print('{} --> {}'.format(grid_file, new_fname))
        os.rename(grid_file, new_fname)