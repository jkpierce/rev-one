#!/bin/bash
#SBATCH --mem=8000M
#SBATCH --time=00:03:00
#SBATCH --account=def-marwanh

module load python/3.6
source $HOME/jupyter_py3/bin/activate
python3 trial.py $1 $2

