import sys 

f1 = sys.argv[1] # ref.out after 04.--.py
f2 = sys.argv[2] # ref gtf tbl
f3 = sys.argv[3] # ref2qury name

x = {}

with open(f2,'r') as inputfile:
    for line in inputfile :
        line = line.strip().split()
        trans_id = line[5]
        gene_id = line[4]
        x[trans_id] = gene_id

with open(f1,'r') as inputfile :
    for line in inputfile :
        line = line.strip()
        if "Reading chains" in line or "No match found" in line or "Already assigned:" in line :
            continue 
        else :
            kda = line.split()
            if kda[0] in x :
                gene_id = x[kda[0]]
                print(f"{gene_id}\t{f3}_chain{kda[1]}")
