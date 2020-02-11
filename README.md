# Frozen CMIP6 Emissions
This repository contains scripts to freeze emissions factors (EFs) for combustion sectors from the [Coupled Model Intercomparison Project Phase 6 (CMIP6)](https://www.wcrp-climate.org/wgcm-cmip/wgcm-cmip6) and computes new emissions from the frozen emission factors. 

# Usage
The scripts are written in Python 3.6 and can be run from the command line:
```
python main.py /path/to/config.yml                        # Freeze EFs factors & calculate final frozen emissions
python main.py /path/to/config.yml -f "freeze_emissions"  # Only freeze EFs
python main.py /path/to/config.yml -f "calc_emissions"    # Only calculate final frozen emissions
```

## Configuration files
Configuration files located in the `init` directory hold paths for input/output directories as well as other information needed to run the scripts.

### Example
The contents of `init/test-config.yml` are shown below:
```
dirs:
  win:
    cmip6_inter: C:\Users\nich980\data\e-freeze\test\CMIP6-emissions\intermediate-output
    root_inter: C:\Users\nich980\data\e-freeze\test\intermediate-output
    root_proj : C:\Users\nich980\code\frozen-emissions
    ceds: C:\Users\nich980\code\CEDS-dev
  linux: 
    cmip6_inter: /mnt/c/Users/nich980/data/e-freeze/test/CMIP6-emissions/intermediate-output
    root_inter: /mnt/c/Users/nich980/data/e-freeze/test/intermediate-output
    root_proj: /mnt/c/Users/nich980/code/frozen-emissions
    ceds: /mnt/c/Users/nich980/code/CEDS-dev
  input: ../input
  output: ../output
  init: ../init
  logs: logs
freeze:
  year: 1970
  isos: all
  species: [BC, CH4, CO, CO2, NH3, NMVOC, NOx, OC, SO2]
ceds:
  year_first: 1750
  year_last: 2014
```
