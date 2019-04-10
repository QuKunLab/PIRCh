import sys
peak1file=sys.argv[1]
peak2file=sys.argv[2]
chrfile=sys.argv[3]
#outfile=sys.argv[4]
chrs=[]
for line in open (chrfile):
    line=line.rstrip()
    data=line.split('\t')
    chrs.append(data[0])

total=0

for chr in chrs:
    count={}
    for line in open (peak1file):
        line=line.rstrip()
        data=line.split('\t')
        if data[0] == chr:
            for i in range(int(data[1]),int(data[2])+1):
                count[i]=1

    for line in open(peak2file):
        line=line.rstrip()
        data=line.split('\t')
        if data[0] == chr:
            for i in range(int(data[1]),int(data[2])+1):
                if count.has_key(i):
                    total+=1

print total
