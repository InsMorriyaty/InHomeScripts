import sys 

f1 = sys.argv[1] ### gff
f2 = sys.argv[2] ### id 

x = []

with open(f2,'r') as infile1 :
    for line in infile1 :
        line = line.strip().split()
        x.append(line[0])

with open(f1,'r') as infile2 :
    for line in infile2 :
        line = line.strip()
        kda = line.split("\t") 
        inff = kda[-1]
        for i in x :
            if i in inff :
                print(line)
