#! /bin/bash

dir=$1
min_total=30

if [ -z $dir ]; then
	echo "Dir $dir is illegal. Exiting ......"
	exit
fi

#####################################################################
for input in `find $dir -name 'gene_methyl.info'`; do
	echo $input
	dirname=`dirname $input`
	output=$dirname/p_value.MinTotal$min_total.output
	script_dir=`dirname $0`
	python "$script_dir/parse_num_methylated_sites.py" --pair ~/project/linc/blast/double-level-results/pairs.list --input $input --min_total $min_total > $output
done

