"""
Dump gridded emissions netCDF metadata into a text file

Matt Nicholson
27 Mar 2020

Usage
------
python nc_meta_dump.py /path/to/files
"""
from __future__ import print_function
import os
import sys
import re

ROOT_DIR = sys.argv[1]
print('Changing working directory to {}'.format(ROOT_DIR))
os.chdir(ROOT_DIR)

outfiles = {'anthro' : '{}_frzn_anthro_gridded_metadata_{}.txt',
            'biofuel': '{}_frzn_solidbiofuel_gridded_metadata_{}.txt'
           }
           
species_pattern = re.compile(r'^(\w{2,5})-em')
dates_pattern = re.compile(r'gn_(\d{6}-\d{6})\.nc$')

grid_files = [f for f in os.listdir(os.getcwd()) if os.path.isfile(f) and f[-3:] == '.nc']

for grid_file in grid_files:
    print('Processing {}...'.format(grid_file))
    match1 = species_pattern.search(grid_file)
    match2 = dates_pattern.search(grid_file)
    if match1 and match2:
        species = match1.group(1)
        dates = match2.group(1)
        if 'BIOFUEL' in grid_file:
            outfile = outfiles['biofuel']
        else:
            outfile = outfiles['anthro']
        outfile = outfile.format(species, dates)
        cmd = 'ncdump -h {} > {}'.format(grid_file, outfile)
        os.system(cmd)
