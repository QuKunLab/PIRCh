#!/usr/bin/python
from __future__ import division
import sys
import re
import numpy as np
import pandas as pd
reffile=sys.argv[1]
chrfile=sys.argv[2]
outfile=sys.argv[-1]
bedfile=[]
chrs=[]
exon={}
sum_reads={}
intron={}
rpkm={}
output = open(outfile,'w')
output.write("Gene\tSNP_position\tGenome_position\tSNP_type")
for i in range(3,len(sys.argv)-1):
    bedfile.append(sys.argv[i])

for line in open (chrfile):
    line=line.rstrip()
    data=line.split('\t')
    chrs.append(data[0])
for bed in bedfile:
    sum_reads[bed]=0
    output.write("\t%s"%(bed))
output.write("\n")
for chr in chrs:
    flag={}
    for line in open (reffile):
        data=line.rstrip().split('\t')
        if data[0] == chr:
            pos=map(int,data[3].split(","))
            for x in pos:
                flag[x]=1
    exp={}
    for bed in bedfile:
        exp[bed]={}
        for line in open(bed):
            line=line.rstrip()
            data=line.split('\t')
            if data[0] == chr:
                for i in range(int(data[1]),int(data[2])+1):
                    if flag.has_key(i) and float(data[3])>0:
                        exp[bed][i]=float(data[3])
    for line in open (reffile):

        data=line.rstrip().split('\t')
        if data[0] == chr:
            output.write(line.rstrip()+"\t")
            #rel=data[2].split(",")
            #snp=data[4].split(",")
            pos=map(int,data[3].split(","))
            for bed in bedfile:
                for i in range(len(pos)):
                    count=0
                    if exp.has_key(bed):
                        if exp[bed].has_key(pos[i]):
                            count+=exp[bed][pos[i]]
                    output.write("%.7f,"%(count))
                output.write("\t")
            output.write("\n")
output.close()
