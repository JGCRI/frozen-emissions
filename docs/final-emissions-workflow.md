# Workflow to produce final emissions from frozen emission factor files
This document describes the workflow used to produce "frozen" emission factor files (where emission factors for years after 1970 are set to their 1970 value).

## 1. Producing Frozen Emission Factor Files
This repository holds the code needed to produce frozen emission factor (EF) files from CEDS EF files. 

`driver.py` contains the two functions that do the heavy lifting: `freeze_emissions()` and `calc_emissions()`. 
* `freeze_emissions()` reads a CMIP6 emissions factors file for a given species (or list of species) and writes a new emissions factors file containing the frozen EFs. 
* `calc_emissions()` constructs a final emissions file for each species using the species' frozen EF file and the corresponding activity file.

The functions in `driver.py` can be invoked from the command line using a command of the form:
```
python driver.py <config_file> <options>
```
### Configuration files
The global configuration files contain directory paths and other information needed to properly execute the functions in `driver.py`. They are located in the `input/` directory and follow the [YAML](https://yaml.org/) format. From the `src/` directory, running `driver.py` with the full path to a config file would look something like this:
```
python driver.py ../input/config-basic.yml
```

### Command line options
* `config_file`: Configuration file (required)
  
  This positional argument specifies which configuration file to use to run the emission freezing scripts. If not given, an error will be raised and execution will stop. 
  
* `-f, --function`: Specify which emissions-related function to run (optional). Since the emission freezing functions take some time to run, users have the option to only execute one or the other. The default is `'all'`, in which both `freeze_emissions()` and `calc_emissions()` will be called.
  
  Examples:
  ```sh
  python driver.py <config_file>  # Run both freeze_emissions() & calc_emissions()
  python driver.py <config_file> -f "freeze_emissions"  # Only run freeze_emissions()
  python driver.py <config_file> -f "calc_emissions"    # Only run calc_emissions()
  ```


## 2. Producing Emission Summary Data
Tthe next step is to produce final emission files using the CEDS `S1.1.write_summary_data.R` script. 

The easiest way to do this is to copy and paste the frozen emission files from `/data/e-freeze/python-output/intermediate-output` to `code/CEDS/intermediate-output`, then execute the script `/code/my_jgcri/emissions-freeze/make_final_emissions.R`. This produces final emission files and places them in `/code/CEDS/final-emissions/current-versions`

## 3. Compare Frozen Emissions to Normal Emissions
The final step is to create plots comparing the frozen emissions to the CMIP6 public release emissions using the `CEDS_version_comparison.R` script located in `/code/CEDS_Data/code`. 

First, ensure that the `CEDS` and `CEDS_Data` directories are in the same parent directory (`/code` in this case). Check that the CEDS version of the summary data files produced in step 2 match the `current_CEDS_version` variable defined in `CEDS_version_comparison.R` (line 66). To make the plots easier to read, I used the script `rename_files.py` to change the filename version of the frozen emissions from `v_2019_12_17` to `v_frozen`

The comparison script will look for the previous release CEDS emission files in the `CEDS_Data/emission-archives/v2016_07_26` directory. Ensure that this directory exists, is polulated with the correct files, and that the `previous_CEDS_version` variable defined in `CEDS_version_comparison.R` (line 64) matches the version in the filenames (i.e., `v2016_07_26`). 

Within RStudio, set the current working directory to the `CEDS_Data` directory, and run the script. Assuming there are no errors (ahem, CH4), comparison `.pdf` graphs should be placed in `/CEDS/final-emissions/diagnostics`

## Summary
### Produce Frozen Emission Factor Files
  1. Navigate to the repository's `src/` directory and run `python driver.py <config_file> <options>` to produce frozen EF files and final emission files
### Produce Emission Summary Data
  1. Copy and paste the frozen emission files from `data/e-freeze/python-output/intermediate-output` to `code/CEDS/intermediate-output` 
  2. Run `/code/my_jgcri/emissions-freeze/make_final_emissions.R`
### Compare Frozen Emissions to Normal Emissions
  1. Configure the `current_CEDS_version` and `previous_CEDS_version` in `CEDS_version_comparison.R` to match the frozen emission & normal emission versions
  2. Run `CEDS_version_comparison.R`
  3. Comparison plots will be placed into `/CEDS/final-emissions/diagnostics`
