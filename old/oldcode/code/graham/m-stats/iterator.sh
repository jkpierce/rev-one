#!/bin/bash
directory="$HOME/scratch/reverting-onecell/*.dat"
for f in $directory; do
    #echo "$f submitted."
    sbatch runit.sh $f
done
