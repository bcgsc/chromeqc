#!/bin/bash

all_samples=`ls | grep '_lrbasic'`

for sample in $all_samples;
do
    sample_name=`basename $sample _lrbasic`
    echo "SampleName" > tmp
    echo $sample_name >> tmp
    paste -d ',' tmp $sample/outs/summary.csv > $sample/outs/${sample_name}_basic_summary.csv
    rm tmp
done
