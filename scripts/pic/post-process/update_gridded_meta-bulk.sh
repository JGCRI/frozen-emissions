#!/bin/bash
#SBATCH -A ceds
#SBATCH -t 30:00
#SBATCH -N 1
#SBATCH -p shared
#SBATCH --mail-user <YOUR_EMAIL@somewhere.com>
#SBATCH --mail-type END
#
# Update the metadata of bulk emissions grids, both anthro & solid biofuel.

# MODIFY THIS PATH 
ROOT_DIR="/path/to/frozen/grids"

module purge
module load gcc
module load netcdf
module load python

now=$(date)
echo "Current time : $now"

python update_gridded_meta_anthro.py $ROOT_DIR
python update_gridded_meta_biomass.py $ROOT_DIR

now=$(date)
echo "Current time : $now"