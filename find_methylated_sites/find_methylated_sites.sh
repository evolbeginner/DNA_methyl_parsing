#! /bin/bash

#############################################################
wd=`dirname $0`
split_gff3="$wd/split_gff3.rb"
run_bedtools_per500b="$wd/run_bedtools_per500b.pl"
generate_gene_methyl_info="$wd/generate_gene_methyl_info.pl"


#############################################################
while [ $# -gt 0 ]; do
	case $1 in
		-i|--binom)
			binom_file=$2
			shift
			;;
		-p|--pvalue)
			p_value_cutoff=$2
			shift
			;;
		--gff|--gff_file|--gff3)
			gff_file=$2
			shift
			;;
		--type)
			type_arg=$2
			shift
			;;
		--outdir)
			outdir=$2
			shift
			;;
		--force)
			is_force=true
			;;
	esac
	shift
done


export p_value_cutoff=$p_value_cutoff

[ ! -z $is_force ] && rm -rf $outdir
mkdir -p $outdir
outfile=$outdir/gene_methyl.info
posi_bed=$outdir/posi.bed
nega_bed=$outdir/nega.bed
split_gff3_outdir=$outdir/split_gff3

posi_bed_intersect=$outdir/posi.bed_intersect
nega_bed_intersect=$outdir/nega.bed_intersect


#############################################################
awk 'BEGIN{OFS="\t"}{if($5<ENVIRON["p_value_cutoff"]){print $1, $2-1, $2}}' $binom_file > $posi_bed
awk 'BEGIN{OFS="\t"}{if($5>=ENVIRON["p_value_cutoff"]){print $1, $2-1, $2}}' $binom_file > $nega_bed

ruby $split_gff3 -i $gff_file --outdir $split_gff3_outdir

perl $run_bedtools_per500b $split_gff3_outdir $posi_bed $posi_bed_intersect
perl $run_bedtools_per500b $split_gff3_outdir $nega_bed $nega_bed_intersect

perl $generate_gene_methyl_info $posi_bed_intersect $nega_bed_intersect > $outfile


