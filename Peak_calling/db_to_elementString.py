#!/usr/bin/python
import sys,os
import commands
import pickle
from optparse import OptionParser
#
opts = OptionParser()
usage = "run db to element string\nusage:%prog [options]"
opts = OptionParser(usage=usage)
opts.add_option("-i",help="dotbracket file directory path")
opts.add_option("-t",help="number of threads")
opts.add_option("-o",help="output file directory path")
opts.add_option("--forgi",help="forgi software downloaded from github path ")
options, arguments = opts.parse_args()
#
input_path=options.i
output_path=options.o
db2element_code_path=options.forgi
thread=options.t
def dot2str():
	return_files,data=commands.getstatusoutput("ls " + input_path +"/*db")
	files=data.split("\n")
	df=open(output_path + "/run.sh","w")
	for i in files:
        	df.write("sed -n '3p' " + i + " | sed 's/ (.*)$//' | python " + db2element_code_path + " - >> " + i +"\n" )
	df.close()
	os.popen("cat " + output_path + "/run.sh | parallel -j " + thread)
	os.popen("rm " +  output_path + "/run.sh" )
#	
def parseDbFile(fileN):
	h = open(fileN)
#	name = h.readline().strip()
	name = h.readline().strip().split(":")[0]
	seq = h.readline()
	sec = h.readline().split(' ')[0]
	ant = h.readline().strip()
 	h.close()
	return name[1:], seq, sec, ant
def pack_elementStr():
	output=output_path + "/transcriptAnot.pickle"
	return_files,data=commands.getstatusoutput("ls " + input_path +"/*db")
	files=data.split("\n")
	dic = {}
	for f in files :
    		n, seq, sec, ant = parseDbFile(f)
   		dic[n] = (seq, sec, ant)
	pickle.dump(dic, open(output,'w'))
def main():
	dot2str()
	pack_elementStr()
if __name__=="__main__":
	main()
