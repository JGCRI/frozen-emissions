# Frozen CMIP6 Emissions
This repository contains scripts to freeze emissions factors (EFs) for combustion sectors from the [Coupled Model Intercomparison Project Phase 6 (CMIP6)](https://www.wcrp-climate.org/wgcm-cmip/wgcm-cmip6) and computes new emissions from the frozen emission factors. 

# Set Up
The scripts to produce the frozen emissions are written and tested in Python 3.6. The easiest way to configure a Python environment with he packages needed to run the script is through [Anaconda](https://anaconda.org/anaconda/conda). Users can create an environment (named `frozen-emissions`) containing all the required packages by using the included `environment.yml` file and the following command:
```
conda env create -f environment.yml
```

The production of the final frozen emissions files depends on scripts from the [Community Emissions Data System (CEDS)](https://github.com/JGCRI/CEDS). Installation instructions can be found in the [User's Guide](https://github.com/JGCRI/CEDS/wiki/User_Guide). Make sure to install CEDS into the same parent directory as this repository, i.e., 
```
/my_code_dir
  |- /CEDS
  |- /frozen-emissions
```

# Producing Frozen Emissions
## 1. Freezing Emissions Factors & Producing Total Frozen Emissions
`src/driver.py` contains the two functions that do the heavy lifting: `freeze_emissions()` and `calc_emissions()`. 
* `freeze_emissions()` reads a CMIP6 emissions factors file for a given species (or list of species) and writes a new emissions factors file containing the frozen EFs. 
* `calc_emissions()` constructs a final emissions file for each species using the species' frozen EF file and the corresponding activity file.

`driver.py` can be run from the command line using a command of the format:
```
python driver.py <config_file> <options>
```

Both the frozen Emissions Factors files and total frozen emissions files are placed in the `/output` directory. 

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
The next step is to produce final emission files using the CEDS `S1.1.write_summary_data.R` script. 

Copy and paste the frozen emission files from the `/output` directory to your CEDS `/intermediate-output` directory. There are two scripts, one written in Python (`make_final_emissions.py`) and one in R (`make_final_emissions.R`), located in `/scripts`, that will run the CEDS summary script to produce final frozen emissions files. 

The Python script can be called via the command line:
```
python make_final_emissions.py /path/to/ceds
```
where `/path/to/ceds` is the path to your CEDS directory. The final frozen emission files will be located in your CEDS `final-emissions/current-versions` directory.

## 3. Compare Frozen Emissions to Normal Emissions
The final step is to create plots comparing the frozen emissions to the CMIP6 public release emissions using the `CEDS_version_comparison.R` script located in `CEDS_Data/code`. 

First, ensure that the `CEDS` and `CEDS_Data` directories are in the same parent directory. Check that the CEDS version of the summary data files produced in step 2 match the `current_CEDS_version` variable defined in `CEDS_version_comparison.R` (line 66). To make the plots easier to read, I used the script `rename_files.py` to change the filename version of the frozen emissions from `v_2019_12_17` to `v_frozen`

The comparison script will look for the previous release CEDS emission files in the `CEDS_Data/emission-archives/v2016_07_26` directory. Ensure that this directory exists, is polulated with the correct files, and that the `previous_CEDS_version` variable defined in `CEDS_version_comparison.R` (line 64) matches the version in the filenames (i.e., `v2016_07_26`). 

Within RStudio, set the current working directory to the `CEDS_Data` directory, and run the script. Assuming there are no errors (ahem, CH4), comparison `.pdf` graphs should be placed in `/CEDS/final-emissions/diagnostics`

## Summary
### Produce Frozen Emission Factor Files
  1. Navigate to the repository's `src/` directory and run `python driver.py <config_file> <options>` to produce frozen EF files and total emission files. The frozen files will be placed in the `/output` directory.
### Produce Emission Summary Data
  1. Copy and paste the frozen emission files from `/output` to `CEDS/intermediate-output` 
  2. CD to `/scripts` and execute the summary script: `python make_final_emissions.py /path/to/ceds`
  3. Retrieve the final frozen emissions from `CEDS/final-emissions/current-versions`.
### Compare Frozen Emissions to Normal Emissions
  1. Configure the `current_CEDS_version` and `previous_CEDS_version` in `CEDS_version_comparison.R` to match the frozen emission & normal emission versions
  2. Run `CEDS_version_comparison.R`
  3. Comparison plots will be placed into `CEDS/final-emissions/diagnostics`
