#!/bin/bash
#SBATCH -A ceds
#SBATCH -t 10:00:00
#SBATCH -N 1
#SBATCH -p shared
#SBATCH --mail-user YOUR_EMAIL_HERE
#SBATCH --mail-type END

#Set up your environment you wish to run in with module commands.
module purge
module load R/3.3.3

now=$(date)
echo "Current time : $now"

# Change this path to the path of your CEDS project root.
cd /pic/projects/GCAM/mnichol/ceds/worktrees/CEDS-frozen-em

# Grid & chunk bulk emissions
Rscript code/module-G/G1.1.grid_bulk_emissions.R CH4 --nosave --no-restore
Rscript code/module-G/G2.1.chunk_bulk_emissions.R CH4 --nosave --no-restore 

# Grid & chunk biofuel emissions
Rscript code/module-G/G1.4.grid_solidbiofuel_emissions.R CH4 --nosave --no-restore
Rscript code/module-G/G2.4.chunk_solidbiofuel_emissions.R CH4 --nosave --no-restore

now=$(date)
echo "Current time : $now"

