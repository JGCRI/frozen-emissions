"""
Modify the metadata of frozen anthropogenic emissions gridded files

Matt Nicholson
12 Mar 2020
"""
from __future__ import print_function
import os
import sys
import re

ROOT_DIR = sys.argv[1]
print('Changing working directory to {}'.format(ROOT_DIR))
os.chdir(ROOT_DIR)

print("*****************************************************************************")
print("*     Post-Processing Frozen Emissions Gridded NetCDF Metadata - Anthro     *")
print("*****************************************************************************")

species_pattern = re.compile(r'^(\w{2,5})-em')

grid_files = [f for f in os.listdir(os.getcwd()) if os.path.isfile(f)
              and f[-3:] == '.nc' and 'BIOMASS' not in f]
              
for fname in grid_files:
    match = species_pattern.search(fname)
    if match:
        species = match.group(1)
    else:
        print('Unable to parse species from filename: {}'.format(fname))
        continue
    # --- Global comment ---------------------------------------------------
    cmd_str = '"Frozen EF USA. Based on CEDS CMIP6 ver 2017-05-18 data with combustion sector emissions factors for years after 1970 frozen at their 1970 value for the USA region."'
    cmd = 'ncatted -O -a comment,global,o,c,{} -h {}'.format(cmd_str, fname)
    os.system(cmd)
    # --- Global MIP era ---------------------------------------------------
    cmd_str = '"postCMIP6"'
    cmd = 'ncatted -O -a mip_era,global,o,c,{} -h {}'.format(cmd_str, fname)
    os.system(cmd)
    # --- Global Product ---------------------------------------------------
    cmd_str = '"emissions-data"'
    cmd = 'ncatted -O -a product,global,o,c,{} -h {}'.format(cmd_str, fname)
    os.system(cmd)
    # --- Global References ------------------------------------------------
    cmd_str = '"Hoesly, R. M., Smith, S. J., Feng, L., Klimont, Z., Janssens-Maenhout, G., Pitkanen, T., Seibert, J. J., Vu, L., Andres, R. J., Bolt, R. M., Bond, T. C., Dawidowski, L., Kholod, N., Kurokawa, J.-I., Li, M., Liu, L., Lu, Z., Moura, M. C. P., O\'Rourke, P. R., and Zhang, Q.: Historical (1750-2014) anthropogenic emissions of reactive gases and aerosols from the Community Emission Data System (CEDS), Geosci. Model Dev., 11, 369-408. doi: 10.5194/gmd-11-369-2018."'
    cmd = 'ncatted -O -a references,global,o,c,{} -h {}'.format(cmd_str, fname)
    os.system(cmd)
    # --- Global Source ----------------------------------------------------
    cmd_str = '"CEDS-2020-02-26: Community Emissions Data System (CEDS)"'
    cmd = 'ncatted -O -a source,global,o,c,{} -h {}'.format(cmd_str, fname)
    os.system(cmd)
    # --- Global Source ID -------------------------------------------------
    cmd_str = '"CEDS-2020-02-26"'
    cmd = 'ncatted -O -a source_id,global,o,c,{} -h {}'.format(cmd_str, fname)
    os.system(cmd)
    # --- Global Title -----------------------------------------------------
    cmd_str = '"Annual Anthropogenic Emissions of {} - Frozen EF-USA"'.format(species)
    cmd = 'ncatted -O -a title,global,o,c,{} -h {}'.format(cmd_str, fname)
    os.system(cmd)
    # ----------------------------------------------------------------------
print('Success!')