#!/bin/bash

all_samples=`ls $1 | grep '*molecule_size*'`

for sample in $all_samples;
do
    sample_name=`basename $sample _lrbasic`
    ./preprocess.py -i $sample -o ${sample_name}_molecule_size.csv
done
