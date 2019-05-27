#!/bin/bash
directory="$HOME/scratch/reverting-onecell/simulations/*.npy"
for f in $directory; do
    #echo $f
    sbatch ana-run.sh $f
done
