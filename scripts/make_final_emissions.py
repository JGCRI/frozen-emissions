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

def delete_file(f):
    print('Removing {}'.format(f))
    os.remove(f)

# Fetch CEDS path CMD arg
ceds_dir = sys.argv[1]

# Path of summary script within the CEDS directory
script_path = 'code/module-S/S1.1.write_summary_data.R'
inter_out = 'intermediate-output'
final_out = os.path.join('final-emissions', 'current-versions')

em_species = ['BC', 'CH4', 'CO', 'CO2', 'NH3', 'NMVOC', 'NOx', 'OC', 'SO2']

print('Changing working directory to {}'.format(ceds_dir))
os.chdir(ceds_dir)

# Remove previously-generated final emissions files
prev_files = [os.path.join(final_out, f) for f in os.listdir(final_out)
              if os.path.isfile(final_out, f) and f.endswith('.csv')]
map(delete_file, prev_files)

for species in em_species:
    # Execute the summary script for each emissions species defined in the above list
    print('=' * 60)
    print('Processing {}...'.format(species))
    print('=' * 60)
    cmd = 'Rscript {} {} --nosave --no-restore'.format(script_path, species)
    os.system(cmd)
    
    





