#!/usr/bin/python
from __future__ import division
import sys
import re
import numpy as np
import pandas as pd
reffile=sys.argv[1]
chrfile=sys.argv[2]
#read_length=int(sys.argv[3])
outfile=sys.argv[-1]
bedfile=[]
chrs=[]
exon={}
sum_reads={}
intron={}
rpkm={}
output = open(outfile,'w')
output.write("name")
for i in range(3,len(sys.argv)-1):
    bedfile.append(sys.argv[i])
for line in open (chrfile):
    line=line.rstrip()
    data=line.split('\t')
    chrs.append(data[0])
for bed in bedfile:
    sum_reads[bed]=0
    output.write("\t%s"%(bed))
#    for line in open (bed):
#        line=line.rstrip()
#        data=line.split('\t')
#        sum_reads[bed]+=float(data[3])*(int(data[2])-int(data[1]))
output.write("\n")
for chr in chrs:
    flag={}
    for line in open (reffile):
        if(re.match('#',line)): print chr
        else:
            line=line.rstrip()
            data=line.split('\t')
            if data[2] == chr:
                if(re.search(',$',data[9])):
                    data[9]=data[9][:-1]
                    data[10]=data[10][:-1]
                exonStart=map(int,data[9].split(','))
                exonEnd=map(int,data[10].split(','))
                for i in range(int(exonStart[0]),int(exonEnd[-1])+1):
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
                        exp[bed][i]=float(data[3])
    for line in open (reffile):
        for bed in bedfile:
            exon[bed]=0
            intron[bed]=0
            rpkm[bed]=0
        line=line.rstrip()
        data=line.split('\t')
        print data[1]
        if data[2] == chr:
            if(re.search(',$',data[9])):
                data[9]=data[9][:-1]
                data[10]=data[10][:-1]
            exonStart=map(int,data[9].split(','))
            exonEnd=map(int,data[10].split(','))
            exon_length=0
            intron_length=0
            for i in range(len(exonStart)):
                exon_length+=exonEnd[i]-exonStart[i]+1
#            for i in range(len(exonStart)-1):
#                intron_length+=exonStart[i+1]-exonEnd[i]-1
            output.write("%s"%(data[1]))
            for i in range(len(exonStart)):
                for j in range (exonStart[i],exonEnd[i]+1):
                    for bed in bedfile:
                        if exp.has_key(bed):
                            if exp[bed].has_key(j):exon[bed]+=exp[bed][j]
#            for i in range(len(exonStart)-1):
#                for j in range (exonEnd[i]+1,exonStart[i+1]):
#                    for bed in bedfile:
#                        if exp.has_key(bed):
#                            if exp[bed].has_key(j):intron[bed]+=exp[bed][j]
            for bed in bedfile:
#                if intron_length != 0 :
#                    exon[bed]=exon[bed]-intron[bed]*exon_length/intron_length
                rpkm[bed]=int(exon[bed]+0.5)
                output.write("\t%d"%(rpkm[bed]))
            output.write("\n")
output.close()
