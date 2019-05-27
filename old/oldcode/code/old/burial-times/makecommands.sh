#!/bin/bash
rm jobs
declare -a arr=("-2.5" "-2.0" "-1.5" "-1.0" "-0.5")

while read p; do
    for z in "${arr[@]}"; do
        echo "python3 burial-analysis.py" "$p" "$z">>jobs
    done
done <buryfiles
