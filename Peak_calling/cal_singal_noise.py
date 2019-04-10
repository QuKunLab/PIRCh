#!/usr/bin/python
import sys,os
import numpy
merged_rt=sys.argv[1]
mock_rt=sys.argv[2]
peaktxt=sys.argv[3]
output1=sys.argv[4]
output2=sys.argv[5]
###
def dic_rt(file_rt):
	with open(file_rt) as f:
		ic=[x.rstrip().split("\t") for x in f]
	out={}
	for i in ic:
		if len(i) > 1:
    			out[i[0]]=i[1].split(";")
	for i in out:
    		out[i]=['0' if x =='NULL' else x for x in out[i]]
	for i in out:
    		out[i]=map(float,out[i])
	return out
###
def dic_peak(peaktxt,out):
	with open(peaktxt) as f:
    		peak=dict(x.rstrip().split(None,1) for x in f)
	for i in peak:
		peak[i]=peak[i].split('\t')
	for i in peak:
		peak[i][0]=int(peak[i][0])
		peak[i][1]=int(peak[i][1])
	peakIC={}
	for i in peak:
    		if i in out:
         		peakIC[i]=out[i][peak[i][0]-200:peak[i][1]+201]

	test=[]
	for i in peakIC:
    		if len(peakIC[i])!=405:
        		test.append(i)
	for i in test:
		del peakIC[i]

	print 'len(peak):',len(peakIC)
	peakIC_mean=[numpy.mean(i) for i in zip(*peakIC.values())]
	peakIC_mean=[str(i) for i in peakIC_mean]
	return peakIC_mean
out1=dic_rt(merged_rt)
out2=dic_rt(mock_rt)
peakIC_mean1=dic_peak(peaktxt,out1)
peakIC_mean2=dic_peak(peaktxt,out2)
with open(output1,'w') as f1:
	f1.write(','.join(peakIC_mean1) + "\n")
with open(output2,'w') as f2:
	f2.write(','.join(peakIC_mean2) + "\n")

