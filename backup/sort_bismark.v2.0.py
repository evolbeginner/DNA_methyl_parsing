#! python

# v2.0: CHH too slow

import sys
import sqlite3
import getopt
import os


################################################################
bismark_extraction_files = []
indb = None
outdir = None
output = None
force = False
counts = {'methyl':{},'unmethyl':{}}
is_sort = False
is_binom_test = False
binomialMethCall = os.path.join(os.path.dirname(__file__),"binomialMethCall.py")
errorRate = 0.01


################################################################
def update_indb(bismark_extraction_file, outdir, mode, indb):
    if mode == "create":
        indb = os.path.join(outdir, "methyl_info" + ".sqlite3")
        os.system("rm -rf " + indb)
        cx = sqlite3.connect(indb)
        cu = cx.cursor()
        create_table_sqlite3 = 'create table methyl_info (id character PRIMARY KEY, chr character, coor int, methyl_counts int, unmethyl_counts int)'
        cu.execute(create_table_sqlite3)

    cx = sqlite3.connect(indb)
    cu = cx.cursor()
    for line in open(bismark_extraction_file,'r'):
        line=line.rstrip('\n\r')
        line_array = line.split('\t')
        if len(line_array) < 4:
            continue
        methyl_sign, chr, coor = line_array[1], line_array[2], line_array[3]
        id = '-'.join([chr,coor])
        new_chr = add_quotes(chr)
        new_id = add_quotes(id)
        is_new=False

        if not id in counts['methyl'] and not id in counts['unmethyl']:
            counts['methyl'][id]=0
            counts['unmethyl'][id]=0
            is_new = True
        if methyl_sign == '+':
            counts['methyl'][id]+=1
        else:
            counts['unmethyl'][id]+=1

        methyl_counts = str(counts['methyl'][id])
        unmethyl_counts = str(counts['unmethyl'][id])

        if is_new:
            execute_sqlite3 = "insert into methyl_info (id, chr, coor, methyl_counts, unmethyl_counts) values(" + \
                                ','.join([new_id, new_chr, coor, methyl_counts, unmethyl_counts]) + ')'
        else:
            execute_sqlite3 = "update methyl_info set methyl_counts = " + methyl_counts + " , unmethyl_counts =" + unmethyl_counts + " where id == " + new_id
        cu.execute(execute_sqlite3)

    cx.commit()
    cu.close()
    cx.close()
    return(indb)


def sort_db(indb, is_sort=False):
    cx = sqlite3.connect(indb)
    cu = cx.cursor()
    if is_sort:
        execute_sqlite3 = "SELECT chr, coor, methyl_counts, unmethyl_counts FROM methyl_info ORDER BY chr, coor ASC"
    else:
        execute_sqlite3 = "SELECT chr, coor, methyl_counts, unmethyl_counts FROM methyl_info"
    get_sqlite3_searching_result(execute_sqlite3,cu)
    fetch_all_result_list = cu.fetchall()
    cx.commit()
    cu.close()
    cx.close()
    return(fetch_all_result_list)


def output_coor_list(coor_list, output=None):
    if output:
        fh = open(output, 'w')
        for i in coor_list:
            fh.write("\t".join(map(lambda x: str(x),i))+"\n")
        fh.close()
    else:
        for i in coor_list:
            print "\t".join(map(lambda x: str(x),i))
        

def get_sqlite3_searching_result(execute_sqlite3,cu):
    cu.execute(execute_sqlite3) 
    return (cu)


def add_quotes(item):
    new_item = item.join(["'"]*2)
    return(new_item)


def binom_test_aggregate(output, binomialMethCall, errorRate):
    cmd = ' '.join(["python",binomialMethCall,"--combined",output,"--errorRate",str(errorRate)])
    os.system(cmd)



################################################################
opts, args = getopt.getopt(
    sys.argv[1:],
    "b:",
    ["bismark_file=","bismark_extraction_file=","indb=","outdir=","output=","binom_test","errorRate=","force","sort"]
)

for opt, value in opts:
    if opt == "-b" or opt == "--bismark_file" or opt == "--bismark_extraction_file":
        bismark_extraction_files.append(value)
    elif opt == "--indb":
        indb = value
    elif opt == "--outdir":
        outdir = value
    elif opt == "--force":
        force = True
    elif opt == "--output":
        output = value
    elif opt == "--sort":
        is_sort = True
    elif opt == "--binom_test":
        is_binom_test=True
    elif opt == "--errorRate":
        errorRate = float(value)


if not outdir:
    if not indb:
        print "outdir or indb has to be given!"
        sys.exit()
else:
    if not indb:
        if os.path.exists(outdir):
            if force:
                os.system("rm -rf " + outdir)
            else:
                print "outdir has already existed! Exiting ......"
                sys.exit()
        os.system("mkdir -p " + outdir)
    

if not indb:
    indb_outdir = os.path.join(outdir, "sqlite3_database")
    os.system("mkdir -p " + indb_outdir)
if indb:
    indb_outdir=os.path.dirname(indb)


#####################################################################
if indb:
    tmp_coor_list = sort_db(indb, is_sort=False)
    for i in tmp_coor_list:
        id = "-".join([i[0],str(i[1])])
        counts_methyl=int(i[2])
        counts_unmethyl=int(i[3])
        if not id in counts['methyl'] and not id in counts['unmethyl']:
            counts['methyl'][id]=counts_methyl
            counts['unmethyl'][id]=counts_unmethyl

if bismark_extraction_files:
    for bismark_extraction_file in bismark_extraction_files:
        print bismark_extraction_file
        if not indb:
            indb = update_indb(bismark_extraction_file, indb_outdir, mode='create', indb=indb)
        else:
            update_indb(bismark_extraction_file, indb_outdir, mode='update', indb=indb)

# after indb has been ready
coor_list = sort_db(indb, is_sort)

output_coor_list(coor_list, output)

if is_binom_test:
    if output:
        binom_test_aggregate(output, binomialMethCall, errorRate)
    else:
        print "Error! binom_test cannot be performed if output is not given!"
        sys.exit()
    


