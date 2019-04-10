#!/usr/bin/python

import numpy as np
import bisect as bi
import sys
from tabformat import parseTab, packTranscriptPeaks
from optparse import OptionParser
#
opts = OptionParser()
usage="run callpeak.py\n%prog --ws windows number -n threshold number -s sample time -i input file -o output file "
opts = OptionParser(usage=usage)
opts.add_option("--ws", help="windows number")
opts.add_option("-n", help="threshold number")
opts.add_option("-s", help="sample time")
opts.add_option("-i", help="input merged_file")
opts.add_option("-o", help="ouput peak_file")
options, arguments = opts.parse_args()
#
ws=options.ws
thre=options.n
sampleTime=options.s
inp=options.i
oup=options.o
def applyWindow(lis, ws):
    half = int(ws /2)
    return np.array([sum(lis[i:i+ws]) for i in range(0, len(lis)-ws+1, half)])

def select(arr, thre):
    med = np.median(filter(lambda x:x!=0,arr))
    pos = np.where((arr>thre*med))[0]
    return pos, med

def group(pos):
    ans = [[pos[0]]]
    now = 0
    pre = pos[0]
    for p in pos[1:]:
        if (p - pre == 1):
            ans[now].append(p)
        else:
            now += 1
            ans.append([p])
        pre = p
    return np.array(ans)

def getOnePeak(pos, arr):
    gp = group(pos)
    ans = []
    for ps in gp:
        ans.append(ps[np.argmax(arr[ps])])
    return np.array(ans)

def peakDetect(lis, ws, thre):
    arr = applyWindow(lis, ws)
    half = int(ws/2)
    pos, med = select(arr, thre)
    if (len(pos)==0):
        return np.array([]), np.array([]), 1
    final = getOnePeak(pos, arr)
    return half * final, arr[final], med

def readTab(line):
    name, tabs = line.split('\t')
    arr = np.array(parseTab(tabs))
    return name, arr

def pvalueEstimate(samplePool, value):
    return 1.0 - bi.bisect_left(samplePool, value)/float(len(samplePool))

def generateSample(tab, ws, n):
    samples = [sum(np.random.choice(tab, ws)) for _ in range(n)]
    samples.sort()
    return samples

def getPeak(line, ws, thre, n):
    name, tab = readTab(line)
    samples = generateSample(tab, ws, n)
    st, val, med = peakDetect(tab, ws, thre)
    pval = [pvalueEstimate(samples, v) for v in val]
    return name, st, pval, val/float(med)


ws = int(ws)
thre = int(thre)
sampleTime = int(sampleTime)
inpF = open(inp)
oupF = open(oup, 'w')
for line in inpF:
    out = packTranscriptPeaks(ws, *getPeak(line, ws, thre, sampleTime))
    if (out != ""):
        oupF.write(out)
