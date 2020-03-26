#!/bin/bash
#SBATCH -A ceds
#SBATCH -t 10:00:00
#SBATCH -N 1
#SBATCH -p shared

#SBATCH --mail-user matthew.nicholson@pnnl.gov
#SBATCH --mail-type END

#Set up your environment you wish to run in with module commands.
module purge
module load R/3.3.3

#Actually codes starts here
now=$(date)
echo "Current time : $now"

cd /pic/projects/GCAM/mnichol/ceds/worktrees/CEDS-frozen-em

Rscript code/module-G/G2.1.chunk_bulk_emissions.R BC --nosave --no-restore
Rscript code/module-G/G2.1.chunk_bulk_emissions.R CO --nosave --no-restore
Rscript code/module-G/G2.1.chunk_bulk_emissions.R CO2 --nosave --no-restore
Rscript code/module-G/G2.1.chunk_bulk_emissions.R NH3 --nosave --no-restore
Rscript code/module-G/G2.1.chunk_bulk_emissions.R NMVOC --nosave --no-restore
Rscript code/module-G/G2.1.chunk_bulk_emissions.R NOx --nosave --no-restore
Rscript code/module-G/G2.1.chunk_bulk_emissions.R OC --nosave --no-restore
Rscript code/module-G/G2.1.chunk_bulk_emissions.R SO2 --nosave --no-restore

now=$(date)
echo "Current time : $now"