#!/bin/bash
#SBATCH --mem=120G
#SBATCH --time=01:00:00
#SBATCH --account=def-marwanh
#SBATCH --tmp=120G

module load python/3.6
cd $SLURM_TMPDIR
source $HOME/jupyter_py3/bin/activate
python3 $HOME/scratch/reverting-onecell/joiner.py $1 $2
cp * $HOME/scratch/reverting-onecell/simulations/

