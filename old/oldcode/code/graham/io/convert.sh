#!/bin/bash
#SBATCH --mem=32G
#SBATCH --time=00:60:00
#SBATCH --account=def-marwanh
#SBATCH --tmp=32G

module load python/3.6
cd $SLURM_TMPDIR
source $HOME/jupyter_py3/bin/activate
python3 $HOME/scratch/reverting-onecell/analysis-codes/io/convert.py $1
cp * $HOME/scratch/reverting-onecell/analysis/entrain-deposit/
echo $1 ' saved as numpy'

