#!/bin/bash
datafiles="$HOME/scratch/reverting-onecell/*.dat"
for data in $datafiles; do
    mpath=$(dirname $data) # cut off the directory from data
    mstat=$(basename $data) # cut off the filename 
    mstat=${mstat::-4} # cut the .dat from the filename
    mstat="$mstat-mstats.dat" # add -mstats.dat to the filename
    mstat="$mpath/analysis/m-stats/$mstat" # add /analysis/m-stats/ to the path + filename
    #echo $mstat
    # now put full paths into runit.sh 
    sbatch runit.sh $data $mstat  # first arg is data file, second is mstats
done
