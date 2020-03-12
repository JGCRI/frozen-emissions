#!/bin/bash
#SBATCH -A ceds
#SBATCH -t 1:00:00
#SBATCH -N 1
#SBATCH -p shared
#SBATCH --mail-user matthew.nicholson@pnnl.gov
#SBATCH --mail-type END

ROOT_DIR="/pic/projects/GCAM/mnichol/ceds/worktrees/CEDS-frozen-em/final-emissions/gridded-emissions"

module purge
module load python

now=$(date)
echo "Current time : $now"

echo "Changing working directory to $ROOT_DIR"
cd $ROOT_DIR

python update_gridded_meta_anthro.py
python update_gridded_meta_biomass.py
python rename_gridded_files.py

now=$(date)
echo "Current time : $now"