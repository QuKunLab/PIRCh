#!/usr/bin/python
from __future__ import division
import sys
import re
reffile=sys.argv[1]
chrfile=sys.argv[2]
annfile=sys.argv[3]
outfile=sys.argv[-1]
bedfile=[]
chrs=[]
sum_reads={}
exon={}
intron={}
UTR_5={}
UTR_3={}
TSS={}
Lnc={}
for i in range(4,len(sys.argv)-1):
    bedfile.append(sys.argv[i])
output = open(outfile,'w')
output.write("category\tfile_names\texon\tintron\tUTR_5\tUTR_3\tTSS\tTotal_reads\n")
for line in open (chrfile):
    line=line.rstrip()
    data=line.split('\t')
    chrs.append(data[0])

for line in open (annfile):
    line=line.rstrip()
    data=line.split('\t')
    Lnc[data[0]]=1

for bed in bedfile:
    sum_reads[bed]=0
    exon[bed]=0
    intron[bed]=0
    UTR_5[bed]=0
    UTR_3[bed]=0
    TSS[bed]=0
    for line in open (bed):
        line=line.rstrip()
        data=line.split('\t')
        sum_reads[bed]+=float(data[3])*(int(data[2])-int(data[1]))


for chr in chrs:
    flag={}
    for line in open (reffile):
        if(re.match('#',line)): print chr
        else:
            line=line.rstrip()
            data=line.split('\t')
            if data[2] == chr:
                for i in range(int(data[4])-100,int(data[5])+1):
                    flag[i]=1
    for bed in bedfile:
            exp={}
            for line in open(bed):
                line=line.rstrip()
                data=line.split('\t')
                if data[0] == chr:
                    for i in range(int(data[1]),int(data[2])):
                        if flag.has_key(i) and float(data[3])>0:
                            exp[i]=float(data[3])
            for line in open (reffile):
                line=line.rstrip()
                data=line.split('\t')
                if data[2] == chr:
                    if Lnc.has_key(data[1]):
                        if(re.search(',$',data[9])):
                            data[9]=data[9][:-1]
                            data[10]=data[10][:-1]
                        exonStart=map(int,data[9].split(','))
                        exonEnd=map(int,data[10].split(','))
                        if data[6] == data[7]:
                            data[6]=exonStart[0]
                            data[7]=exonEnd[-1]
                        for i in range(int(data[4]),int(data[6])):
                            if exp.has_key(i):
                                UTR_5[bed]+=exp[i]
                        for i in range(int(data[7])+1,int(data[5])+1):
                            if exp.has_key(i):
                                UTR_3[bed]+=exp[i]
                        for i in range(int(data[4])-100,int(data[4])+51):
                            if exp.has_key(i):
                                TSS[bed]+=exp[i]
                        for i in range(len(exonStart)):
                            for j in range (exonStart[i],exonEnd[i]+1):
                                if exp.has_key(j):
                                    exon[bed]+=exp[j]
                        for i in range(len(exonStart)-1):
                            for j in range (exonEnd[i]+1,exonStart[i+1]):
                                if exp.has_key(j):
                                    intron[bed]+=exp[j]
for bed in bedfile:
    output.write("%s\t%s\t%f\t%f\t%f\t%f\t%f\t%f\n"%(annfile,bed,exon[bed],intron[bed],UTR_5[bed],UTR_3[bed],TSS[bed],sum_reads[bed]))
output.close()
