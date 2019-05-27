#!/bin/bash
# ("a" "g" "i" "l" "n")
trial="n"
# echo "$trial"
declare -a lvals=("0" "1" "2" "3" "4" "5" "6" "7" "8" "9")
for j in "${lvals[@]}";
do
    sbatch join-run.sh "$trial" "$j"
done

