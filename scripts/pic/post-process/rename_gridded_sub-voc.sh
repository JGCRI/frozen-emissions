#!/bin/bash
#SBATCH -A ceds
#SBATCH -t 1:00:00
#SBATCH -N 1
#SBATCH -p shared
#SBATCH --mail-user matthew.nicholson@pnnl.gov
#SBATCH --mail-type END

ROOT_DIR="/pic/dtn/data/gcam/frozen-emissions/speciated-voc"

module purge
module load gcc
module load netcdf
module load python

now=$(date)
echo "Current time : $now"

python rename_gridded_sub-voc.py $ROOT_DIR

now=$(date)
echo "Current time : $now"