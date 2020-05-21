This directory contains scripts for producing & post-processing final/summary frozen emissions files.

* `S1.1.write_summary_data.R` is a modified version of the CEDS script by the same name, modified to handle the older CMIP-style emissions files. Copy & paste this file into your `CEDS/code/module-S` directory, overwriting the current file.

* `pic/` contains scripts designed to run on the `pic` HPC cluster.
* `local/` contains scripts designed to run locally on a Windows workstation.
* 'ceds/' CEDS scripts modified specifically for the frozen emissions project.
  * `S1.1.write_summary_data.R` is a modified version of the CEDS script by the same name, modified to handle the older CMIP-style emissions files. Copy & paste this file into your           `CEDS/code/module-S` directory, overwriting the current file.
  * `CEDS_version_comparison.R` is a modified version of the CEDS_Data script that compares emissions produced by two different versions of CEDS.