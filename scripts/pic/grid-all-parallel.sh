#!/bin/bash
# Submit all CEDS species to run in parallel

# Wait for activity to finish, then run all species as their own jobs
SO2id=$(sbatch --parsable grid-SO2.sh)
NOxid=$(sbatch --parsable grid-NOx.sh)
#NMVOCid=$(sbatch --parsable grid-NMVOC.sh)
NH3id=$(sbatch --parsable grid-NH3.sh)
COid=$(sbatch --parsable grid-CO.sh)
BCid=$(sbatch --parsable grid-BC.sh)
OCid=$(sbatch --parsable grid-OC.sh)
# CH4id=$(sbatch --parsable grid-CH4.sh)
# CO2id=$(sbatch --parsable grid-CO2.sh)

# show dependencies in squeue output:
squeue -u $USER -a -o "%.5a %.10l %.6D %.6t %N %.40E"
