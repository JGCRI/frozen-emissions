"""
Modify the metadata of frozen biofuel emissions gridded files

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
print("*    Post-Processing Frozen Emissions Gridded NetCDF Metadata - Biofuel     *")
print("*****************************************************************************")

species_pattern = re.compile(r'^(\w{2,5})-em')

grid_files = [f for f in os.listdir(os.getcwd()) if os.path.isfile(f)
              and f.endswith('.nc') and 'SOLID-BIOFUEL' in f]
              
for fname in grid_files:
    match = species_pattern.search(fname)
    if match:
        species = match.group(1)
    else:
        print('Unable to parse species from filename: {}'.format(fname))
        continue
    print('Processing {}...'.format(fname))
    # --- Global comment ---------------------------------------------------
    cmd_str = '"Frozen EF USA. Based on CEDS CMIP6 ver 2017-05-18 data with combustion sector emissions factors for years after 1970 frozen at their 1970 value for the USA region."'
    cmd = 'ncatted -O -a comment,global,o,c,{} -h {}'.format(cmd_str, fname)
    os.system(cmd)
    # --- Global Contact -------------------------------------------------------
    cmd_str = '"Steven J Smith(ssmith@pnnl.gov)"'
    cmd = 'ncatted -O -a contact,global,o,c,{} -h {}'.format(cmd_str, fname)
    os.system(cmd)
    # --- Global Further Info URL ----------------------------------------------
    cmd_str = '"http://www.globalchange.umd.edu/ceds/"'
    cmd = 'ncatted -O -a further_info_url,global,o,c,{} -h {}'.format(cmd_str, fname)
    os.system(cmd)
    # --- Global Institution ---------------------------------------------------
    cmd_str = '"Joint Global Change Research Institute, Pacific Northwest National Laboratory"'
    cmd = 'ncatted -O -a institution,global,o,c,{} -h {}'.format(cmd_str, fname)
    os.system(cmd)
    # --- Global Institution ID ------------------------------------------------
    cmd_str = '"JGCRI/PNNL"'
    cmd = 'ncatted -O -a institution_id,global,o,c,{} -h {}'.format(cmd_str, fname)
    os.system(cmd)
    # --- Global MIP era ---------------------------------------------------
    cmd_str = '"postCMIP6"'
    cmd = 'ncatted -O -a mip_era,global,o,c,{} -h {}'.format(cmd_str, fname)
    os.system(cmd)
    # --- Global Product ---------------------------------------------------
    cmd_str = '"supplementary-emissions-data"'
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
    cmd_str = '"CEDS-2020-02-26-supplemental-data"'
    cmd = 'ncatted -O -a source_id,global,o,c,{} -h {}'.format(cmd_str, fname)
    os.system(cmd)
    # --- Global Title -----------------------------------------------------
    cmd_str = '"Annual SOLID BIOFUEL Anthropogenic Emissions of {} - Frozen EF-USA"'.format(species)
    cmd = 'ncatted -O -a title,global,o,c,{} -h {}'.format(cmd_str, fname)
    os.system(cmd)
    
print('Success!')
    
    