import sys 

f1 = sys.argv[1] # species 

clusterFile = "AnchorsCluster.v3.py.tmp"
maploactFile = f"{f1}_OR_Filter_Intermediate/{f1}.OR.Filter.loact.stat"
outfile = f"{f1}_OR_Filter_Intermediate/{f1}.OR.Filter.loact.cluster.stat"
x = {}

with open(clusterFile,'r') as inputfile0 :
    for line in inputfile0 :
        line = line.strip().split()
        x[line[1]] = line[0]

with open(maploactFile,'r') as inputfile1 , open(outfile,'w') as inputfile2 :
    for line in inputfile1 :
        line = line.strip().split()
        cluster = ""
        for i in x :
            if line[0] in i  :
                cluster = x[i]
                break
            else :
                continue
        if cluster :
            inputfile2.write(f"{line[0]}\t{cluster}\t{line[1]}\t{line[2]}\t{line[3]}\t{line[4]}\t{line[5]}\n")
        else :
            inputfile2.write(f"{line[0]}\tNone\t{line[1]}\t{line[2]}\t{line[3]}\t{line[4]}\t{line[5]}\n")
