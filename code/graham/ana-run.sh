#!/bin/bash
#SBATCH --mem=160G
#SBATCH --time=08:00:00
#SBATCH --account=def-marwanh
#SBATCH --tmp=32G

module load python/3.6
cd $SLURM_TMPDIR
source $HOME/jupyter_py3/bin/activate
python3 $HOME/scratch/reverting-onecell/analyze.py $1
cp * $HOME/scratch/reverting-onecell/simulations-cat/analysis/

