#! /bin/env perl

use strict;

##################################################################
my $posi_infile = $ARGV[0];
my $nega_infile = $ARGV[1];
my %counts;


##################################################################
sub read_infile{
    my ($infile, $type) = @_;
    open(my $IN, '<', $infile) || die;
    while(my $line = <$IN>){
        chomp($line);
        my @line_arr = split("\t", $line);
        my ($attr) = $line_arr[-1] =~ /=([^;=]+)/;
        $counts{$attr}{$type}++;
    }
    return(\%counts)
}

##################################################################
%counts = %{&read_infile($posi_infile, "posi", \%counts)};
%counts = %{&read_infile($nega_infile, "nega", \%counts)};

foreach my $i (keys %counts){
    $counts{$i}{'posi'}=0 if not exists $counts{$i}{'posi'};
    $counts{$i}{'nega'}=0 if not exists $counts{$i}{'nega'};
    print $i."\t".$counts{$i}{'posi'}."\t".$counts{$i}{'nega'}."\n";
}


