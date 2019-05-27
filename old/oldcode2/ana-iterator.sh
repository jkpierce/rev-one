#!/bin/bash
directory="$HOME/scratch/reverting-onecell/*.npy"
for f in $directory; do
    #echo $f
    sbatch run.sh $f
done
