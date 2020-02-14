# Frozen CMIP6 Emissions
This repository contains scripts to freeze emissions factors (EFs) for combustion sectors from the [Coupled Model Intercomparison Project Phase 6 (CMIP6)](https://www.wcrp-climate.org/wgcm-cmip/wgcm-cmip6) and computes new emissions from the frozen emission factors. 

# Usage
The scripts are written in Python 3.6 and can be run from the command line:
```sh
python main.py /path/to/config.yml                         # Freeze EFs & calculate final frozen emissions
python main.py /path/to/config.yml -f "freeze_emissions"   # Only freeze emissions factors
python main.py /path/to/config.yml -f "calc_emissions"     # Only calculate final frozen emissions
```

## Configuration files
Configuration files are located in the `input/` directory and hold paths for input/output directories as well as other information needed to run the scripts. They follow the [YAML](https://yaml.org/) format.
