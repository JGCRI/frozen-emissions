This directory holds scipts to post-process gridded frozen emissions files on the pic HPC cluster.


**IMPORTANT***: Users must modify the `ROOT_DIR` variables in the shell scripts before use.


* `rename_em_grids.py` : Modifies the filenames of the frozen emissions NetCDF grids their respective CSV checksum files to better describe the contents of the file. Submit this script as a batch job via `rename_em_grids.sh`. Renames bulk anthro, bulk solid biofuel, and sub-VOC emissions grids and checksums.
  
  For example,
  ```
  BC-em-anthro_input4MIPs_emissions_CMIP_CEDS-2020-04-07_gn_195001-199912.nc
  ```
  will be renamed as
  ```
  BC-em-anthro_input4MIPs_emissions_CEDS-2017-05-18-frozen-US-EF_gn_195001-199912.nc 
  ```

* `update_gridded_meta-anthro.py` : Modifies the global metadata values of the gridded anthropogenic emissions netCDF files. Although its better to modify these values within the CEDS code itself, this script can be used to retroactively fix any metadata values instead of re-running the CEDS gridding functions. 

* `update_gridded_meta-biofuel.py` : Modifies the global metadata values of the gridded biofuel emissions netCDF files. Although its better to modify these values within the CEDS code itself, this script can be used to retroactively fix any metadata values instead of re-running the CEDS gridding functions.

* `post_process-bulk.sh` : Modifies the netCDF metadata and filenames for bulk anthro & solid biofuel emissions grids & CSV checksum files. Launches `update_gridded_meta-anthro.py`, `update_gridded_meta-biofuel.py`, `rename_em_grids.py`.

* `post_process-sub_voc.sh` : Modifies the netCDF metadata and filenames for sub-VOC emissions grids & CSV checksum files. Launches `update_gridded_meta-sub_voc.py` and `rename_em_grids.py`.

* `update_gridded_meta-bulk.sh` : Submit this script as a batch job to run `update_gridded_meta-anthro.py` & `update_gridded_meta-biomass.py` on pic.

* `rename_em_grids.sh` : Shell script to run `rename_em_grids.py` on pic.

