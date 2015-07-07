#! /bin/bash

for i in ./*.fastq; do corename=`basename $i`; ruby /mnt/bay3/sswang/tools_program/NGS_scripts/basic/cutadapt.rb -i $i --args "-q 20 -m 20" --outdir ../cutadapt_output/${corename%.fastq} --force; done

