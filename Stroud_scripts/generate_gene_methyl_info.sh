#! /bin/bash

DNA_methyl_stat="/mnt/bay2/sswang/resources/RNA-seq/Epigenetics/DNA_methyl/scripts/DNA_methyl_stat.py"
indir=$1

for i in `find $indir -name final_results.binom`; do
	dir=`dirname $i`
	python $DNA_methyl_stat --gff ~/project/linc/data/gff/liu_linc.new.gff --binom_test_result $i > $dir/gene_methyl.info
done


