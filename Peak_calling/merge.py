#!/usr/bin/python
import sys
from tabformat import packTab, parseTab, parseTabWithName
from optparse import OptionParser
#
opts = OptionParser()
usage="run merge.py\n%prog --t1 input bam1.rt --t2 input bam2.rt -o output merged_file "
opts = OptionParser(usage=usage)
opts.add_option("--t1", help="generated from bam_file1 by rtCounts")
opts.add_option("--t2", help="generated from bam_file2 by rtCounts")
opts.add_option("-o", help="merged two bam.rt")
options, arguments = opts.parse_args()
#
tab1=options.t1
tab2=options.t2
outputname=options.o
inp1 = open(tab1)
inp2 = open(tab2)
#
oup = open(outputname, 'w')
for line1 in inp1:
    line2 = inp2.readline()
    n1, t1 = parseTabWithName(line1)
    n2, t2 = parseTabWithName(line2)
    if (n1 != n2):
        print >> StandardError, "Files don't match!!"
        sys.exit(-1)
    else:
        if (t1 != [] and t2 != []):
            oup.write(n1 + '\t' + packTab(map(min, t1, t2)) + '\n')
