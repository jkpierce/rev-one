#!/bin/bash
# directory="$HOME/scratch/reverting-onecell/simulations-cat/*.npy"
directory="$HOME/scratch/reverting-onecell/simulations-cat/flow_n*.npy"
for f in $directory; do
    #echo $f
    sbatch ana-run.sh $f
done
