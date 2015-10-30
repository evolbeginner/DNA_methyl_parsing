#! /bin/env python

import getopt
import sys
import scipy as sp
import scipy.stats


#####################################################
input = None
pair_file = None
gene_methyl_info = {}
pairs = []
min_total = 0


#####################################################
def get_pairs(pair_file):
    pairs = []
    fh = open(pair_file, 'r')
    for line in fh.readlines():
        line = line.rstrip('\n\r')
        pairs.append(line.split('-'))
    return(pairs)


def get_gene_methyl_info(input):
    with open(input, 'r') as fh:
        line = fh.readline()
        while line:
            line = line.rstrip('\n\r')
            gene_name,num_of_methyl,num_of_unmethyl,laji = line.split("\t")
            num_of_methyl = int(num_of_methyl)
            num_of_unmethyl = int(num_of_unmethyl)
            gene_methyl_info[gene_name]={}
            gene_methyl_info[gene_name]['methyl'] = num_of_methyl
            gene_methyl_info[gene_name]['unmethyl'] = num_of_unmethyl
            line = fh.readline()
    return(gene_methyl_info)


#####################################################
opts, args = getopt.getopt(
    sys.argv[1:],
    'i:',
    ["input=","pair=","pair_file=","min_total="],
)

for opt, value in opts:
    if opt == "-i" or opt == "--input":
        input = value
    elif opt == "--pair_file" or opt == "--pair":
        pair_file = value
    elif opt == "--min_total":
        min_total = int(value)


#####################################################
pairs = get_pairs(pair_file)

gene_methyl_info = get_gene_methyl_info(input)

for pair in pairs:
    list = []
    is_next = False
    for gene in pair:
        if not gene in gene_methyl_info:
            is_next = True
            continue
        list.append(gene_methyl_info[gene]['methyl'])
        list.append(gene_methyl_info[gene]['unmethyl'])
    if is_next:
        continue
    x = [list[0:2],list[2:4]]
    if sum(list) < min_total:
        continue
    results = sp.stats.fisher_exact(x)
    print "\t".join(pair)+"\t"+"\t".join(map(lambda x:str(x),list))+"\t"+str(results[1])
    

