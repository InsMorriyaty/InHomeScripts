import sys

f1 = sys.argv[1]

with open(f1,'r') as infile :
    for line in infile :
        line = line.strip()
        if line.startswith("#") : 
            continue 
        else :
            ifo = line.split("\t")
            chrr = ifo[0].split(":")[0]
            start = int(ifo[3]) + int(ifo[0].split(":")[1].split("-")[0] )
            end = int(ifo[4]) + int(ifo[0].split(":")[1].split("-")[0] )
            print(f"{chrr}\t{ifo[1]}\t{ifo[2]}\t{start}\t{end}\t{ifo[5]}\t{ifo[6]}\t{ifo[7]}\t{ifo[8]}")

