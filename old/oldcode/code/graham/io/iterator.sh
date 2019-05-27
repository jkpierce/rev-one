#!/bin/bash
directory="$HOME/scratch/reverting-onecell/analysis/entrain-deposit/*.dat"
for f in $directory; do
    #echo "$f submitted."
    sbatch convert.sh $f
done
