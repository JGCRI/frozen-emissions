#!/bin/bash
#SBATCH -A ceds
#SBATCH -t 30:00
#SBATCH -N 1
#SBATCH -p shared
#SBATCH --mail-user <YOUR_EMAIL@somewhere.com>
#SBATCH --mail-type END

# MODIFY THIS PATH
ROOT_DIR="/path/to/frozen/grids"

module purge
module load gcc
module load netcdf
module load python

now=$(date)
echo "Current time : $now"

python rename_em_grids.py $ROOT_DIR

now=$(date)
echo "Current time : $now"