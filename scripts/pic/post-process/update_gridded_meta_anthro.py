"""
Modify the metadata of frozen anthropogenic emissions gridded files

Matt Nicholson
12 Mar 2020
"""
import os
import sys

SPECIES = ['BC', 'CO', 'CO2', 'NH3', 'NOx', 'NMVOC', 'OC', 'SO2']

YEARS = ['196001-200912', '201001-201412']
BAD_FILES = []

print("*****************************************************************************")
print("*     Post-Processing Frozen Emissions Gridded NetCDF Metadata - Anthro     *")
print("*****************************************************************************")

for year in YEARS:
    for s in SPECIES:
        print('Processing {} {}...'.format(s, YEARS))
        fname = '{}-em-anthro_input4MIPs_emissions_CMIP_CEDS-2020-02-27_gn_{}.nc'.format(s, year)
        if not os.path.isfile(fname):
            fname = '{}-em-anthro_input4MIPs_emissions_CMIP_CEDS-2020-03-10_gn_{}.nc'.format(s, year)
            if not os.path.isfile(fname):
                fname = '{}-em-anthro_input4MIPs_emissions_CMIP_CEDS-2020-03-09_gn_{}.nc'.format(s, year)
                if not os.path.isfile(fname):
                    BAD_FILES.append('{}_{}'.format(s, year)
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
        cmd_str = '"Annual Anthropogenic Emissions of {} - Frozen EF-USA"'.format(s)
        cmd = 'ncatted -O -a title,global,o,c,{} -h {}'.format(cmd_str, fname)
        os.system(cmd)
        # ----------------------------------------------------------------------
for bad_f in BAD_FILES:
    print('Unable to process {}'.format(bad_f))