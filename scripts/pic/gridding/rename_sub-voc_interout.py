"""
Rename the gridded annual files to remove the CEDS version from the filename.

Example
-------
Original filename:  CEDS_VOC01_anthro_1950_0.5_v_2020_1_13.nc
Corrected filename: CEDS_VOC01_anthro_1950_0.5.nc

Usage
-----
python rename_sub-voc_interout.py

Matt Nicholson
20 April 2020
"""
import os
import re

# Set this variable to the path of the directory holding the gridded annual
# speciated VOC files
DIR = '/pic/projects/GCAM/mnichol/ceds/worktrees/CEDS-frozen-em/intermediate-output/gridded-emissions'

dir_init = os.getcwd()
print('Changing directory to {}'.format(DIR))
os.chdir(DIR)

pattern = re.compile(r'^CEDS_VOC\d{2}_anthro_\d{4}_\d\.\d_\w+\.nc$')
voc_files = [f for f in os.listdir('.') if os.path.isfile(f) and
             pattern.match(f)]

print('Files found: {}'.format(len(voc_files)))

for curr_file in voc_files:
    new_file = curr_file.replace('_v_2020_1_13', '')
    os.rename(curr_file, new_file)
    print('{} --> {}'.format(curr_file, new_file))
    
print('Finished! Returning to {}'.format(dir_init))
os.chdir(dir_init)
