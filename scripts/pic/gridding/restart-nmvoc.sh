#!/bin/bash
#SBATCH -A ceds
#SBATCH -t 10:00:00
#SBATCH -N 2
#SBATCH -p shared
#SBATCH --mail-user matthew.nicholson@pnnl.gov
#SBATCH --mail-type END

# Usage
# -------
# sbatch restart-nmvoc.sh <voc-num>
# sbatch restart-nmvoc.sh VOC04

module purge
module load python

now=$(date)
echo "Current time : $now"
echo "Restarting NMVOC gridding at $1"

python restart-nmvoc.py $1

now=$(date)
echo "Current time : $now"