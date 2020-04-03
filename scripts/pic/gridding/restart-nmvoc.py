"""
Restart NMVOC gridding at a specified sub-species

Notes
------
* User MUST change "ROOT_DIR" variable to the path of their CEDS root directory

Usage
-----
python restart-nmvoc.py <voc-number>
python restart-nmvoc.py VOC04

Matt Nicholson
3 April 2020
"""
from __future__ import print_function
import os
import sys
import re

# !!! User MUST change the value of ROOT_DIR to the path of their CEDS root directory !!!
ROOT_DIR = '/pic/projects/GCAM/mnichol/ceds/worktrees/CEDS-frozen-em'

# --- Variable definitions
cmd_grid  = 'Rscript code/module-G/G1.2.grid_subVOC_emissions.R {} --nosave --no-restore'
cmd_chunk = 'Rscript code/module-G/G2.2.chunk_subVOC_emissions.R {} --nosave --no-restore'
validate_err ='Invalid VOC param. Expected "VOCXX", got {}'
voc_pattern = re.compile(r'^VOC\d{2}$')
voc_nums = ['01', '02', '03', '04', '05', '06', '07', '08', '09',
            '12', '13', '14', '15', '16', '17', '18', '19', '20',
            '21', '22', '23', '24', '25']

# --- Retrieve & validate VOC command line arg
voc_arg = sys.argv[1]
try:
    voc_arg = voc_arg.upper()
except:
    raise ValueError(validate_err.format(voc_arg))

match = voc_pattern.match(voc_arg)
if not match:
    raise ValueError('Invalid VOC param. Expected "VOCXX", got {}'.format(voc_arg))

print('Changing working directory to {}'.format(ROOT_DIR))
os.chdir(ROOT_DIR)

# Get a subset of the VOC species that we need to run based on the index of the 
# voc cmd arg in voc_nums
voc_num = voc_arg[3:]
idx_start = voc_nums.index(voc_num)
voc_subset = voc_nums[idx_start:]

for voc in voc_num_subset:
    print('Processing {}'.format(voc))
    os.system(cmd_grid.format(voc))
    os.system(cmd_chunk.format(voc))