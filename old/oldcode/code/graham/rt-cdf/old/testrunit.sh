#!/bin/bash

#SBATCH --mem=8G
#SBATCH --time=00:05:00
#SBATCH --account=def-marwanh
#SBATCH --tmp=1G
echo $1 $2
module load python/3.6
cd $SLURM_TMPDIR
source $HOME/jupyter_py3/bin/activate
python3 $HOME/scratch/reverting-onecell/analysis-codes/rt-cdf/testcdf.py $1 $2
cp * $HOME/scratch/reverting-onecell/analysis/rt-cdf/

