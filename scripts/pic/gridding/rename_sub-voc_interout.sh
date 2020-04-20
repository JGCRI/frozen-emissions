#!/bin/bash
#SBATCH -A ceds
#SBATCH -t 30
#SBATCH -N 1
#SBATCH -p shared
#SBATCH --mail-user YOUR_EMAIL_HERE
#SBATCH --mail-type END

module purge
module load python

now=$(date)
echo "Current time : $now"

python rename_sub-voc_interout.py

now=$(date)
echo "Current time : $now"