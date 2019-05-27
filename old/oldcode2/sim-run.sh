#!/bin/bash
#SBATCH --mem=8G
#SBATCH --time=24:00:00
#SBATCH --account=def-marwanh
#SBATCH --tmp=250G	
#SBATCH --output=slurm-%j.out

module load python/3.6
source $HOME/jupyter_py3/bin/activate
cd $SLURM_TMPDIR
python3 $HOME/reverting-onecell/simulation/trial.py $1 $2
cp * $HOME/scratch/reverting-onecell

