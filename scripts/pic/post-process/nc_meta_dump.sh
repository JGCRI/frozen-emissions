#!/bin/bash
#SBATCH -A ceds
#SBATCH -t 1:00:00
#SBATCH -N 1
#SBATCH -p shared
#SBATCH --mail-user matthew.nicholson@pnnl.gov
#SBATCH --mail-type END

ROOT_DIR="/pic/projects/GCAM/mnichol/ceds/worktrees/CEDS-frozen-em/final-emissions/gridded-emissions"
#ROOT_DIR="/pic/dtn/data/gcam/frozen-emissions"

module purge
module load gcc
module load netcdf
module load python

now=$(date)
echo "Current time : $now"

python nc_meta_dump.py $ROOT_DIR

now=$(date)
echo "Current time : $now"
