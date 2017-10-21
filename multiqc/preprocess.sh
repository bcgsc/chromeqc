#!/bin/bash

all_samples=`ls | grep '_lrbasic'`

for sample in $all_samples;
do
    sample_name=`basename $sample _lrbasic`
    echo $sample_name
    awk -v OFS=',' '{ print "'$sample_name'",$0; }' $sample/outs/summary.csv > $sample/outs/${sample_name}_basic_summary.csv
done

