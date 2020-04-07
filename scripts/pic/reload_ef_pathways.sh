# Copy the emissions factors extended adjusted pathway files from the latest
# CEDS release to the frozen emissions CEDS directory
SRC=/pic/projects/GCAM/CEDS_Releases/CEDS-release_v_2019_12_23/CEDS/intermediate-output/H.*_total_EFs_extended_adjusted-pathway*.csv
DST=/pic/projects/GCAM/mnichol/ceds/worktrees/CEDS-frozen-em/intermediate-output
cp -v $SRC $DST