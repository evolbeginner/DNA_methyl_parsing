#! /bin/env perl

use strict;

##################################################################
my $count = 0;
my $size = 0;
my @bs;

my $indir = $ARGV[0];
my $bed_file = $ARGV[1];
my $outfile = $ARGV[2];


##################################################################
`rm $outfile` if -e $outfile;

my @infiles = glob("$indir/*");

foreach my $i (@infiles){
    $count++;
    push @bs, $i;
    if ($count % 100 == 0 or $count == scalar(@infiles)){
        my $b = join(" ", @bs);
        `bedtools intersect -wa -wb -a $bed_file -b $b 2>/dev/null >> $outfile`;
        @bs = ();
    }
}


