#!/bin/bash

# this script makes the two figures from their components
montage activity.pdf ele.pdf -mode Concatenate -tile 2x1 montage2.pdf
montage 1.pdf 2.pdf 3.pdf 4.pdf -mode Concatenate -tile 2x2 montage1.pdf

