#!/bin/bash
#SBATCH -A ceds
#SBATCH -t 30:00
#SBATCH -N 1
#SBATCH -p shared
#SBATCH --mail-user <YOUR_EMAIL@somewhere.com>
#SBATCH --mail-type END
#
# This script handles the post-processing of all bulk emissions grids:
#   * updates metadata of anthro emissions grids.
#   * updates metadata of solid biofuel emissions grids.
#   * Updates the filenames of all emissions grids NetCDF & checksum CSV files.

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
python rename_em_grids.py $ROOT_DIR


now=$(date)
echo "Current time : $now"