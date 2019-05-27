#!/bin/bash
#SBATCH --mem=8G
#SBATCH --time=03:00:00
#SBATCH --account=def-marwanh
#SBATCH --tmp=100G

module load python/3.6
cd $SLURM_TMPDIR
source $HOME/jupyter_py3/bin/activate
python3 $HOME/scratch/reverting-onecell/analysis-codes/analyze_file.py $1
cp * $HOME/scratch/reverting-onecell/analysis/

