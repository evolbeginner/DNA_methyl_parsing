#! /bin/bash

scripts_dir=`dirname $0`

while [ $# -gt 0 ]; do
	case $1 in
		-i|--in)
			OLDIFS=$IFS
			IFS=','
			for i in $2; do
				inputs=(${inputs[@]} $i)
			done
			IFS=$OLDIFS
			shift
			;;
		--errorRate)
			errorRate=$2
			shift
			;;
		--outdir)
			outdir=$2
			shift
			;;
		--force)
			force=true
			;;
		*)
			echo "Illegal params! Exiting ......"
			exit
			;;
	esac
	shift
done


if [ -e $outdir ]; then
	if [ -z $force ]; then
		echo "outdir $outdir has already existed! Exiting ......"; exit
	else
		rm -rf $outdir
	fi
fi
mkdir -p $outdir

if [ -z $errorRate ]; then
	echo "errorRate has to be given! Exiting ......"
	exit
fi

context_sorted_base=$outdir/"CpG_context.sorted.txt"
aggregate_base=$outdir/"CpG_context.aggregate"


##########################################################################
for index0 in ${!inputs[@]}; do
	input=${inputs[$index0]}
	echo $input
	let "index=$index0+1"
	awk 'FNR>1' $input | sort -k3,3 -k4,4n -S10G > "$context_sorted_base"$index
	python $scripts_dir/aggragateBismark.py --bismark ${context_sorted_base}$index --aggregate ${aggregate_base}$index
	python $scripts_dir/binomialMethCall.py --combined ${aggregate_base}$index --errorRate $errorRate
done


