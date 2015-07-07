#! /bin/bash

if [ $# != 2 ]; then
	echo "Usage: bash $0 indir outdir"
	exit
fi

indir=$1
outdir=$2
bs_genome_dir=~/resource/genome_seq/ATH/TAIR9/for_DNA_methyl/

if [ -d $outdir ]; then
	mkdir -p $outdir
fi

export PATH=$PATH:/mnt/bay3/sswang/software/NGS/reads_map/bismark_package/bismark_v0.8.3/

####################################################################
date
for i in `find $indir -name '*fastq'`; do
	basename=`basename $i`
	corename=${basename%.fastq}
	echo $corename
	time bismark --bowtie2 --non_directional -p 2 -o $outdir/$corename $bs_genome_dir $i {} \;
	date
done


