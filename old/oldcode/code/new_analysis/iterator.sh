#!/bin/bash
for filename in *.dat; do
    echo $filename
    #sbatch runit.sh $filename | bash -
done
