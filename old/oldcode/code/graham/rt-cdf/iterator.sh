#!/bin/bash
datafiles="$HOME/scratch/reverting-onecell/analysis/m-stats/*.dat"
for data in $datafiles; do
    data=$(basename $data) # cut off the filename 
    # echo $data
    sbatch runit.sh $data
done
