#!/bin/bash
#SBATCH -A ceds
#SBATCH -t 40:00:00
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

# Grid speciated-VOCs
Rscript code/module-G/G1.2.grid_subVOC_emissions.R VOC01 --nosave --no-restore
Rscript code/module-G/G1.2.grid_subVOC_emissions.R VOC02 --nosave --no-restore
Rscript code/module-G/G1.2.grid_subVOC_emissions.R VOC03 --nosave --no-restore
Rscript code/module-G/G1.2.grid_subVOC_emissions.R VOC04 --nosave --no-restore
Rscript code/module-G/G1.2.grid_subVOC_emissions.R VOC05 --nosave --no-restore
Rscript code/module-G/G1.2.grid_subVOC_emissions.R VOC06 --nosave --no-restore
Rscript code/module-G/G1.2.grid_subVOC_emissions.R VOC07 --nosave --no-restore
Rscript code/module-G/G1.2.grid_subVOC_emissions.R VOC08 --nosave --no-restore
Rscript code/module-G/G1.2.grid_subVOC_emissions.R VOC09 --nosave --no-restore
Rscript code/module-G/G1.2.grid_subVOC_emissions.R VOC12 --nosave --no-restore
Rscript code/module-G/G1.2.grid_subVOC_emissions.R VOC13 --nosave --no-restore
Rscript code/module-G/G1.2.grid_subVOC_emissions.R VOC14 --nosave --no-restore
Rscript code/module-G/G1.2.grid_subVOC_emissions.R VOC15 --nosave --no-restore
Rscript code/module-G/G1.2.grid_subVOC_emissions.R VOC16 --nosave --no-restore
Rscript code/module-G/G1.2.grid_subVOC_emissions.R VOC17 --nosave --no-restore
Rscript code/module-G/G1.2.grid_subVOC_emissions.R VOC18 --nosave --no-restore
Rscript code/module-G/G1.2.grid_subVOC_emissions.R VOC19 --nosave --no-restore
Rscript code/module-G/G1.2.grid_subVOC_emissions.R VOC20 --nosave --no-restore
Rscript code/module-G/G1.2.grid_subVOC_emissions.R VOC21 --nosave --no-restore
Rscript code/module-G/G1.2.grid_subVOC_emissions.R VOC22 --nosave --no-restore
Rscript code/module-G/G1.2.grid_subVOC_emissions.R VOC23 --nosave --no-restore
Rscript code/module-G/G1.2.grid_subVOC_emissions.R VOC24 --nosave --no-restore
Rscript code/module-G/G1.2.grid_subVOC_emissions.R VOC25 --nosave --no-restore

# Chunk speciated-VOCs
Rscript code/module-G/G2.2.chunk_subVOC_emissions.R VOC01 --nosave --no-restore
Rscript code/module-G/G2.2.chunk_subVOC_emissions.R VOC02 --nosave --no-restore
Rscript code/module-G/G2.2.chunk_subVOC_emissions.R VOC03 --nosave --no-restore
Rscript code/module-G/G2.2.chunk_subVOC_emissions.R VOC04 --nosave --no-restore
Rscript code/module-G/G2.2.chunk_subVOC_emissions.R VOC05 --nosave --no-restore
Rscript code/module-G/G2.2.chunk_subVOC_emissions.R VOC06 --nosave --no-restore
Rscript code/module-G/G2.2.chunk_subVOC_emissions.R VOC07 --nosave --no-restore
Rscript code/module-G/G2.2.chunk_subVOC_emissions.R VOC08 --nosave --no-restore
Rscript code/module-G/G2.2.chunk_subVOC_emissions.R VOC09 --nosave --no-restore
Rscript code/module-G/G2.2.chunk_subVOC_emissions.R VOC12 --nosave --no-restore
Rscript code/module-G/G2.2.chunk_subVOC_emissions.R VOC13 --nosave --no-restore
Rscript code/module-G/G2.2.chunk_subVOC_emissions.R VOC14 --nosave --no-restore
Rscript code/module-G/G2.2.chunk_subVOC_emissions.R VOC15 --nosave --no-restore
Rscript code/module-G/G2.2.chunk_subVOC_emissions.R VOC16 --nosave --no-restore
Rscript code/module-G/G2.2.chunk_subVOC_emissions.R VOC17 --nosave --no-restore
Rscript code/module-G/G2.2.chunk_subVOC_emissions.R VOC18 --nosave --no-restore
Rscript code/module-G/G2.2.chunk_subVOC_emissions.R VOC19 --nosave --no-restore
Rscript code/module-G/G2.2.chunk_subVOC_emissions.R VOC20 --nosave --no-restore
Rscript code/module-G/G2.2.chunk_subVOC_emissions.R VOC21 --nosave --no-restore
Rscript code/module-G/G2.2.chunk_subVOC_emissions.R VOC22 --nosave --no-restore
Rscript code/module-G/G2.2.chunk_subVOC_emissions.R VOC23 --nosave --no-restore
Rscript code/module-G/G2.2.chunk_subVOC_emissions.R VOC24 --nosave --no-restore
Rscript code/module-G/G2.2.chunk_subVOC_emissions.R VOC25 --nosave --no-restore

now=$(date)
echo "Current time : $now"
