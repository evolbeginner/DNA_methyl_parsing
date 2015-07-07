#! /bin/bash

for i in mapping/*/$1*; do
	basename=`basename $i`
	outdir=$1/${basename%.txt}
	python ../scripts/sort_bismark.py -b $i --outdir $outdir --force --binom_test --output $outdir/final_output
done


