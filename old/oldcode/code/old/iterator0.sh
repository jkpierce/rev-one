#!/bin/bash
declare -a trial=("a" "b" "c" "d" "e" "f" "g" "h" "i" "j" "k" "l" "m" "n")
END=11 # this is the length of the l array

for i in "${trial[@]}"
do
    for j in $(seq 1 $END);
    do
        echo python3 iterate_l.py "$i" "$j"
    done
done
