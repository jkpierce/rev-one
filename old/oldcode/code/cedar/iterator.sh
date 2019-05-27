#!/bin/bash
declare -a trial=("a" "b" "c" "d" "e" "f" "g" "h" "i" "j" "k" "l" "m" "n")
declare -a lvals=("0" "1" "2" "3" "4" "5" "6" "7")

for i in "${trial[@]}";
do
    for j in "${lvals[@]}";
    do
        sbatch runone.sh "$i" "$j"
    done
done
