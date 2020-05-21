"""
Rename frozen gridded emissions netcdf files & .csv checksum files produced by 
CEDS gridding module. Will update the names of bulk anthro, bulk solid biofuel,
and sub-VOC emissions files.

Filename changes
----------------
* Removes 'CMIP' sub-string.
* Adds 'frozen-US-EF' sub-string.
* Changes file production date sub-string to the CMIP6 date '2017-05-18'.
* Example
    * Default filename:
        NOx-em-anthro_input4MIPs_emissions_CMIP_CEDS-2020-03-10_gn_201001-201412.csv
    * Updated filename:
        NOx-em-anthro_input4MIPs_emissions_CEDS-2017-05-18-frozen-US-EF_gn_201001-201412.csv

Usage
-----
$ python rename_em_grids.py /path/to/em_grids/dir

To submit on pic, see rename_em_grids.sh.

Tested with Python 2.7, 3.6 - 3.8.

Matt Nicholson
20 April 2020
"""
from __future__ import print_function
import os
import sys
import re

print("*****************************************************************************")
print("*               Updating Frozen Emissions Grids Filenames                   *")
print("*****************************************************************************")

orig_wd = os.getcwd()
ROOT_DIR = sys.argv[1]
print('Changing working directory to {}'.format(ROOT_DIR))
os.chdir(ROOT_DIR)

date_pattern = re.compile(r'CMIP_CEDS-(\d{4}-\d{2}-\d{2})(-supplemental-data)?_gn')

# Get the names of every file in the current directory with an '.nc' or '.csv' extension
grid_files = [f for f in os.listdir(os.getcwd()) if os.path.isfile(f) and 
              (f.endswith('.nc') or f.endswith('.csv'))]
              
print('Emission grids & checksum files found: {}'.format(len(grid_files)))

for grid_file in grid_files:
    print('Processing {}...'.format(grid_file))
    match = date_pattern.search(grid_file)
    if match:
        date_to_replace = match.group(1)
    else:
        print('WARNING: Unable to parse {}'.format(grid_file))
        continue
    str_to_replace = 'CMIP_CEDS-{}'.format(date_to_replace)
    new_fname = grid_file.replace(str_to_replace, 'CEDS-2017-05-18-frozen-US-EF')
    print('{} --> {}'.format(grid_file, new_fname))
    os.rename(grid_file, new_fname)
print('Finished renaming emissions grids! Returning to original working directory...')
os.chdir(orig_wd)
