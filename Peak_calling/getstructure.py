#!/usr/bin/env python
import pickle
import sys
import os
from tabformat import parseTranscriptPeaks
from optparse import OptionParser
#
opts = OptionParser()
usage = "run scripts to get structure annotation for eCLIP data\nusage:%prog -e extend_number -i input peakfile -s pars structure_ref -o ouput file -p another output file "
opts = OptionParser(usage=usage)
opts.add_option("-e", help="number to extend of central position")
opts.add_option("-i", help="peak file generated from eCLIP data")
opts.add_option("-s", help="structure annotation generated from PARS")
opts.add_option("-o", help="output file for downstream analysis")
opts.add_option("-p", help="output file for downstream analysis")
options, arguments = opts.parse_args()
#
extend=options.e
peak=options.i
structure=options.s
out1=options.o
out2=options.p
#
extend = int(extend)
structDic = pickle.load(open(structure))
openPeak = open(peak)
output1 = open(out1, 'w')
output2=open(out2,'w')

def getSeqAndStruct(seq, struct, ext, st, en):
    begin = st-ext-1
    if (begin < 0): return None
    end = en + ext
    if (end >= len(struct)): return None
    return seq[begin:end], struct[begin:end]

def fromPeaks1(ext, intervals, pvs, ts, seq, struct, anot):
    for i in range(len(intervals)):
        ans = getSeqAndStruct(seq, struct, ext, *intervals[i])
        if ans != None:
            yield (pvs[i], sum(intervals[i])/2, ts[i], ans[0], ans[1])
def fromPeaks2(ext, intervals, pvs, ts, seq, struct, anot):
    for i in range(len(intervals)):
        ans = getSeqAndStruct(seq, anot, ext, *intervals[i])
        if ans != None:
            yield (pvs[i], sum(intervals[i])/2, ts[i], ans[0], ans[1])
for line in openPeak:
    n, intervLis, pvLis, times = parseTranscriptPeaks(line)
    if structDic.has_key(n):
        for p, mid, t, seq, stru in fromPeaks1(extend, intervLis, pvLis, times, *structDic[n]):
            print >> output1, '\t'.join([n, str(mid), seq, stru, str(p), str(t)])
	for p, mid, t, seq, anot in fromPeaks2(extend, intervLis, pvLis, times, *structDic[n]):
	    print >> output2, '\t'.join([n, str(mid), seq, anot, str(p), str(t)])
