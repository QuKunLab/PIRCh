#!/usr/bin/python
from __future__ import division
import sys
import re
import math

reffile=sys.argv[1] #read in referance file
chrfile=sys.argv[2] #read in chromosome information file
length=int(sys.argv[3])
outfile=sys.argv[-1]
bedfile=[]  #read in different bedGraph file
for i in range(4,len(sys.argv)-1):
    bedfile.append(sys.argv[i])

intronfile = open(outfile,'w')
intronfile.write("BedGraph_file")
for i in range(length):
    intronfile.write("\t%d"%(i))
intronfile.write("\n")


chrs=[]
intron={}
exp={}
total_reads={}
for line in open (chrfile):
    line=line.rstrip()
    data=line.split('\t')
    chrs.append(data[0])

#chrs=["chr1"]

for bed in bedfile:
    total_reads[bed]=0
    intron[bed]={}
    for i in range(length):
        intron[bed][i]=0
    for line in open(bed):
        line=line.rstrip()
        data=line.split('\t')
        if data[0]!='chrM':
            total_reads[bed]+=float(data[3])*(int(data[2])-int(data[1]))


def count_intron(start,end,bed):
    global intron
    summit=(end+start)/2-length/2
    for i in range(length):
        if exp[bed].has_key(summit+i):
            intron[bed][i]+=exp[bed][summit+i]

for chr in chrs:
    flag={}
    for line in open (reffile):
        line=line.rstrip()
        data=line.split('\t')
        if data[0] == chr:
            exonStart=int(data[1])
            exonEnd=int(data[2])
            summit=(exonStart+exonEnd)/2
            for i in range(int(summit-length/2),int(summit+length/2)):
                flag[i]=1

    exp={}
    for bed in bedfile:
        exp[bed]={}
        for line in open(bed):
            line=line.rstrip()
            data=line.split('\t')
            if data[0] == chr:
                for i in range(int(data[1]),int(data[2])):
                    if flag.has_key(i) and float(data[3])>0:
                        exp[bed][i]=float(data[3])

    for line in open (reffile):
        line=line.rstrip()
        data=line.split('\t')
        if data[0] == chr:
            exonStart=int(data[1])
            exonEnd=int(data[2])
            for bed in bedfile:
                count_intron(exonStart,exonEnd,bed)

for bed in bedfile:
    intronfile.write("%s"%(bed))
    for i in range(length):
        intronfile.write("\t%f"%(intron[bed][i]))
    intronfile.write("\n")
intronfile.close()
