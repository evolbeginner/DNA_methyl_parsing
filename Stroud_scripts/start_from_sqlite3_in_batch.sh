#! /bin/bash

indir=$1

[ -z $indir ] && echo "The dir that is searched against should be given! Exiting ......" && exit

sort_bismark="$mnt3_sswang/resources/RNA-seq/Epigenetics/DNA_methyl/scripts/sort_bismark.py"
outdir="chrC_corrected_results"

for i in `find $indir -name 'methyl_info.sqlite3'`; do
	dir1=`dirname $i`
	dir2=`dirname $dir1`
	dir2_basename=`basename $dir2`
	dir3=`dirname $dir2`
	dir3_basename=`basename $dir3`
	new_outdir="$outdir/$dir3_basename/$dir2_basename"
	python $sort_bismark --indb $i --outdir $new_outdir --binom_test --output $new_outdir/final_results --force --auto_errorRate
done

