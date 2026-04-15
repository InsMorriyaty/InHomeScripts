import sys 
import random

f1 = sys.argv[1]
f2 = sys.argv[2]

x = {}
sid = {}
sp = f1.split(".")[0]

with open(f2,'r') as infile1 :
    for line in infile1 :
        line = line.strip().split()
        k = line[0].replace(">","")
        v = " ".join(line[0:])
        x[k] = v 
num = str(random.randint(10000, 99999))
outname = f"{sp}.tmp.{num}"

with open(f1,'r') as infile2 , open(outname,'w') as outfile : 
    for line in infile2 :
        line = line.strip().split()
        kda = line[1]
        if kda in x :
            outfile.write(f"{line[0]}\t{x[kda]}\n")
