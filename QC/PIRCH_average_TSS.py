#!/usr/bin/python
from __future__ import division
import sys
import re
import math

reffile=sys.argv[1] #read in referance file
TSSfile=sys.argv[2]
chrfile=sys.argv[3]
outfile=sys.argv[-1]
bedfile=[]  #read in different bedGraph file
chrs=[]
count=[]
chip={}
total_reads={}
TSScount=0
for i in range(4,len(sys.argv)-1):
    bedfile.append(sys.argv[i])

chipfile = open(outfile,'w')
chipfile.write("Chip_file")
for i in range(4000):
    chipfile.write("\t%d"%(i))
chipfile.write("\n")

for line in open (chrfile):
    line=line.rstrip()
    data=line.split('\t')
    chrs.append(data[0])

for line in open (TSSfile):
    line=line.rstrip()
    data=line.split('\t')
    count.append(data[0])
    TSScount+=1

for bed in bedfile:
    total_reads[bed]=0
    chip[bed]={}
    for i in range(4000):
        chip[bed][i]=0
    for line in open(bed):
        line=line.rstrip()
        data=line.split('\t')
        total_reads[bed]+=float(data[3])*(int(data[2])-int(data[1]))

for chr in chrs:
    flag={}
    for line in open (reffile):
        if(re.match('#',line)): print chr
        else:
            line=line.rstrip()
            data=line.split('\t')
            if data[2] == chr:
                if data[1] in count:
                    tss=int(data[4])
                    for i in range(tss-2000,tss+2000):
                        flag[i]=1
    exp={}
    for bed in bedfile:
        exp[bed]={}
        for line in open(bed):
            line=line.rstrip()
            data=line.split('\t')
            if data[0] == chr:
                for i in range(int(data[1]),int(data[2])+1):
                    if flag.has_key(i) and float(data[3])>0:
                        exp[bed][i]=float(data[3])*10**9/total_reads[bed]

    for line in open (reffile):
        line=line.rstrip()
        data=line.split('\t')
        if data[2] == chr:
            if data[1] in count:
                tss=int(data[4])
		for bed in bedfile:
                    for i in range(tss-2000,tss+2000):
                        if exp[bed].has_key(i) and (exp[bed][i]!=0):
                            chip[bed][i-tss+2000]+=math.log(exp[bed][i],2)
for bed in bedfile:
    chipfile.write("%s"%(bed))
    for i in range(4000):
        chipfile.write("\t%f"%(chip[bed][i]/TSScount))
    chipfile.write("\n")
chipfile.close()
