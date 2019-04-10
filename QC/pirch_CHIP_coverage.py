#!/usr/bin/python
from __future__ import division
import sys
import re
reffile=sys.argv[1]
chrfile=sys.argv[2]
outfile=sys.argv[-1]
chipfile=[]
chrs=[]
count={}
cover={}
output = open(outfile,'w')
output.write("name")
for i in range(3,len(sys.argv)-1):
    chipfile.append(sys.argv[i])

for line in open (chrfile):
    line=line.rstrip()
    data=line.split('\t')
    chrs.append(data[0])
for chip in chipfile:
    output.write("\t%s"%(chip))
output.write("\n")
for chr in chrs:
    exp={}
    for chip in chipfile:
        exp[chip]={}
        for line in open(chip):
            line=line.rstrip()
            data=line.split('\t')
            if data[0] == chr:
                for i in range(int(data[1]),int(data[2])+1):
                        exp[chip][i]=1
    for line in open (reffile):
        for chip in chipfile:
            count[chip]=0
            cover[chip]=0
        line=line.rstrip()
        data=line.split('\t')
        if data[2] == chr:
            exonStart=int(data[4])-2000
            exonEnd=int(data[5])+2000
            length=exonEnd-exonStart
            for i in range(exonStart,exonEnd+1):
                for chip in chipfile:
                    if exp[chip].has_key(i):
                        count[chip]+=1
            for chip in chipfile:
                cover[chip]=float(count[chip])/length
                output.write("\t%.7f"%(cover[chip]))
            output.write("\n")
output.close()
