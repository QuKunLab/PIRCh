#!/usr/bin/python
import itertools as it
import re
import sys
import numpy as np
from tabformat import packTab
from optparse import OptionParser
#
opts = OptionParser()
usage="run rtCounts\nusage:%prog -l halfLength -m minimum -i input bam_file -o output file -a annotation file"
opts = OptionParser(usage=usage)
opts.add_option("-l", help="halflength")
opts.add_option("-m", help="minimum")
opts.add_option("-i", help="input bam_file")
opts.add_option("-o", help="output file")
opts.add_option("-a", help="annotation file")
options, arguments = opts.parse_args()
#
halfLength=options.l
annotation=options.a
minimumNumber=options.m
inp=options.i
oup=options.o
def checkRev(flag):
    return flag & 16

def checkUnmap(flag):
    return flag & 4

def readSam(fileH):
    for line in fileH:
        if line[0] == '@':
            pass
        else:
            sps=line.split('\t')
            flag = int(sps[1])
            if checkUnmap(flag):
                pass
            else:
                yield(sps)

def cigarToLength(cigar):
    return sum(map(int ,re.findall('\d+', cigar)))

def parseSam(record):
    flag = int(record[1])
    chro = record[2]
    pos = int(record[3])
    rev = 0
    if checkRev(flag):
        rev = 1
        seqL = cigarToLength(record[5])
        pos = pos + seqL - 1
    return rev, chro, pos

def parseSamFile(fileH):
    return it.imap(parseSam, readSam(fileH))



def addToDict(dic, key, value):
    if dic.has_key(key):
        dic[key] += value
    else:
        dic[key] = value

def generateChromo(parsedSam, halfLength):
    dic = {}
    tot = 0
    for rev, chro, pos in parsedSam:
        tot += 1
        if not(dic.has_key(chro)):
            dic[chro] = [{}, {}]
        countDic = dic[chro][rev]
        for i in range(pos-halfLength, pos+halfLength + 1):
            addToDict(countDic, i, 1)
    return dic, tot
#
def parseAnnotation(fileN):
    inp = open(fileN)
    inp.readline()
    for line in inp:
        data = line.split('\t')
        sts = map(int, data[9].split(',')[:-1])
        ens = map(int, data[10].split(',')[:-1])
        if data[3] == '-':
            rev = 1
        else:
            rev = 0
        yield data[1], data[2], rev, sts, ens
    inp.close()

def readAnnotation(fileN):
    allExons = {}
    for name, chro, rev, sts, ens in parseAnnotation(fileN):
        if not(allExons.has_key(chro)):
            allExons[chro]=[[], []]
        allExons[chro][rev].append((name, sts, ens))
    return allExons

inp_file=open(inp)
chroDic, tot = generateChromo(parseSamFile(inp_file), int(halfLength))
inp_file.close()
#chroDic, tot = generateChromo(parseSamFile(open(inp)), int(halfLength))

print "sam file loaded"

output = open(oup, 'w')
minimumNumber = int(minimumNumber)
for name, chro, rev, sts, ens in parseAnnotation(annotation):
    if chroDic.has_key(chro):
        tab = chroDic[chro][rev]
        geneTab = []
        totalR = 0
        # geneLen = sum(np.array(ens) - np.array(sts))
        for k in range(len(sts)):
            for i in range(sts[k], ens[k] + 1):
                if tab.has_key(i):
                    v = tab[i]
                    geneTab.append(v)
                    totalR += v
                else : geneTab.append(0)
        if rev == 1:
            geneTab.reverse()
        # if (float(totalR)/tot/geneLen * 10**8 > minimumNumber):
        if (totalR > minimumNumber):
            output.write('\t'.join([name, packTab([float(x)/tot for x in geneTab])])+'\n')
        else:
            output.write(name + "\t\n")
output.close()
