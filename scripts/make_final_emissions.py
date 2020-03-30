"""
Make final CEDS emissions from frozen emissions files.

Command Line args
------------------
Path to CEDS (Positional)

Usage
-----
python make_final_emissions.py /path/to/ceds

Matt Nicholson
30 Mar 2020
"""
import os
import sys

# Fetch CEDS path CMD arg
ceds_dir = sys.argv[1]

# Path of summary script within the CEDS directory
script_path = 'code/module-S/S1.1.write_summary_data.R'

species = ['BC', 'CH4', 'CO', 'CO2', 'NH3', 'NMVOC', 'NOx', 'OC', 'SO2']

print('Changing working directory to {}'.format(ceds_dir))
os.chdir(ceds_dir)

for specie in species:
    # Execute the summary script for each emissions species defined in the above list
    print('\nProcessing {}...'.format(specie))
    cmd = 'Rscript {} {} --nosave --no-restore'.format(script_path, specie)
    os.system(cmd)
    
    





