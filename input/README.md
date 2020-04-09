This directory holds various input files needed to run the frozen emissions scripts, including:
* Script configuration YAML files
* Log configuration files
* CEDS combustion sectors & ISO files

# Script configuration YAML files
At the beginning of execution, the frozen emissions scripts read a configuration YAML file that is passed via command line. Two configuration files are included with the repo: 
* `config-basic.yml` freezes all combustion-related emissions at 1970 for all ISOs.
* `config-usa.yml` freezes all combustion-related emissions at 1970 for USA only.

## Fields
Each YAML configuration file has numerous fields that pass crucial information to the frozen emissions scripts.

* `freeze' contains information that tells the scripts which ISOs and species to freeze and at what year.
  * `year` : int; year at which to freeze the emissions.
  * `isos` : string or list of strings; ISOs to freeze. To freeze a subset of CEDS ISOs, set as a list of ISO strings (e.g., `[usa]`). To freeze all CEDS ISOs, set to `all`. 
  * `species` : list or strings; Emission species to freeze.
* `ceds` contains metadata about the CMIP6 input files produced by the CEDS package.
  * `year_first`: int; First year of emissions.
  * `year_last` : int; Final year of emissions.
  
 # Log configuration YAML file
 `log-config.yml` contains information to configure the frozen emissions logger. The log is written to `src/logs/main.log`.
  
 # Other files in the directory
 * `ceds_isos.csv` : Maps CEDS ISOs to their country name & region.
 * `combustion_sectors.csv` : Contains the names of all CEDS combustion-related sectors.
 * `master_sector.csv` : Master list of CEDS sectors.
