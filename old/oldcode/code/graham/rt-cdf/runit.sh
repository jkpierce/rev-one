#!/bin/bash
#SBATCH --mem=32G
#SBATCH --time=00:30:00
#SBATCH --account=def-marwanh
#SBATCH --tmp=4G

module load python/3.6
cd $SLURM_TMPDIR
source $HOME/jupyter_py3/bin/activate
python3 $HOME/scratch/reverting-onecell/analysis-codes/rt-cdf/cdf.py $1
cp * $HOME/scratch/reverting-onecell/analysis/rt-cdf/

