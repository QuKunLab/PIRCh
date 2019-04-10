#this script is used to convert icshape.out result symbol name to refseq transcript name
#you need tarnscript annotation file:mm9_refseq_genes.txt  &&  icshape result file:v65_icshape.out
import numpy
with open('/Users/huangbeibei/Desktop/pirch/h3/mm9_refseq_genes.txt') as f:
    refseq=[x.rstrip().split() for x in f]

del refseq[0]
i=0

while i < len(refseq):
    refseq[i][9]=refseq[i][9].rstrip(',')
    refseq[i][10]=refseq[i][10].rstrip(',')
    refseq[i][9]=map(int,refseq[i][9].split(','))
    refseq[i][10]=map(int,refseq[i][10].split(','))
    refseq[i].append(sum(map(lambda a,b:a - b,refseq[i][10],refseq[i][9])))
    i=i+1


with open('/Users/huangbeibei/Desktop/pirch/h3/v65_icshape.out') as f:
    ic=[x.rstrip().split() for x in f]

for i in ic:
    i[1]=int(i[1])

out={}

for i in ic:
    for j in refseq:
        if (i[0]==j[12]) & (i[1]==j[16]):
            out[j[1]]=i[1:]

for i in out:
    out[i]=['0' if x =='NULL' else x for x in out[i]]
for i in out:
    out[i]=map(float,out[i])

with open('/Users/huangbeibei/Desktop/pirch/h3/h3_low5000.txt') as f:
    peak_low=dict(x.rstrip().split(None,1) for x in f)
with open('/Users/huangbeibei/Desktop/pirch/h3/h3_high5000.txt') as f:
    peak_high=dict(x.rstrip().split(None,1) for x in f)

for i in peak_low:
    peak_low[i]=peak_low[i].split('\t')
for i in peak_low:
    peak_low[i][1]=int(peak_low[i][1])
    peak_low[i][2]=int(peak_low[i][2])

for i in peak_high:
    peak_high[i]=peak_high[i].split('\t')
for i in peak_high:
    peak_high[i][1]=int(peak_high[i][1])
    peak_high[i][2]=int(peak_high[i][2])


peakIC_low={}
peakIC_high={}

for i in peak_low:
    if peak_low[i][0] in out:
        if peak_low[i][1]>=10 & peak_low[i][2]+10<=len(out[peak_low[i][0]]):
            peakIC_low[i]=out[peak_low[i][0]][peak_low[i][1]-8:peak_low[i][2]+13]

for i in peak_high:
    if peak_high[i][0] in out:
         if peak_high[i][1]>=10 & peak_high[i][2]+10<=len(out[peak_high[i][0]]):
            peakIC_high[i]=out[peak_high[i][0]][peak_high[i][1]-8:peak_high[i][2]+13]
print 'high:'
print len(peakIC_high)
print 'low'
print len(peakIC_low)
test_high=[]
for i in peakIC_high:
    if len(peakIC_high[i])!=25:
        test_high.append(i)
for i in test_high:
    del peakIC_high[i]

test_low=[]
for i in peakIC_low:
    if len(peakIC_low[i])!=25:
        test_low.append(i)
for i in test_low:
    del peakIC_low[i]

peakIC_low_mean=[numpy.mean(i) for i in zip(*peakIC_low.values())]
peakIC_high_mean=[numpy.mean(i) for i in zip(*peakIC_high.values())]

with open('/Users/huangbeibei/Desktop/pirch/h3/h3_low5000_mean.txt','w') as f:
    for i in peakIC_low_mean:
        f.write('%s,'%i)
with open('/Users/huangbeibei/Desktop/pirch/h3/h3_high5000_mean.txt','w') as f:
    for i in peakIC_high_mean:
        f.write('%s,'%i)

