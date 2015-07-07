#! python

import getopt
import sys
import csv
 

###########################################################################
def parseMethLine(line):
    (readid,meth,chrm,coord,methcall) = line
    return (True if meth == '+' else False, chrm, coord)
 

###########################################################################
if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "",
                                  ["bismark=", "aggregate="])
    except getopt.GetoptError, err:
        # print help information and exit
        # will print something like "option -a not recognized"
        print str(err) 
        sys.exit(2)
     
    infile = None
    aggregatefile= None
     
    for o, a in opts:
        if o=="--bismark":
            infile = a
            print "Bismark", a
        elif o=="--aggregate":
            aggregatefile = a
            print "Aggregate", a
     
    assert infile != None
    assert aggregatefile != None
     
    bismark = csv.reader(open(infile, "r"), delimiter="\t")
     
    aggregate = csv.writer(open(aggregatefile,"w"),delimiter='\t')      
     
    currentchrm = None
    currentpos = None
     
    methylated = 0
    unmethylated = 0
     
    for line in bismark:
        (methcall, chrm, coord) = parseMethLine(line)
         
        # meth calls in 1 base, ucsc / bedgraph in 0 base
        coord = int(coord) -1
         
        # init
        if currentpos == None or chrm == None:
            currentchrm = chrm
            currentpos = coord
        elif currentpos != coord or currentchrm != chrm:
            # a new position or chromosome encountered
            # output our counts until now
            aggregate.writerow([currentchrm,currentpos,
                                methylated,unmethylated])
             
            # reset counts for next position
            currentchrm = chrm
            currentpos = coord
            methylated = 0
            unmethylated = 0
         
        if methcall:
            methylated += 1
        else:
            unmethylated += 1
     
    # output last line
    aggregate.writerow([currentchrm,currentpos,
                        methylated,unmethylated])

