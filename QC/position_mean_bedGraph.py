#!/usr/bin/python
from __future__ import division
import sys
import re
import math

reffile=sys.argv[1] #read in referance file
chrfile=sys.argv[2] #read in chromosome information file
outfile=sys.argv[-1]
bedfile=[]  #read in different bedGraph file
for i in range(3,len(sys.argv)-1):
    bedfile.append(sys.argv[i])

exonfile = open("exon."+outfile,'w')
intronfile = open("intron."+outfile,'w')
exonfile.write("BedGraph_file")
intronfile.write("BedGraph_file")
for i in range(300):
    exonfile.write("\t%d"%(i))
    intronfile.write("\t%d"%(i))
exonfile.write("\n")
intronfile.write("\n")

chrs=[]
exon={}
intron={}
exp={}
total_reads={}
for line in open (chrfile):
    line=line.rstrip()
    data=line.split('\t')
    chrs.append(data[0])

for bed in bedfile:
    total_reads[bed]=0
    exon[bed]={}
    intron[bed]={}
    for i in range(300):
        exon[bed][i]=0
        intron[bed][i]=0
    for line in open(bed):
        line=line.rstrip()
        data=line.split('\t')
        total_reads[bed]+=float(data[3])*(int(data[2])-int(data[1]))
exoncount=0
introncount=0

def split_f(start,end):
    s= start.split(',')
    e= end.split(',')
    if s[-1]=='':
        del s[-1]
        del e[-1]
    s= map(int,s)
    e=map(int,e)
    return s,e
#def split_f(start,end):
#    (re.search(',$',start)):
#        start=start[:-1]
#        end=data[:-1]
#    return map(int,start.split(',')),map(int,end.split(','))

#def count(start,para,step,mod):
#    global exon,intron
#    if para=="left" :
#        for i in range(100):
#            tmp={}
#            for bed in bedfile:
#                tmp[bed]=0
#                for j in range(start-(100-i)*step,start-(100-i-1)*step):
#                    if exp[bed].has_key(j):
#                        tmp[bed]+=exp[bed][j]
#                    if mod =="e":
#                        exon[bed][i]+=tmp[bed]/step
#                    else : intron[bed][i]+=tmp[bed]/step
#    else :
#        for i in range(100):
#            tmp={}
#            for bed in bedfile:
#                tmp[bed]=0
#                for j in range(start+i*step,start+(i+1)*step):
#                    if exp[bed].has_key(j):
#                        tmp[bed]+=exp[bed][j]
#                    if mod =="e":
#                        exon[bed][i+200]+=tmp[bed]/step
#                    else : intron[bed][i+200]+=tmp[bed]/step

def scale_count(start,end,length,mod):
    global exon,intron
    step=(float(end)-start+1)/100
    start=start-length
    end=end+length
    if step<1 :
        nex = -1
        for i in range(300):
            tmp={}
            if(int((i+1)*step)-int(i*step))>0 :
                for bed in bedfile:
                    tmp[bed]=0
                    if exp[bed].has_key(start+int(i*step)):
                        tmp[bed]=exp[bed][start+int(i*step)]
                        last=nex+1
                        nex = i
                        tmp[bed]=math.log(tmp[bed]+1,2)
                        for j in range(last,nex+1):
                            if mod == "e":
                                exon[bed][j]+=tmp[bed]/(nex-last+1)
                            else :
                                intron[bed][j]+=tmp[bed]/(nex-last+1)
    else :
        for i in range(300):
            tmp={}
            for bed in bedfile:
                tmp[bed]=0
                for j in range(start+int(i*step),start+int((i+1)*step)):
                    if exp[bed].has_key(j):
                        tmp[bed]+=exp[bed][j]
                if mod == "e":
                        exon[bed][i]+=math.log(tmp[bed]/(int((i+1)*step)-int(i*step))+1,2)
                else :
                        intron[bed][i]+=math.log(tmp[bed]/(int((i+1)*step)-int(i*step))+1,2)

for chr in chrs:
    flag={}
    for line in open (reffile):
        if(re.match('#',line)): print chr
        else:
            line=line.rstrip()
            data=line.split('\t')
            if data[2] == chr:
                exonStart,exonEnd=split_f(data[9],data[10])
                for i in range(len(exonStart)):
                    exonlength = exonEnd[i]-exonStart[i]+1
                    for j in range(exonStart[i]-exonlength,exonEnd[i]+exonlength+1):
                        flag[j]=1
                for i in range(len(exonStart)-1):
                    intronlength=exonStart[i+1]-1-exonEnd[i]-1+1
                    for j in range(exonEnd[i]+1-intronlength,exonStart[i+1]-1+intronlength+1):
                        flag[j]=1

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
            exonStart,exonEnd=split_f(data[9],data[10])
            exoncount+=len(exonStart)
            introncount+=len(exonStart)-1
            for i in range(len(exonStart)):
                length=exonEnd[i]-exonStart[i]+1
                scale_count(exonStart[i],exonEnd[i],length,"e")
            for i in range(len(exonStart)-1):
                length=exonStart[i+1]-1-exonEnd[i]-1+1
                scale_count(exonEnd[i]+1,exonStart[i+1]-1,length,"i")

for bed in bedfile:
    exonfile.write("%s"%(bed))
    intronfile.write("%s"%(bed))
    for i in range(300):
        exonfile.write("\t%f"%(exon[bed][i]/exoncount))
        intronfile.write("\t%f"%(intron[bed][i]/introncount))
    exonfile.write("\n")
    intronfile.write("\n")
exonfile.close()
intronfile.close()
