#! python

import getopt
import re
import sys
import os
import sqlite3
sys.path.append(os.path.join(os.path.dirname(__file__),'lib'))
import gff_class


########################################################
lincRNA_gff = None
indb = None
binom_test_result = None
pvalue_cutoff = 0.05
binom_test_result_max_line = None
output = None


########################################################
def read_gff(ingff,types_included=['gene'],target_regexps=['ID']):
    gene_info={}
    gff_objs = {}
    with open(ingff,'r') as f:
        for line_no,line in enumerate(f.readlines()):
            line=line.rstrip('\n\r')
            if line.startswith('#'):
                continue
            gff_item_obj = gff_class.gff_items_class(line,types_included,target_regexps)
            gff_item = gff_item_obj.parse_gff_line()
            if gff_item:
                for key,value in gff_item.iteritems():
                    value.chr = re.sub('\|.+',"",value.chr)
                gff_objs.update(gff_item)
    f.close()
    return(gff_objs)
    
    
def generate_indb(gff_objs):
    indb = "./lincRNA_gff.sqlite3"
    os.system("rm -rf " + indb)
    cx = sqlite3.connect(indb)
    cu = cx.cursor()
    create_table_sqlite3 = 'create table genes_gff_info (id character primary key,chr character,strand character,start int,stop int)'
    cu.execute(create_table_sqlite3)
    for gene,obj in gff_objs.iteritems():
        chr = obj.chr
        strand = obj.strand
        start  = obj.start
        stop   = obj.stop
        gene   = add_quotes(gene)
        chr = add_quotes(chr)
        strand = add_quotes(strand)
        execute_sqlite3 = "insert into genes_gff_info values(" + \
                            ','.join([gene,chr,strand,start,stop]) + ')'
        cu.execute(execute_sqlite3)
    cx.commit()
    cu.close()
    cx.close()
    return(indb)


def search_db(db, binom_test_file, pvalue_cutoff, binom_test_result_max_line):
    cx = sqlite3.connect(db)
    cu = cx.cursor()
    genes_list = {}
    with open(binom_test_file, 'r') as f:
        line_counter = 0
        for line_no,line in enumerate(f.readlines()):
            line_counter += 1
            if binom_test_result_max_line and line_counter > binom_test_result_max_line:
                break
            if line.startswith('#'):
                continue
            #chr5	11703036	70	258	2.9643177677434211e-69
            line = line.rstrip('\n\r')
            line_array = line.split("\t")
            pvalue = float(line_array[4])
            chr = add_quotes(line_array[0])
            coor = add_quotes(line_array[1])

            execute_sqlite3s = []
            execute_sqlite3 = "select id from genes_gff_info where start <= " + coor + \
                                " AND stop >= " + coor + \
                                " and chr= " + chr
            execute_sqlite3s.append(execute_sqlite3)
            #execute_sqlite3 = "select id from genes_gff_info where chr= " + chr
            #execute_sqlite3s.append(execute_sqlite3)

            for execute_sqlite3 in execute_sqlite3s:
                get_sqlite3_searching_result(execute_sqlite3,cu)
                fetch_all_result_list = cu.fetchall()
                if fetch_all_result_list:
                    gene_name = fetch_all_result_list[0][0]
                    if not gene_name in genes_list:
                        genes_list[gene_name]={'methyl':0,'unmethyl':0}
                    if pvalue <= pvalue_cutoff:
                        genes_list[gene_name]['methyl'] += 1
                    elif pvalue > pvalue_cutoff:
                        genes_list[gene_name]['unmethyl'] += 1
                    break

    cu.close()
    cx.close()
    return(genes_list)


def get_sqlite3_searching_result(execute_sqlite3,cu):
    cu.execute(execute_sqlite3) 
    return (cu)


def add_quotes(item):
    new_item = item.join(["'"]*2)
    return(new_item)



########################################################
opts, args = getopt.getopt(
    sys.argv[1:],
    '',
    ["indb=","lincRNA_gff=","gff=","binom_test_result=","pvalue_cutoff=","head=","output=","out="],
)

for opt,value in opts:
    if opt == "--indb":
        indb = value
    elif opt == "--lincRNA_gff" or opt == "--gff":
        lincRNA_gff = value
    elif opt == "--binom_test_result":
        binom_test_result = value
    elif opt == "--pvalue_cutoff":
        pvalue_cutoff = float(value)
    elif opt == "--head":
        binom_test_result_max_line = int(value)
    elif opt == "--output" or opt == "--out":
        output = value


########################################################
gff_objs = read_gff(lincRNA_gff, "lincRNA")

if not indb:
    indb = generate_indb(gff_objs)

genes_list = search_db(indb, binom_test_result, pvalue_cutoff, binom_test_result_max_line)

if output:
    out_fh = open(output, 'w')
for k,v in genes_list.iteritems():
    if output:
        out_fh.write("\t".join([k,str(v['methyl']),str(v['unmethyl']),"\n"]))
    else:
        sys.stdout.write("\t".join([k,str(v['methyl']),str(v['unmethyl']),"\n"]))



