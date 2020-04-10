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

The frozen-emissions scripts also depend on CMIP6 emissions factors and activity files. These files **must** be placed in the repository's `input/cmip` directory in order for the scripts to produce any output. They must also follow the CEDS intermediate output naming conventions: 
* Emissions factors files: `H.<species>_total_EFs_extended.csv` 
* Activity files: `H.<species>_total_activity_extended.csv`

For example, the CMIP6 emissions factors and activity files for SO2 must be `H.SO2_total_EFs_extended.csv` and `H.SO2_total_activity_extended.csv`, respectively.

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

More information on the configuration files can be found [here](input/README.md)

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
The next step is to produce final emission files using the CEDS `S1.1.write_summary_data.R` script. Since the frozen emissions files are formatted for an older version of CEDS, this summary script `scripts/S1.1.write_summary_data.R` **must** be copied and pasted into your `CEDS/code/module-S` directory, overwriting the current CEDS summary script file.

Next, copy and paste the frozen emission files from the `/output` directory to your CEDS `/intermediate-output` directory. There are two scripts, one written in Python (`make_final_emissions.py`) and one in R (`make_final_emissions.R`), located in `/scripts`, that will run the CEDS summary script to produce final frozen emissions files. 

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

## 4. Producing Gridded Frozen Emissions
The CEDS package can be used to produce gridded bulk and biofuel frozen emissions netCDF files. Scripts to submit batch gridding jobs for emissions species on the `pic` HPC cluster can be found in `scripts/pic/gridding`. 

Before submitting a gridding job, the frozen final emissions files produced by the summary script in step 2 must be moved to your `CEDS/final-emissions/current-versions` directory. Annual gridded emissions files and their checksum files will be placed in `CEDS/intermediate-output/gridded-emissions`. The chunked bulk and biofuel gridded emissions will be placed in `CEDS/final-emissions/gridded-emissions`. 

**NOTE**: The gridding functions **must** be run via the commands illustrated in the gridding bash scripts in order to produce correct gridded emissions. Using the `Make` targets (i.e., `make so2-gridded`) will cause the frozen emissions files that have been placed in `CEDS/final-emissions/current-versions` to be overwritten with non-frozen emissions, leading to incorrect grids.

## 5. Post-Processing Gridded Emissions Files
CEDS produces the gridded frozen emissions files with the same filenames as normal gridded emissions. To avoid confusion, scripts located in `scripts/pic/post-process` can assist in re-naming the files. These directories also hold scripts that can modify the gridded netCDF file metadata. 

## Summary
### Produce Frozen Emission Factor Files
  1. Navigate to the repository's `src/` directory and run `python driver.py <config_file> <options>` to produce frozen EF files and total emission files. The frozen files will be placed in the `/output` directory.
### Produce Emission Summary Data
  1. Copy and paste `scripts/S1.1.write_summary_data.R` into your `CEDS/code/module-S` directory.
  2. Copy and paste the frozen emission files from `/output` to `CEDS/intermediate-output`.
  3. CD to `/scripts` and execute the summary script: `python make_final_emissions.py /path/to/ceds`.
  4. Retrieve the final frozen emissions from `CEDS/final-emissions/current-versions`.
### Compare Frozen Emissions to Normal Emissions
  1. Configure the `current_CEDS_version` and `previous_CEDS_version` in `CEDS_version_comparison.R` to match the frozen emission & normal emission versions.
  2. Run `CEDS_version_comparison.R`.
  3. Comparison plots will be placed into `CEDS/final-emissions/diagnostics`.
### Producing Gridded Emissions Files (optional)
  1. Copy and paste the frozen final emissions files into `CEDS/final-emissions/current-versions`.
  2. Launch the gridding job.
  3. Retrieve the gridded frozen emissions files & checksum files from `CEDS/final-emissions/gridded-emissions.`
  4. Modify the gridded frozen emissions filenames.
