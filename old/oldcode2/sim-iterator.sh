#!/bin/bash
# declare -a trial=("a" "g" "i" "l" "n")
declare -a trial=("i" "l" "n")
declare -a lvals=("0" "1" "2" "3" "4" "5" "6" "7")
for i in "${trial[@]}";
do
    for j in "${lvals[@]}";
    do
        sbatch runone.sh "$i" "$j"
    done
done

