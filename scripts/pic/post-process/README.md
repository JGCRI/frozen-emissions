This directory holds scipts to post-process gridded frozen emissions files on the pic HPC cluster.

* `rename_gridded_files.py` : Modifies the filenames of the frozen gridded emissions files to better describe the contents of the file. Submit this script as a batch job via `rename_gridded_files.sh`.
  
  For example,
  ```
  BC-em-anthro_input4MIPs_emissions_CMIP_CEDS-2020-04-07_gn_195001-199912.nc
  ```
  will be renamed as
  ```
  BC-em-anthro_input4MIPs_emissions_CEDS-2017-05-18-frozen-US-EF_gn_195001-199912.nc 
  ```
  
* `rename_gridded_checksum.py` : Modifies the filenames of the gridded checksum `.csv` files in the same manner as `rename_gridded_files.py`. Submit this script as a batch job via `rename_gridded_checksum.sh`.

* `update_gridded_meta_anthro.py` : Modifies the global metadata values of the gridded anthropogenic emissions netCDF files. Although its better to modify these values within the CEDS code itself, this script can be used to retroactively fix any metadata values instead of re-running the CEDS gridding functions. 

* `update_gridded_meta_biomass.py` : Modifies the global metadata values of the gridded biofuel emissions netCDF files. Although its better to modify these values within the CEDS code itself, this script can be used to retroactively fix any metadata values instead of re-running the CEDS gridding functions.

* `update_gridded_meta.sh` : Launches `update_gridded_meta_anthro.py` and `update_gridded_meta_biomass.py`. Submit this script as a batch job to run `update_gridded_meta_anthro.py` & `update_gridded_meta_biomass.py` on pic.

* `rename_gridded_checksum.sh` : Shell script to run `rename_gridded_checksum.py` on pic.

* `post-process.sh` : Launches `update_gridded_meta_anthro.py`, `update_gridded_meta_biomass.py`, `rename_gridded_files.py`, & `rename_gridded_checksum.py`.
