#! python

import sys
import sqlite3
import getopt
import os


################################################################
bismark_extraction_files = []
indb = None
outdir = None
force = False


################################################################
def update_indb(bismark_extraction_file, outdir, mode, indb):
    if mode == "create":
        indb = os.path.join(outdir, "methyl_info" + ".sqlite3")
        os.system("rm -rf " + indb)
        cx = sqlite3.connect(indb)
        cu = cx.cursor()
        create_table_sqlite3 = 'create table methyl_info (id integer PRIMARY KEY autoincrement, chr character, coor int)'
        cu.execute(create_table_sqlite3)

    cx = sqlite3.connect(indb)
    cu = cx.cursor()
    counter = 0
    for line in open(bismark_extraction_file,'r'):
        line=line.rstrip('\n\r')
        line_array = line.split('\t')
        chr, coor = line_array[2], line_array[3]
        counter+=1
        counter_str=str(counter)
        chr = add_quotes(chr)
        execute_sqlite3 = "insert into methyl_info (chr, coor) values(" + \
                            ','.join([chr,coor]) + ')'
        cu.execute(execute_sqlite3)

    cx.commit()
    cu.close()
    cx.close()
    return(indb)


def sort_db(indb):
    cx = sqlite3.connect(indb)
    cu = cx.cursor()
    execute_sqlite3 = "SELECT chr, coor FROM methyl_info ORDER BY chr, coor ASC"
    get_sqlite3_searching_result(execute_sqlite3,cu)
    fetch_all_result_list = cu.fetchall()
    cx.commit()
    cu.close()
    cx.close()
    return(fetch_all_result_list)


def output_coor_list(coor_list):
    for i in coor_list:
        print "\t".join(map(lambda x: str(x),i))


def get_sqlite3_searching_result(execute_sqlite3,cu):
    cu.execute(execute_sqlite3) 
    return (cu)


def add_quotes(item):
    new_item = item.join(["'"]*2)
    return(new_item)

################################################################
opts, args = getopt.getopt(
    sys.argv[1:],
    "b:",
    ["bismark_file=","bismark_extraction_file=","indb=","outdir=","force"]
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


if not outdir:
    sys.exit()
else:
    if os.path.exists(outdir):
        if force:
            os.system("rm -rf " + outdir)
        else:
            print "outdir has already existed! Exiting ......"
            sys.exit()
    os.system("mkdir -p " + outdir)
    
indb_outdir = os.path.join(outdir, "sqlite3_database")
os.system("mkdir " + indb_outdir)


#####################################################################
# if indb has not been built
if not indb:
    for bismark_extraction_file in bismark_extraction_files:
        if not indb:
            indb = update_indb(bismark_extraction_file, indb_outdir, mode='create', indb=indb)
        else:
            update_indb(bismark_extraction_file, indb_outdir, mode='update', indb=indb)
        
# after indb has been ready

coor_list = sort_db(indb)

output_coor_list(coor_list)


